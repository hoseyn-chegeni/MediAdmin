from django import forms
from .models import Equipment
from django.core.exceptions import ValidationError  # Add this import
import re


class EquipmentCreateForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Equipment.objects.filter(name=name).exists():
            raise ValidationError("یک  دستگاه با این نام قبلاً ایجاد شده است.")

        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")

        return name


class EquipmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")

        return name
