from rest_framework.permissions import BasePermission

from apps.accounts.models import UserRole


def is_employee(user):
    return bool(user.is_authenticated and user.roles.filter(role=UserRole.Role.EMPLOYEE).exists())


class IsEmployee(BasePermission):
    message = "Profil zawodowy jest dostępny dla konta z rolą pracownika."

    def has_permission(self, request, view):
        return is_employee(request.user)
