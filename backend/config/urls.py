from allauth.account.decorators import secure_admin_login
from allauth.headless.constants import Client
from apps.accounts import views as account_views
from apps.accounts.headless import MobileResendView, MobileSignupView
from apps.core.views import health, readiness
from django.contrib import admin
from django.urls import include, path

admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
    path("", account_views.entrance, name="home"),
    path("konto/", account_views.account_home, name="account_home"),
    path(
        "konta/potwierdz-ponownie/", account_views.resend_verification, name="resend_verification"
    ),
    path("konta/", include("allauth.urls")),
    path("api/auth/app/v1/auth/signup", MobileSignupView.as_api_view(client=Client.APP)),
    path(
        "api/auth/app/v1/auth/email/verify/resend",
        MobileResendView.as_api_view(client=Client.APP),
    ),
    path("api/auth/", include("allauth.headless.urls")),
    path("health/", health, name="health"),
    path("ready/", readiness, name="readiness"),
    path("api/v1/", include("api.urls")),
    path("admin/", admin.site.urls),
]
admin.site.site_header = "OOKULAR · administracja"
admin.site.site_title = "OOKULAR"
admin.site.index_title = "Zarządzanie portalem"
