from django.conf import settings
from django.db import models

EDITABLE_FIELDS = ("display_name", "location", "desired_role", "career_goal")


class EmployeeProfile(models.Model):
    """Private first-step draft. No public projection or employer access exists yet."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee_profile"
    )
    display_name = models.CharField("Imię lub pseudonim", max_length=80, blank=True, default="")
    location = models.CharField("Miejscowość", max_length=120, blank=True, default="")
    desired_role = models.CharField("Jakiej pracy szukasz?", max_length=120, blank=True, default="")
    career_goal = models.TextField("Twój cel zawodowy", max_length=1000, blank=True, default="")
    revision = models.PositiveIntegerField(default=1, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "prywatny szkic profilu pracownika"
        verbose_name_plural = "prywatne szkice profili pracowników"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(revision__gte=1), name="profile_revision_positive"
            )
        ]

    def __str__(self):
        return f"Szkic profilu {self.pk}"
