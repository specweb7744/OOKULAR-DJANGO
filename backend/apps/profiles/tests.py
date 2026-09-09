from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from allauth.account.models import EmailAddress
from django.core.cache import cache
from django.db import close_old_connections, connection
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User, UserRole

from .models import EmployeeProfile
from .services import DraftConflict, save_draft

API = "/api/v1/me/employee-profile/"
PASSWORD = "Szkic-profilu-test-947!"


def account(email="employee@profiles.example.test", role="employee", verified=True, **kwargs):
    user = User.objects.create_user(email, PASSWORD, **kwargs)
    if role:
        UserRole.objects.create(user=user, role=role)
    EmailAddress.objects.create(user=user, email=user.email, verified=verified, primary=True)
    return user


class EmployeeProfileTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = account()
        self.browser = Client(enforce_csrf_checks=True)
        self.browser.force_login(self.user)
        self.path = reverse("employee_profile")
        self.api = APIClient()
        self.api.force_authenticate(self.user)

    def post(self, data, browser=None):
        browser = browser or self.browser
        browser.get("/konta/password/reset/")
        return browser.post(
            self.path, {**data, "csrfmiddlewaretoken": browser.cookies["csrftoken"].value}
        )

    def test_reading_and_head_do_not_create_a_draft(self):
        self.assertEqual(self.browser.get(self.path).status_code, 200)
        self.assertEqual(self.api.head(API).status_code, 200)
        self.assertEqual(
            self.api.get(API).json(),
            {
                "display_name": "",
                "location": "",
                "desired_role": "",
                "career_goal": "",
                "revision": 0,
                "updated_at": None,
                "status": "draft",
                "visibility": "private",
                "schema_version": 1,
            },
        )
        self.assertFalse(EmployeeProfile.objects.exists())

    def test_partial_web_draft_survives_a_new_session_and_links_from_account(self):
        home = self.browser.get(reverse("account_home"))
        self.assertContains(home, "Rozpocznij profil")
        saved = self.post({"revision": 0, "display_name": "  Ola  "})
        self.assertRedirects(saved, self.path)
        second = Client(enforce_csrf_checks=True)
        second.force_login(self.user)
        page = second.get(self.path)
        self.assertEqual(page.context["form"]["display_name"].value(), "Ola")
        self.assertEqual(page.context["form"]["revision"].value(), 1)
        self.assertContains(second.get(reverse("account_home")), "Wróć do szkicu")
        self.assertEqual(EmployeeProfile.objects.count(), 1)
        self.assertEqual(self.api.get(API).json()["display_name"], "Ola")

    def test_empty_draft_is_allowed_and_patch_preserves_omitted_fields(self):
        first = self.api.patch(API, {"revision": 0}, format="json")
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json()["revision"], 1)
        self.api.patch(
            API, {"revision": 1, "display_name": "Łukasz", "location": "Gdańsk"}, format="json"
        )
        changed = self.api.patch(API, {"revision": 2, "career_goal": "Nowy zawód"}, format="json")
        self.assertEqual(changed.json()["display_name"], "Łukasz")
        self.assertEqual(changed.json()["location"], "Gdańsk")
        cleared = self.api.patch(API, {"revision": 3, "location": " "}, format="json")
        self.assertEqual(cleared.json()["location"], "")
        self.assertEqual(cleared.json()["career_goal"], "Nowy zawód")
        self.assertEqual(cleared.json()["revision"], 4)

    def test_anonymous_and_unverified_accounts_are_rejected(self):
        self.assertRedirects(
            Client().get(self.path), reverse("account_login") + "?next=" + self.path
        )
        self.assertEqual(APIClient().get(API).status_code, 403)
        EmailAddress.objects.filter(user=self.user).update(verified=False)
        self.assertEqual(self.browser.get(self.path).status_code, 403)
        self.assertEqual(self.post({"revision": 0}).status_code, 403)
        self.assertEqual(self.api.get(API).status_code, 403)
        self.assertEqual(self.api.patch(API, {"revision": 0}, format="json").status_code, 403)
        self.assertFalse(EmployeeProfile.objects.exists())

    def test_employer_staff_and_no_role_do_not_bypass_employee_permission(self):
        for role, staff in (("employer", False), ("employer", True), (None, True)):
            with self.subTest(role=role, staff=staff):
                user = account(f"{role}-{staff}@profiles.example.test", role=role, is_staff=staff)
                self.browser.force_login(user)
                self.api.force_authenticate(user)
                self.assertEqual(self.browser.get(self.path).status_code, 403)
                self.assertEqual(self.post({"revision": 0}).status_code, 403)
                self.assertEqual(self.api.get(API).status_code, 403)
                self.assertEqual(
                    self.api.patch(API, {"revision": 0}, format="json").status_code, 403
                )
                self.assertNotContains(self.browser.get(reverse("account_home")), self.path)
        self.assertFalse(EmployeeProfile.objects.exists())

    def test_dual_role_can_use_own_draft(self):
        UserRole.objects.create(user=self.user, role="employer")
        self.assertEqual(self.post({"revision": 0}).status_code, 302)
        self.assertEqual(self.api.get(API).json()["revision"], 1)

    def test_other_user_id_never_selects_another_draft(self):
        other = account("other@profiles.example.test")
        EmployeeProfile.objects.create(user=other, career_goal="Other account private goal")
        own = EmployeeProfile.objects.create(user=self.user, career_goal="My private goal")
        response = self.api.get(API, {"user_id": other.pk, "id": other.employee_profile.pk})
        self.assertEqual(response.json()["career_goal"], own.career_goal)
        self.assertNotIn("user", response.json())
        self.assertNotContains(self.browser.get(self.path), "Other account private goal")
        self.assertEqual(self.api.get(API + str(other.pk) + "/").status_code, 404)

    def test_api_rejects_ownership_publication_and_read_only_fields(self):
        for field in (
            "user",
            "user_id",
            "id",
            "status",
            "visibility",
            "updated_at",
            "schema_version",
        ):
            with self.subTest(field=field):
                response = self.api.patch(API, {"revision": 0, field: "injected"}, format="json")
                self.assertEqual(response.status_code, 400)
        self.assertFalse(EmployeeProfile.objects.exists())

    def test_web_cannot_reassign_or_publish_draft(self):
        other = account("target@profiles.example.test")
        response = self.post(
            {
                "revision": 0,
                "display_name": "My own draft",
                "user_id": other.pk,
                "status": "published",
                "visibility": "public",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(EmployeeProfile.objects.get().user, self.user)
        self.assertEqual(self.api.get(API).json()["visibility"], "private")

    def test_invalid_fields_and_revision_are_rejected_without_changing_data(self):
        self.api.patch(API, {"revision": 0, "display_name": "Ola"}, format="json")
        invalid = [
            {},
            {"revision": -1},
            {"revision": "invalid"},
            {"revision": 1, "display_name": "x" * 81},
            {"revision": 1, "location": "x" * 121},
            {"revision": 1, "desired_role": "x" * 121},
            {"revision": 1, "career_goal": "x" * 1001},
            {"revision": 1, "career_goal": None},
            {"revision": 1, "display_name": 123},
            {"revision": 1, "location": []},
        ]
        for data in invalid:
            with self.subTest(data_type=list(data)):
                self.assertEqual(self.api.patch(API, data, format="json").status_code, 400)
        draft = EmployeeProfile.objects.get()
        self.assertEqual((draft.display_name, draft.revision), ("Ola", 1))
        response = self.post({"revision": 1, "display_name": "x" * 81})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'aria-invalid="true"', status_code=400)

    def test_stale_first_and_later_api_saves_return_conflict(self):
        first = self.api.patch(API, {"revision": 0, "career_goal": "Version 1"}, format="json")
        self.assertEqual(first.status_code, 200)
        for revision in (0, 7):
            response = self.api.patch(API, {"revision": revision}, format="json")
            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["current_revision"], 1)
        self.api.patch(API, {"revision": 1, "career_goal": "Version 2"}, format="json")
        stale = self.api.patch(API, {"revision": 1, "career_goal": "Stale"}, format="json")
        self.assertEqual(stale.status_code, 409)
        self.assertEqual(stale.json()["code"], "draft_conflict")
        self.assertEqual(EmployeeProfile.objects.get().career_goal, "Version 2")

    def test_web_conflict_preserves_submitted_values_without_overwriting(self):
        self.post({"revision": 0, "career_goal": "Saved elsewhere"})
        stale = self.post({"revision": 0, "career_goal": "My unsaved changes"})
        self.assertEqual(stale.status_code, 409)
        self.assertEqual(stale.context["form"]["career_goal"].value(), "My unsaved changes")
        self.assertContains(stale, "Wczytaj zapisaną wersję", status_code=409)
        self.assertEqual(EmployeeProfile.objects.get().career_goal, "Saved elsewhere")

    def test_html_escapes_saved_text_and_requires_csrf(self):
        response = self.browser.post(self.path, {"revision": 0, "display_name": "Ola"})
        self.assertEqual(response.status_code, 403)
        text = '<script>alert("x")</script>'
        self.assertEqual(self.post({"revision": 0, "career_goal": text}).status_code, 302)
        page = self.browser.get(self.path)
        self.assertNotContains(page, text)
        self.assertContains(page, "&lt;script&gt;")
        self.assertEqual(EmployeeProfile.objects.get().career_goal, text)

    def test_cookie_api_requires_csrf_and_json(self):
        self.browser.get(self.path)
        payload = {"revision": 0, "location": "Sopot"}
        rejected = self.browser.patch(API, payload, content_type="application/json")
        self.assertEqual(rejected.status_code, 403)
        saved = self.browser.patch(
            API,
            payload,
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.browser.cookies["csrftoken"].value,
        )
        self.assertEqual(saved.status_code, 200)
        unsupported = self.browser.patch(
            API,
            "revision=1",
            content_type="application/x-www-form-urlencoded",
            HTTP_X_CSRFTOKEN=self.browser.cookies["csrftoken"].value,
        )
        self.assertEqual(unsupported.status_code, 415)

    def test_mobile_token_resumes_web_draft_and_revocation_blocks_access(self):
        self.post({"revision": 0, "location": "Gdynia"})
        native = Client()
        result = native.post(
            "/api/auth/app/v1/auth/login",
            {"email": self.user.email, "password": PASSWORD},
            content_type="application/json",
        )
        token = result.json()["meta"]["session_token"]
        headers = {"HTTP_X_SESSION_TOKEN": token}
        self.assertEqual(native.get(API, **headers).json()["location"], "Gdynia")
        saved = native.patch(
            API,
            {"revision": 1, "career_goal": "Zmiana zawodu"},
            content_type="application/json",
            **headers,
        )
        self.assertEqual(saved.status_code, 200)
        self.assertEqual(
            self.browser.get(self.path).context["form"]["career_goal"].value(), "Zmiana zawodu"
        )
        self.user.set_password("Nowe-haslo-test-743!")
        self.user.save()
        self.assertEqual(native.get(API, **headers).status_code, 403)
        self.assertEqual(
            native.patch(
                API, {"revision": 2}, content_type="application/json", **headers
            ).status_code,
            403,
        )

    def test_role_removal_and_inactive_account_block_existing_draft(self):
        EmployeeProfile.objects.create(user=self.user, display_name="Ola")
        self.user.roles.all().delete()
        self.assertEqual(self.api.get(API).status_code, 403)
        self.assertEqual(self.browser.get(self.path).status_code, 403)
        UserRole.objects.create(user=self.user, role="employee")
        self.user.is_active = False
        self.user.save()
        self.assertEqual(self.api.patch(API, {"revision": 1}, format="json").status_code, 403)

    def test_private_headers_apply_to_profile_pages_and_api_errors(self):
        for response in (
            self.browser.get(self.path),
            self.api.get(API),
            APIClient().get(API),
            self.api.patch(API, {}, format="json"),
        ):
            self.assertIn("no-store", response["Cache-Control"])
            self.assertEqual(response["Referrer-Policy"], "no-referrer")

    def test_public_collection_and_write_methods_are_not_exposed(self):
        self.assertEqual(self.api.get("/api/v1/profiles/").status_code, 404)
        for method in (self.api.post, self.api.put, self.api.delete):
            self.assertEqual(method(API, {}, format="json").status_code, 405)


class ConcurrentDraftTests(TransactionTestCase):
    def test_two_devices_cannot_overwrite_the_same_revision(self):
        if connection.vendor != "postgresql":
            self.skipTest("Real concurrent writes are checked in the PostgreSQL CI job.")
        user = account()
        for revision in (0, 1):
            with self.subTest(revision=revision):
                gate = Barrier(2)

                def write(name, gate=gate, revision=revision):
                    close_old_connections()
                    try:
                        gate.wait(timeout=5)
                        save_draft(user, revision=revision, data={"display_name": name})
                        return "saved"
                    except DraftConflict:
                        return "conflict"
                    finally:
                        close_old_connections()

                with ThreadPoolExecutor(max_workers=2) as pool:
                    outcomes = list(pool.map(write, ("Device A", "Device B")))
                self.assertCountEqual(outcomes, ["saved", "conflict"])
                self.assertEqual(EmployeeProfile.objects.get(user=user).revision, revision + 1)
