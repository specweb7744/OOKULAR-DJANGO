from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils import timezone

from .models import EDITABLE_FIELDS, EmployeeProfile

CONFLICT_MESSAGE = (
    "Ten profil został zapisany w innej karcie lub na innym urządzeniu. "
    "Twoje zmiany w formularzu zostały zachowane, ale nie nadpisały nowszego szkicu. "
    "Skopiuj je przed wczytaniem zapisanej wersji."
)


class DraftConflict(Exception):
    pass


def get_draft(user):
    return EmployeeProfile.objects.filter(user=user).first()


def draft_data(profile):
    return {
        **{field: getattr(profile, field, "") for field in EDITABLE_FIELDS},
        "revision": profile.revision if profile else 0,
        "updated_at": profile.updated_at.isoformat() if profile else None,
        "status": "draft",
        "visibility": "private",
        "schema_version": 1,
    }


def save_draft(user, *, revision, data):
    """Accept validated fields and compare revisions in SQL to prevent lost updates."""
    if set(data) - set(EDITABLE_FIELDS):
        raise ValueError("Unsupported profile fields")
    try:
        with transaction.atomic():
            if revision == 0:
                return EmployeeProfile.objects.create(user=user, **data)
            updated = EmployeeProfile.objects.filter(user=user, revision=revision).update(
                **data, revision=F("revision") + 1, updated_at=timezone.now()
            )
            if not updated:
                raise DraftConflict
            return EmployeeProfile.objects.get(user=user)
    except IntegrityError as exc:
        # A second initial save must not replace the first device's draft.
        if revision == 0 and EmployeeProfile.objects.filter(user=user).exists():
            raise DraftConflict from exc
        raise
