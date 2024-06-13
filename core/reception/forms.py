from django import forms 
from .models import Reception
from django.core.exceptions import ValidationError
import re

class ReceptionCreateForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = [
            "reason",
            "payment_type",
            "payment_status",
            "client",
            "service",
            "invoice_attachment",
        ]

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", reason):
            raise ValidationError(" علت مراجعه باید فقط شامل حروف و اعداد باشد.")
        return reason
    
class ReceptionWithClientIDCreateForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = [
            "reason",
            "payment_type",
            "payment_status",
            "service",
            "invoice_attachment",
        ]

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", reason):
            raise ValidationError(" علت مراجعه باید فقط شامل حروف و اعداد باشد.")
        return reason



class ReceptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = [
            "client",
            "service",
            "reason",
            "payment_type",
            "payment_status",
        ]

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", reason):
            raise ValidationError(" علت مراجعه باید فقط شامل حروف و اعداد باشد.")
        return reason