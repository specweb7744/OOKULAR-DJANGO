from apps.core.views import health, readiness
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("health/", health, name="health"),
    path("ready/", readiness, name="readiness"),
    path("api/v1/", include("api.urls")),
    path("admin/", admin.site.urls),
]
admin.site.site_header = "OOKULAR · administracja"
admin.site.site_title = "OOKULAR"
admin.site.index_title = "Zarządzanie portalem"
