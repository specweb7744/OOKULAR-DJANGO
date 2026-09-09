from collections.abc import Mapping

from rest_framework import serializers

from .models import EDITABLE_FIELDS, EmployeeProfile


class EmployeeProfilePatchSerializer(serializers.ModelSerializer):
    revision = serializers.IntegerField(min_value=0, required=True)

    class Meta:
        model = EmployeeProfile
        fields = (*EDITABLE_FIELDS, "revision")

    def to_internal_value(self, data):
        if isinstance(data, Mapping):
            unknown = set(data) - set(self.fields)
            if unknown:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Przesłano nieobsługiwane pola profilu."]}
                )
            # JSON profile fields are text, not coerced numeric or boolean values.
            errors = {
                field: ["Podaj tekst."]
                for field in EDITABLE_FIELDS
                if field in data and not isinstance(data[field], str)
            }
            if errors:
                raise serializers.ValidationError(errors)
        return super().to_internal_value(data)
