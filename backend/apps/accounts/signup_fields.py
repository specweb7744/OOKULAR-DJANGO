"""Fields shared by the HTML form and the mobile JSON signup input."""

from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import User, UserRole


class SignupFields(forms.Form):
    role = forms.ChoiceField(
        label="Zakładam konto jako",
        choices=UserRole.Role.choices,
        widget=forms.RadioSelect,
        initial=UserRole.Role.EMPLOYEE,
    )

    def clean(self):
        data = super().clean()
        # Headless's built-in password check has no user yet. Enforce similarity
        # against the supplied email just as in the HTML signup form.
        password = data.get("password")
        if password and data.get("email"):
            validate_password(password, user=User(email=data["email"]))
        return data

    def signup(self, request, user):
        # Called within AtomicSignupMixin's transaction for both clients.
        UserRole.objects.create(user=user, role=self.cleaned_data["role"])
