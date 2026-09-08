from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from .models import User, UserRole


class AccountCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = User
        fields = ("email",)


class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"


class RoleInline(admin.TabularInline):
    model = UserRole
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    ordering = ("email",)
    list_display = ("email", "is_active", "is_staff")
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Dane konta", {"fields": ("first_name", "last_name")}),
        (
            "Uprawnienia",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Daty", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    inlines = (RoleInline,)
