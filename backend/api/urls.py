from apps.accounts.views import me
from apps.core.views import api_root, module_catalog
from apps.profiles.views import my_employee_profile
from django.urls import path

app_name = "api"
urlpatterns = [
    path("", api_root, name="root"),
    path("me/", me, name="me"),
    path("me/employee-profile/", my_employee_profile, name="employee_profile"),
    path("modules/", module_catalog, name="modules"),
]
