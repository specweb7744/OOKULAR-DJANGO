from unittest.mock import patch

from allauth.account.models import EmailAddress
from django.db import DatabaseError
from django.test import Client, TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User, UserRole


class ApiBoundaryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_diagnostics_and_api_root_are_read_only(self):
        for url in ("/health/", "/ready/", "/api/v1/"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
                self.assertEqual(self.client.post(url).status_code, 405)

    def test_readiness_failure_hides_database_details(self):
        with patch(
            "apps.core.views.connection.cursor",
            side_effect=DatabaseError("private-database-password"),
        ):
            response = self.client.get("/ready/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})

    def test_anonymous_user_cannot_read_account_or_internal_catalog(self):
        for url in ("/api/v1/me/", "/api/v1/modules/"):
            self.assertEqual(self.client.get(url).status_code, 403)

    def test_me_ignores_other_account_id_and_omits_staff_fields(self):
        own = User.objects.create_user("own@example.test")
        EmailAddress.objects.create(user=own, email=own.email, verified=True, primary=True)
        other = User.objects.create_user("other@example.test")
        UserRole.objects.create(user=own, role="employee")
        self.client.force_authenticate(user=own)
        response = self.client.get("/api/v1/me/", {"id": str(other.pk)})
        self.assertEqual(
            response.json(), {"id": str(own.pk), "email": own.email, "roles": ["employee"]}
        )

    def test_employer_role_does_not_expose_internal_catalog(self):
        account = User.objects.create_user("employer@example.test")
        UserRole.objects.create(user=account, role="employer")
        self.client.force_authenticate(user=account)
        self.assertEqual(self.client.get("/api/v1/modules/").status_code, 403)

    def test_staff_can_read_module_status_without_business_endpoints(self):
        staff = User.objects.create_user("staff@example.test", is_staff=True)
        EmailAddress.objects.create(user=staff, email=staff.email, verified=True, primary=True)
        self.client.force_authenticate(user=staff)
        response = self.client.get("/api/v1/modules/")
        self.assertEqual(response.status_code, 200)
        modules = {m["id"]: m for m in response.json()["modules"]}
        self.assertEqual(modules["matching"]["status"], "planned")
        self.assertEqual(modules["profiles"]["status"], "partial")
        self.assertEqual(self.client.get("/api/v1/search/").status_code, 404)
        self.assertEqual(self.client.get("/api/v1/matches/").status_code, 404)

    def test_admin_login_rejects_post_without_csrf(self):
        browser = Client(enforce_csrf_checks=True)
        response = browser.post(
            "/admin/login/", {"username": "admin@example.test", "password": "irrelevant"}
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_add_page_renders_with_custom_user(self):
        admin = User.objects.create_superuser(
            "admin@example.test", "safe-test-only-passphrase-743!"
        )
        self.client.force_login(admin)
        response = self.client.get("/admin/accounts/user/add/")
        self.assertEqual(response.status_code, 200)
