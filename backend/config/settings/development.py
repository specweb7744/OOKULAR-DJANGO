"""Local developer setup. Never select this module on a public server."""

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
if not SECRET_KEY or SECRET_KEY == "CHANGE_ME":
    raise ImproperlyConfigured("Uruchom: python scripts/init_local.py")
