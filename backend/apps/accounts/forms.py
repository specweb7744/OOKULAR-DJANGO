from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.core import context
from django import forms
from django.db import IntegrityError, transaction

from .models import User


class AtomicSignupMixin:
    def try_save(self, request):
        try:
            with transaction.atomic():
                return super().try_save(request)
        except IntegrityError:
            # A simultaneous signup can win after form validation. Keep the
            # response generic and never attach a new role to that account.
            if not User.objects.filter(email__iexact=self.cleaned_data["email"]).exists():
                raise
            self.account_already_exists = True
            return super().try_save(request)


class SignupForm(AtomicSignupMixin, AllauthSignupForm):
    field_order = ["role", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound and context.request:
            role = context.request.GET.get("role")
            if role in {"employee", "employer"}:
                self.initial["role"] = role
        self.fields["email"].label = "Adres e-mail"
        self.fields["password1"].label = "Hasło"
        self.fields["password2"].label = "Powtórz hasło"


class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        label="Adres e-mail",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
