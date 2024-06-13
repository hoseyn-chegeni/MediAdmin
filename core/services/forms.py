from django import forms
from .models import Service
from django.core.exceptions import ValidationError
import re

class ServiceSelectionForm(forms.Form):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all())
    percentage_change = forms.DecimalField(label="Percentage Change (%)")


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Service.objects.filter(name=name).exists():
            raise ValidationError("یک  سرویس با این نام قبلاً ایجاد شده است.")

        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام سرویس باید فقط شامل حروف و اعداد باشد.")
        return name  
    

class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "name",
            "doctor",
            "description",
            "category",
            "duration",
            "price",
            "is_active",
            "preparation_instructions",
            "documentation_requirements",
            "therapeutic_measures",
            "recommendations",
            "medical_equipment",
            "doctors_wage_percentage",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام سرویس باید فقط شامل حروف و اعداد باشد.")
        return name  