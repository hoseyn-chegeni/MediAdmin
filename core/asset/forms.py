from django import forms
from .models import Equipment
from django.core.exceptions import ValidationError  # Add this import
import re

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        exclude = ['serial_number', 'acquisition_date', 'warranty_expiry_date', 'last_maintenance_date']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return name
