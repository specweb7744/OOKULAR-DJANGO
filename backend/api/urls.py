from apps.accounts.views import me
from apps.core.views import api_root, module_catalog
from django.urls import path

app_name = "api"
urlpatterns = [
    path("", api_root, name="root"),
    path("me/", me, name="me"),
    path("modules/", module_catalog, name="modules"),
]
