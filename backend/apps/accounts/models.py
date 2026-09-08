from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower

from .managers import UserManager


class User(AbstractUser):
    """Authentication identity only. The professional portrait belongs to profiles."""

    username = None
    email = models.EmailField("adres e-mail", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = "konto"
        verbose_name_plural = "konta"
        constraints = [
            models.UniqueConstraint(Lower("email"), name="account_email_case_insensitive_unique"),
            models.CheckConstraint(condition=~models.Q(email=""), name="account_email_not_empty"),
        ]

    def clean(self):
        super().clean()
        self.email = UserManager.normalize_email(self.email)

    def save(self, *args, **kwargs):
        self.email = UserManager.normalize_email(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class UserRole(models.Model):
    """One account can act as employee and employer. Roles never grant staff access."""

    class Role(models.TextChoices):
        EMPLOYEE = "employee", "Pracownik"
        EMPLOYER = "employer", "Pracodawca"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roles"
    )
    role = models.CharField(max_length=16, choices=Role.choices)

    class Meta:
        verbose_name = "rola konta"
        verbose_name_plural = "role konta"
        constraints = [
            models.UniqueConstraint(fields=["user", "role"], name="unique_role_per_account"),
            models.CheckConstraint(
                condition=models.Q(role__in=["employee", "employer"]), name="account_role_allowed"
            ),
        ]

    def __str__(self):
        return self.get_role_display()
