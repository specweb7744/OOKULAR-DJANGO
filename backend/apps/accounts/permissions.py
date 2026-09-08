from allauth.account.models import EmailAddress
from rest_framework.permissions import BasePermission


def has_verified_email(user):
    return bool(
        user.is_authenticated
        and user.is_active
        and EmailAddress.objects.filter(user=user, email__iexact=user.email, verified=True).exists()
    )


class HasVerifiedAccount(BasePermission):
    message = "Potwierdź adres e-mail, aby korzystać z konta."

    def has_permission(self, request, view):
        return has_verified_email(request.user)
