"""End-to-end account flows: HTML with real CSRF and mobile JSON sessions."""

import re
import time
from datetime import datetime, timedelta
from unittest.mock import patch
from urllib.parse import urlsplit

from allauth.account.models import EmailAddress
from django.contrib.auth import SESSION_KEY
from django.contrib.sessions.models import Session
from django.core import mail
from django.core.cache import cache
from django.db import IntegrityError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import User, UserRole

PASSWORD = "Rzeka-zielona-784!Bezpieczna"
NEW_PASSWORD = "Nowa-fala-902!Spokojna"
MOBILE = "/api/auth/app/v1/auth/"


class AuthFlowTests(TestCase):
    def setUp(self):
        cache.clear()
        self.browser = Client(enforce_csrf_checks=True)

    def account(self, email="konto@example.test", role="employee", verified=True, **kwargs):
        user = User.objects.create_user(email, PASSWORD, **kwargs)
        UserRole.objects.create(user=user, role=role)
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=verified)
        return user

    def form_post(self, path, data, browser=None, **kwargs):
        browser = browser or self.browser
        page = browser.get(path, follow=True)
        self.assertEqual(page.status_code, 200)
        return browser.post(
            path,
            {**data, "csrfmiddlewaretoken": browser.cookies["csrftoken"].value},
            **kwargs,
        )

    def signup(self, role="employee", email="osoba@example.test", **extra):
        return self.form_post(
            reverse("account_signup"),
            {
                "role": role,
                "email": email,
                "password1": PASSWORD,
                "password2": PASSWORD,
                **extra,
            },
        )

    def login(self, user, browser=None, **extra):
        return self.form_post(
            reverse("account_login"),
            {
                "login": user.email.upper(),
                "password": PASSWORD,
                **extra,
            },
            browser=browser,
        )

    def mail_path(self, fragment):
        urls = re.findall(r"https?://[^\s<>]+", mail.outbox[-1].body)
        return urlsplit(next(url for url in urls if fragment in url)).path

    def mobile_post(self, action, data, token=None, client=None):
        headers = {"HTTP_X_SESSION_TOKEN": token} if token else {}
        return (client or self.client).post(
            MOBILE + action, data, content_type="application/json", **headers
        )

    def mobile_login(self, user):
        response = self.mobile_post("login", {"email": user.email, "password": PASSWORD})
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()["meta"]["session_token"]

    def test_full_web_registration_verification_login_and_logout_for_both_roles(self):
        for role in UserRole.Role.values:
            with self.subTest(role=role):
                self.browser = Client(enforce_csrf_checks=True)
                response = self.signup(role, email=f"{role.upper()}@Example.test")
                self.assertRedirects(response, reverse("account_email_verification_sent"))
                user = User.objects.get(email=f"{role}@example.test")
                self.assertEqual(list(user.roles.values_list("role", flat=True)), [role])
                self.assertTrue(user.check_password(PASSWORD))
                self.assertFalse(user.is_staff or user.is_superuser)
                self.assertNotIn(SESSION_KEY, self.browser.session)
                path = self.mail_path("confirm-email/")
                self.assertContains(self.browser.get(path), user.email)
                self.assertFalse(EmailAddress.objects.get(user=user).verified)
                confirmed = self.form_post(path, {})
                self.assertRedirects(confirmed, reverse("account_login"))
                self.assertTrue(EmailAddress.objects.get(user=user).verified)
                self.assertNotIn(SESSION_KEY, self.browser.session)
                self.assertRedirects(self.login(user), reverse("account_home"))
                self.assertContains(
                    self.browser.get(reverse("account_home")), UserRole.Role(role).label
                )
                self.assertEqual(self.browser.get("/api/v1/me/").json()["roles"], [role])
                self.browser.get(reverse("account_logout"))
                self.assertIn(SESSION_KEY, self.browser.session)
                self.form_post(reverse("account_logout"), {})
                self.assertEqual(self.browser.get("/api/v1/me/").status_code, 403)

    def test_role_choice_is_required_and_client_cannot_create_admin_or_change_flags(self):
        for role in ("", "admin", "staff", "EMPLOYER"):
            with self.subTest(role=role):
                response = self.signup(role)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors.get("role"))
                self.assertFalse(User.objects.exists())
        cache.clear()
        self.signup("employer", is_staff="true", is_superuser="true", roles=["employee"])
        user = User.objects.get()
        self.assertFalse(user.is_staff or user.is_superuser)
        self.assertEqual(list(user.roles.values_list("role", flat=True)), ["employer"])

    def test_invalid_email_weak_mismatched_and_similar_passwords_create_nothing(self):
        cases = [
            {"email": "niepoprawny"},
            {"password1": "short", "password2": "short"},
            {"password2": "inna-wartosc-9874!"},
            {
                "email": "abc.def@example.test",
                "password1": "abc.def@example.test",
                "password2": "abc.def@example.test",
            },
        ]
        for data in cases:
            with self.subTest(data=data):
                response = self.signup(**data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                self.assertFalse(User.objects.exists())

    def test_duplicate_email_has_generic_response_without_adding_role_or_changing_password(self):
        user = self.account()
        response = self.signup(
            "employer", email=user.email.upper(), password1=NEW_PASSWORD, password2=NEW_PASSWORD
        )
        self.assertRedirects(response, reverse("account_email_verification_sent"))
        self.assertEqual(User.objects.count(), 1)
        user.refresh_from_db()
        self.assertTrue(user.check_password(PASSWORD))
        self.assertEqual(list(user.roles.values_list("role", flat=True)), ["employee"])

    def test_email_conflict_after_validation_has_generic_response(self):
        user = self.account()
        with patch(
            "allauth.account.forms.BaseSignupForm.validate_unique_email", lambda form, value: value
        ):
            response = self.signup("employer", email=user.email)
        self.assertRedirects(response, reverse("account_email_verification_sent"))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserRole.objects.count(), 1)

    def test_signup_rolls_back_if_role_cannot_be_saved(self):
        with patch(
            "apps.accounts.signup_fields.UserRole.objects.create",
            side_effect=IntegrityError("forced role failure"),
        ):
            with self.assertRaises(IntegrityError):
                self.signup()
        self.assertFalse(User.objects.exists())
        self.assertFalse(EmailAddress.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_unverified_accounts_cannot_login_or_access_private_api_even_with_a_session(self):
        user = self.account(verified=False)
        self.assertRedirects(self.login(user), reverse("account_email_verification_sent"))
        self.assertNotIn(SESSION_KEY, self.browser.session)
        self.browser.force_login(user)
        self.assertEqual(self.browser.get("/api/v1/me/").status_code, 403)
        self.assertEqual(self.browser.get(reverse("account_home")).status_code, 403)

    def test_wrong_password_and_unknown_email_have_the_same_error(self):
        user = self.account()
        errors = []
        for email in (user.email, "nieznany@example.test"):
            response = self.form_post(
                reverse("account_login"), {"login": email, "password": "Nieprawidlowe-675!"}
            )
            self.assertNotIn(SESSION_KEY, self.browser.session)
            errors.append(response.context["form"].non_field_errors())
        self.assertEqual(errors[0], errors[1])

    def test_inactive_account_cannot_login_on_web_or_mobile(self):
        user = self.account(is_active=False)
        self.login(user)
        self.assertNotIn(SESSION_KEY, self.browser.session)
        response = self.mobile_post("login", {"email": user.email, "password": PASSWORD})
        self.assertFalse(response.json().get("meta", {}).get("is_authenticated", False))
        self.assertNotEqual(response.status_code, 200)

    def test_remember_me_cookie_and_browser_session_expiry(self):
        user = self.account()
        self.login(user)
        self.assertTrue(self.browser.session.get_expire_at_browser_close())
        self.form_post(reverse("account_logout"), {})
        self.login(user, remember="on")
        self.assertFalse(self.browser.session.get_expire_at_browser_close())
        self.assertEqual(self.browser.session.get_expiry_age(), 14 * 86400)

    def test_login_rotates_session_and_rejects_external_redirects(self):
        user = self.account()
        session = self.browser.session
        session["pre_login"] = True
        session.save()
        old_key = session.session_key
        response = self.login(user, next="https://foreign.example/steal")
        self.assertRedirects(response, reverse("account_home"))
        self.assertNotEqual(self.browser.session.session_key, old_key)
        self.assertFalse(Session.objects.filter(session_key=old_key).exists())

    def test_email_confirmation_rejects_invalid_expired_and_used_links(self):
        self.signup()
        path = self.mail_path("confirm-email/")
        with patch("django.core.signing.time.time", return_value=time.time() + 2 * 86400):
            self.assertContains(self.browser.get(path), "Ten link już nie działa")
        self.assertFalse(EmailAddress.objects.get().verified)
        self.form_post(path, {})
        self.assertContains(self.browser.get(path), "Ten link już nie działa")
        self.assertContains(
            self.browser.get("/konta/confirm-email/niepoprawny/"), "Ten link już nie działa"
        )

    def test_resend_is_generic_and_cooldown_limits_mail(self):
        user = self.account(verified=False)
        path = reverse("resend_verification")
        known = self.form_post(path, {"email": user.email})
        self.assertEqual(len(mail.outbox), 1)
        self.form_post(path, {"email": user.email.upper()})
        self.assertEqual(len(mail.outbox), 1)
        unknown = self.form_post(path, {"email": "nobody@example.test"})
        self.assertEqual(known.url, unknown.url)
        self.assertEqual(len(mail.outbox), 1)
        self.form_post(self.mail_path("confirm-email/"), {})
        self.assertTrue(EmailAddress.objects.get().verified)

    def test_web_password_reset_rejects_reuse_and_revokes_other_web_and_mobile_sessions(self):
        user = self.account()
        self.login(user)
        token = self.mobile_login(user)
        resetter = Client(enforce_csrf_checks=True)
        self.form_post(reverse("account_reset_password"), {"email": user.email}, browser=resetter)
        path = self.mail_path("password/reset/key/")
        page = resetter.get(path, follow=True)
        # allauth removes the secret from the URL before displaying the form.
        self.assertNotIn(path, [page.request["PATH_INFO"]])
        response = self.form_post(
            page.request["PATH_INFO"],
            {"password1": NEW_PASSWORD, "password2": NEW_PASSWORD},
            browser=resetter,
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.check_password(NEW_PASSWORD))
        self.assertFalse(user.check_password(PASSWORD))
        self.assertNotIn(SESSION_KEY, resetter.session)
        self.assertEqual(self.browser.get("/api/v1/me/").status_code, 403)
        self.assertEqual(
            self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=token).status_code, 403
        )
        self.assertContains(Client().get(path, follow=True), "Ten link już nie działa")

    def test_expired_reset_token_is_rejected(self):
        user = self.account()
        self.form_post(reverse("account_reset_password"), {"email": user.email})
        path = self.mail_path("password/reset/key/")
        with patch(
            "django.contrib.auth.tokens.PasswordResetTokenGenerator._now",
            return_value=datetime.now() + timedelta(hours=2),
        ):
            self.assertContains(self.browser.get(path, follow=True), "Ten link już nie działa")
        self.assertTrue(User.objects.get().check_password(PASSWORD))

    def test_password_reset_does_not_disclose_unknown_or_inactive_account(self):
        user = self.account()
        inactive = self.account("inactive@example.test", is_active=False)
        responses = [
            self.form_post(reverse("account_reset_password"), {"email": email})
            for email in (user.email, "nobody@example.test", inactive.email)
        ]
        self.assertEqual({r.url for r in responses}, {reverse("account_reset_password_done")})
        self.assertEqual(len(mail.outbox), 1)

    def test_password_change_requires_old_password_and_logs_out(self):
        user = self.account()
        token = self.mobile_login(user)
        self.login(user)
        path = reverse("account_change_password")
        bad = self.form_post(
            path, {"oldpassword": "wrong", "password1": NEW_PASSWORD, "password2": NEW_PASSWORD}
        )
        self.assertTrue(bad.context["form"].errors)
        response = self.form_post(
            path, {"oldpassword": PASSWORD, "password1": NEW_PASSWORD, "password2": NEW_PASSWORD}
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(SESSION_KEY, self.browser.session)
        self.assertEqual(
            self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=token).status_code, 403
        )

    def test_all_browser_mutations_require_csrf(self):
        for name in (
            "account_login",
            "account_signup",
            "account_reset_password",
            "account_logout",
            "resend_verification",
        ):
            with self.subTest(name=name):
                self.assertEqual(self.browser.post(reverse(name), {}).status_code, 403)
        self.signup()
        path = self.mail_path("confirm-email/")
        self.assertEqual(Client(enforce_csrf_checks=True).post(path).status_code, 403)
        self.assertFalse(EmailAddress.objects.get().verified)

    @override_settings(ACCOUNT_RATE_LIMITS={"signup": "1/m/ip"})
    def test_signup_rate_limit_is_shared_across_clients_and_ignores_forged_proxy_header(self):
        self.signup()
        response = self.mobile_post(
            "signup",
            {"email": "other@example.test", "password": PASSWORD, "role": "employer"},
            client=Client(HTTP_X_FORWARDED_FOR="8.8.8.8"),
        )
        self.assertEqual(response.status_code, 429)
        self.assertEqual(User.objects.count(), 1)

    @override_settings(ACCOUNT_RATE_LIMITS={"login": "1/m/ip"})
    def test_login_throttling_has_a_polish_page(self):
        self.form_post(reverse("account_login"), {"login": "x@example.test", "password": "wrong"})
        response = self.form_post(
            reverse("account_login"), {"login": "x@example.test", "password": "wrong"}
        )
        self.assertContains(response, "Chwila przerwy", status_code=429)

    def test_worker_and_employer_entry_links_preselect_only_known_roles(self):
        for query, expected in (
            ("", "employee"),
            ("?role=employer", "employer"),
            ("?role=admin", "employee"),
        ):
            response = self.browser.get(reverse("account_signup") + query)
            self.assertEqual(response.context["form"]["role"].value(), expected)

    def test_account_pages_are_private_and_do_not_leak_tokens_to_referrers(self):
        response = self.browser.get(reverse("account_login"))
        self.assertIn("no-store", response["Cache-Control"])
        self.assertEqual(response["Referrer-Policy"], "no-referrer")
        self.assertContains(response, '<html lang="pl">')

    def test_email_tokens_use_configured_origin_instead_of_request_host(self):
        with override_settings(OOKULAR_PUBLIC_ORIGIN="https://accounts.example.test"):
            self.signup()
            self.assertIn(
                "https://accounts.example.test/konta/confirm-email/", mail.outbox[-1].body
            )
            self.form_post(reverse("account_reset_password"), {"email": "osoba@example.test"})
            self.assertIn(
                "https://accounts.example.test/konta/password/reset/key/", mail.outbox[-1].body
            )

    def test_admin_uses_throttled_portal_login_and_rejects_business_roles(self):
        response = self.browser.get("/admin/login/")
        self.assertEqual(urlsplit(response.url).path, reverse("account_login"))
        user = self.account(role="employer")
        self.login(user)
        self.assertEqual(self.browser.get("/admin/login/").status_code, 403)

    def test_mobile_registration_verification_login_logout_for_both_roles(self):
        for role in UserRole.Role.values:
            with self.subTest(role=role):
                response = self.mobile_post(
                    "signup", {"email": f"{role}@example.test", "password": PASSWORD, "role": role}
                )
                self.assertEqual(response.status_code, 401, response.content)
                self.assertFalse(response.json()["meta"]["is_authenticated"])
                pending = response.json()["meta"]["session_token"]
                self.assertEqual(
                    self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=pending).status_code, 403
                )
                key = self.mail_path("confirm-email/").rstrip("/").split("/")[-1]
                verified = self.mobile_post("email/verify", {"key": key}, token=pending)
                self.assertIn(verified.status_code, (200, 401))
                user = User.objects.get(email=f"{role}@example.test")
                self.assertTrue(EmailAddress.objects.get(user=user).verified)
                token = self.mobile_login(user)
                own = self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=token)
                self.assertEqual(
                    own.json(), {"id": str(user.pk), "email": user.email, "roles": [role]}
                )
                self.assertEqual(
                    self.client.get("/api/v1/modules/", HTTP_X_SESSION_TOKEN=token).status_code, 403
                )
                self.assertEqual(
                    self.client.delete(MOBILE + "session", HTTP_X_SESSION_TOKEN=token).status_code,
                    401,
                )
                self.assertEqual(
                    self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=token).status_code, 403
                )

    def test_mobile_validation_and_duplicate_do_not_change_existing_role(self):
        for role in ("admin", "", None):
            response = self.mobile_post(
                "signup", {"email": "new@example.test", "password": PASSWORD, "role": role}
            )
            self.assertEqual(response.status_code, 400)
        response = self.mobile_post(
            "signup",
            {
                "email": "example.person@example.test",
                "password": "example.person@example.test",
                "role": "employee",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.exists())
        user = self.account()
        response = self.mobile_post(
            "signup",
            {
                "email": user.email.upper(),
                "password": NEW_PASSWORD,
                "role": "employer",
                "is_staff": True,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserRole.objects.get().role, "employee")
        self.assertFalse(User.objects.get().is_staff)
        self.assertTrue(User.objects.get().check_password(PASSWORD))

    def test_mobile_resend_and_reset_password(self):
        user = self.account(verified=False)
        response = self.mobile_post("email/verify/resend", {"email": user.email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        response = self.mobile_post("password/request", {"email": user.email})
        self.assertEqual(response.status_code, 200)
        path = self.mail_path("password/reset/key/")
        key = path.rstrip("/").split("/")[-1]
        response = self.mobile_post("password/reset", {"key": key, "password": NEW_PASSWORD})
        self.assertIn(response.status_code, (200, 401))
        self.assertTrue(User.objects.get().check_password(NEW_PASSWORD))
        response = self.mobile_post("password/reset", {"key": key, "password": PASSWORD})
        self.assertEqual(response.status_code, 400)

    def test_mobile_session_expires_and_deactivation_revokes_access(self):
        user = self.account()
        token = self.mobile_login(user)
        Session.objects.filter(session_key=token).update(
            expire_date=timezone.now() - timedelta(seconds=1)
        )
        self.assertEqual(
            self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=token).status_code, 403
        )
        token = self.mobile_login(user)
        user.is_active = False
        user.save()
        self.assertEqual(
            self.client.get("/api/v1/me/", HTTP_X_SESSION_TOKEN=token).status_code, 403
        )
        self.assertEqual(
            self.client.get(MOBILE + "session", HTTP_X_SESSION_TOKEN=token).status_code, 401
        )

    def test_native_api_ignores_browser_cookies_and_rejects_non_json_writes(self):
        user = self.account()
        self.login(user)
        self.assertEqual(self.browser.get(MOBILE + "session").status_code, 401)
        response = self.browser.post(MOBILE + "login", {"email": user.email, "password": PASSWORD})
        self.assertEqual(response.status_code, 400)
        self.assertIn(SESSION_KEY, self.browser.session)

    def test_changing_email_requires_confirmation_and_preserves_role(self):
        user = self.account(role="employer")
        self.login(user)
        response = self.form_post(
            reverse("account_email"),
            {"email": "nowa-skrzynka@example.test", "action_add": ""},
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.email, "konto@example.test")
        pending = EmailAddress.objects.get(email="nowa-skrzynka@example.test")
        self.assertFalse(pending.verified)
        path = self.mail_path("confirm-email/")
        self.form_post(path, {})
        user.refresh_from_db()
        self.assertEqual(user.email, "nowa-skrzynka@example.test")
        self.assertEqual(list(user.roles.values_list("role", flat=True)), ["employer"])
        self.assertEqual(self.browser.get("/api/v1/me/").json()["email"], user.email)

    def test_mobile_signup_cannot_inject_staff_flags(self):
        response = self.mobile_post(
            "signup",
            {
                "email": "new-employer@example.test",
                "password": PASSWORD,
                "role": "employer",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        self.assertEqual(response.status_code, 401)
        user = User.objects.get()
        self.assertFalse(user.is_staff or user.is_superuser)
        self.assertEqual(UserRole.objects.get().role, "employer")
