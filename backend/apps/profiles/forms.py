from django import forms

from .models import EDITABLE_FIELDS, EmployeeProfile


class EmployeeProfileForm(forms.ModelForm):
    revision = forms.IntegerField(min_value=0, widget=forms.HiddenInput)

    class Meta:
        model = EmployeeProfile
        fields = EDITABLE_FIELDS
        widgets = {
            "display_name": forms.TextInput(attrs={"autocomplete": "nickname"}),
            "location": forms.TextInput(attrs={"autocomplete": "address-level2"}),
            "desired_role": forms.TextInput(attrs={"placeholder": "Np. operator produkcji"}),
            "career_goal": forms.Textarea(attrs={"rows": 5}),
        }
        help_texts = {
            "display_name": "Tak będziemy się do Ciebie zwracać. Do 80 znaków.",
            "location": "Wystarczy miejscowość, bez dokładnego adresu. Do 120 znaków.",
            "desired_role": "Możesz wpisać stanowisko lub obszar pracy. Do 120 znaków.",
            "career_goal": (
                "Opisz, co chcesz robić i w jakim kierunku się rozwijać. Do 1000 znaków."
            ),
        }
