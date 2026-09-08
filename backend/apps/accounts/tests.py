from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from django.test import TestCase

from .admin import AccountCreationForm
from .models import User, UserRole


class AccountTests(TestCase):
    def test_email_login_is_normalized_and_password_is_hashed(self):
        account = User.objects.create_user("  USER@Example.test ", "example-test-password-743!")
        self.assertEqual(account.email, "user@example.test")
        self.assertNotEqual(account.password, "example-test-password-743!")
        self.assertTrue(account.check_password("example-test-password-743!"))
        self.assertEqual(
            authenticate(email="USER@EXAMPLE.TEST", password="example-test-password-743!"),
            account,
        )

    def test_database_rejects_case_variant_even_when_save_is_bypassed(self):
        User.objects.create_user("user@example.test", "example-test-password-743!")
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.bulk_create([User(email="USER@example.test")])

    def test_missing_email_is_rejected(self):
        with self.assertRaises(ValueError):
            User.objects.create_user("", "example-test-password-743!")

    def test_two_roles_do_not_grant_staff_permissions(self):
        account = User.objects.create_user("two@example.test", "example-test-password-743!")
        for role in UserRole.Role.values:
            UserRole.objects.create(user=account, role=role)
        self.assertEqual(account.roles.count(), 2)
        account.refresh_from_db()
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)

    def test_duplicate_and_invalid_roles_are_rejected_by_database(self):
        account = User.objects.create_user("roles@example.test")
        UserRole.objects.create(user=account, role="employee")
        for role in ("employee", "admin"):
            with self.subTest(role=role), self.assertRaises(IntegrityError), transaction.atomic():
                UserRole.objects.create(user=account, role=role)

    def test_inactive_user_cannot_authenticate(self):
        User.objects.create_user(
            "inactive@example.test", "example-test-password-743!", is_active=False
        )
        self.assertIsNone(
            authenticate(email="inactive@example.test", password="example-test-password-743!")
        )

    def test_superuser_cannot_be_created_without_required_flags(self):
        for flag in ("is_staff", "is_superuser", "is_active"):
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                User.objects.create_superuser(
                    "admin@example.test", "example-test-password-743!", **{flag: False}
                )

    def test_admin_creation_form_uses_custom_email_user(self):
        form = AccountCreationForm(
            data={
                "email": "created@example.test",
                "password1": "safe-test-only-passphrase-743!",
                "password2": "safe-test-only-passphrase-743!",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        account = form.save()
        self.assertTrue(account.check_password("safe-test-only-passphrase-743!"))
        self.assertFalse(account.is_staff)
