from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import ConsumableV2
from django import forms



class ConsumableForm(forms.ModelForm):
    class Meta:
        model = ConsumableV2
        fields ='__all__'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")

        name = self.cleaned_data.get("name")
        if ConsumableV2.objects.filter(name=name).exists():
            raise ValidationError("یک  محصول با این نام قبلاً ایجاد شده است.")

        return name
