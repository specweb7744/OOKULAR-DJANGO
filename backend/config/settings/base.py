"""Shared settings. All feature APIs require authentication unless explicitly public."""

from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = ROOT_DIR / "backend"
env = environ.Env()
environ.Env.read_env(ROOT_DIR / ".env", overwrite=False)

SECRET_KEY = env("DJANGO_SECRET_KEY", default="")
DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.headless",
    "apps.core",
    "apps.accounts",
    "apps.taxonomy",
    "apps.profiles",
    "apps.organizations",
    "apps.jobs",
    "apps.feed",
    "apps.content",
    "apps.education",
    "apps.search",
    "apps.matching",
    "apps.social",
    "apps.messaging",
    "apps.notifications",
    "apps.billing",
    "apps.moderation",
    "apps.privacy",
    "apps.integrations",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.accounts.middleware.PrivateAccountPagesMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BACKEND_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {"default": env.db("DATABASE_URL", default=f"sqlite:///{ROOT_DIR / 'db.sqlite3'}")}
if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
    db_name = Path(DATABASES["default"]["NAME"])
    if not db_name.is_absolute():
        DATABASES["default"]["NAME"] = ROOT_DIR / db_name

AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "account_home"
LOGOUT_REDIRECT_URL = "account_login"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_SIGNUP_FORM_CLASS = "apps.accounts.signup_fields.SignupFields"
ACCOUNT_FORMS = {"signup": "apps.accounts.forms.SignupForm"}
ACCOUNT_ADAPTER = "apps.accounts.adapters.AccountAdapter"
ACCOUNT_EMAIL_MAX_LENGTH = 254
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_PREVENT_ENUMERATION = True
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[OOKULAR] "
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "account_home"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "account_login"
ACCOUNT_RATE_LIMITS = {
    "signup": "5/m/ip",
    "login": "20/m/ip",
    "login_failed": "10/m/ip,5/5m/key",
    "reset_password": "5/m/ip,3/10m/key",
    "resend_verification": "5/m/ip,3/10m/key",
    "confirm_email": "1/60s/key",
}
# Shared by every worker, including after a process restart. Created by migration.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "ookular_auth_cache",
        "OPTIONS": {"MAX_ENTRIES": 10000},
    }
}
# Never trust client-provided forwarding headers without a configured edge proxy.
ALLAUTH_TRUSTED_PROXY_COUNT = env.int("ALLAUTH_TRUSTED_PROXY_COUNT", default=0)
HEADLESS_CLIENTS = ("app",)
HEADLESS_ADAPTER = "apps.accounts.adapters.HeadlessAdapter"
HEADLESS_FRONTEND_URLS = {}  # Mail links open our Django views on web and phone.
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
PASSWORD_RESET_TIMEOUT = 60 * 60
OOKULAR_PUBLIC_ORIGIN = env("OOKULAR_PUBLIC_ORIGIN", default="http://127.0.0.1:8000").rstrip("/")
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "apps.accounts.authentication.MobileSessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["apps.accounts.permissions.HasVerifiedAccount"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
LANGUAGE_CODE = "pl"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "static/"
STATIC_ROOT = ROOT_DIR / "staticfiles"
STATICFILES_DIRS = [BACKEND_DIR / "static"]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="OOKULAR <noreply@localhost>")
CSRF_FAILURE_VIEW = "apps.accounts.views.csrf_failure"
