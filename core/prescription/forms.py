from django import forms
from .models import PrescriptionItem


class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = [
            "medicine",
            "quantity",
            "consumption_time",
            "consumption_dose",
            "how_to_use",
            "repeat_interval",
            "repeat_period",
        ]
