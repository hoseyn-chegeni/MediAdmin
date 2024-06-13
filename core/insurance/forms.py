from django import forms 
from .models import Insurance
from django.core.exceptions import ValidationError  
import re
class InsuranceCreateForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Insurance.objects.filter(name=name).exists():
            raise ValidationError("یک  بیمه با این نام قبلاً ایجاد شده است.")

        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return name
       
    def clean_policy_number(self):
        policy_number = self.cleaned_data.get("policy_number")
        if not policy_number.isdigit():
            raise ValidationError("شماره بیمه باید فقط شامل اعداد باشد")
        return policy_number
    
    def clean_insurance_company(self):
        insurance_company = self.cleaned_data.get("insurance_company")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", insurance_company):
            raise ValidationError("نام شرکت ارایه دهنده باید فقط شامل حروف و اعداد باشد.")
        return insurance_company

    def clean_policy_type(self):
        policy_type = self.cleaned_data.get("policy_type")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", policy_type):
            raise ValidationError("این فیلد باید فقط شامل حروف و اعداد باشد.")
        return policy_type

class InsuranceUpdateForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return name
       
    def clean_policy_number(self):
        policy_number = self.cleaned_data.get("policy_number")
        if not policy_number.isdigit():
            raise ValidationError("شماره بیمه باید فقط شامل اعداد باشد")
        return policy_number
    
    def clean_insurance_company(self):
        insurance_company = self.cleaned_data.get("insurance_company")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", insurance_company):
            raise ValidationError("نام شرکت ارایه دهنده باید فقط شامل حروف و اعداد باشد.")
        return insurance_company

    def clean_policy_type(self):
        policy_type = self.cleaned_data.get("policy_type")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", policy_type):
            raise ValidationError("این فیلد باید فقط شامل حروف و اعداد باشد.")
        return policy_type