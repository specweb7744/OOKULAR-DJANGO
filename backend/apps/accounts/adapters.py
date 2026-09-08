from allauth.account.adapter import DefaultAccountAdapter
from allauth.headless.adapter import DefaultHeadlessAdapter
from django.conf import settings
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return settings.OOKULAR_PUBLIC_ORIGIN + reverse(
            "account_confirm_email", args=[emailconfirmation.key]
        )

    def get_reset_password_from_key_url(self, key):
        uid, token = key.split("-", 1)
        return settings.OOKULAR_PUBLIC_ORIGIN + reverse(
            "account_reset_password_from_key", kwargs={"uidb36": uid, "key": token}
        )


class HeadlessAdapter(DefaultHeadlessAdapter):
    def serialize_user(self, user):
        # Exposed during partially authenticated flows too; keep this minimal.
        return {"id": str(user.pk) if user.pk else None}
