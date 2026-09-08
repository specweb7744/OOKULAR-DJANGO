"""Production settings template; deployment requires the gates in docs/04-etapy.md."""

from django.core.exceptions import ImproperlyConfigured

from .base import *

if not SECRET_KEY or len(SECRET_KEY) < 50 or SECRET_KEY.startswith(("CHANGE_", "ookular-tests")):
    raise ImproperlyConfigured("Wymagany unikalny DJANGO_SECRET_KEY o długości min. 50 znaków.")
if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("Podaj konkretne DJANGO_ALLOWED_HOSTS.")
if DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql":
    raise ImproperlyConfigured("W środowisku produkcyjnym OOKULAR wymaga PostgreSQL.")
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
# Configure SECURE_PROXY_SSL_HEADER only after a trusted proxy is configured
# to remove client-supplied forwarded headers. Do not trust them by default.
