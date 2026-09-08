"""Exercise the actual TypeScript client over HTTP, without fetch mocks."""

import shutil
import subprocess
from unittest import skipUnless

from allauth.account.models import EmailAddress
from django.conf import settings
from django.core.cache import cache
from django.test import LiveServerTestCase

from .models import User, UserRole


@skipUnless(shutil.which("node"), "Node 24 is required for the TypeScript client check.")
class MobileClientHttpTests(LiveServerTestCase):
    def test_typescript_client_against_django(self):
        cache.clear()
        for role in UserRole.Role.values:
            user = User.objects.create_user(
                f"{role}@client.example.test", "Rzeka-zielona-784!Bezpieczna"
            )
            UserRole.objects.create(user=user, role=role)
            EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
        result = subprocess.run(
            [
                shutil.which("node"),
                "--experimental-transform-types",
                "scripts/check_mobile_client.mts",
                self.live_server_url,
            ],
            cwd=settings.ROOT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
