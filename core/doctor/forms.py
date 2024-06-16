from django import forms
from django.core.exceptions import ValidationError
from .models import Doctor
import re

class DoctorCreateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "specialization",
            "registration_number",
            "is_active",
            "image",
            "user",
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r"^[A-Za-zا-ی\s]+$", first_name):
            raise ValidationError("نام باید فقط شامل حروف باشد.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r"^[A-Za-zا-ی\s]+$", last_name):
            raise ValidationError("نام خانوادگی فقط باید شامل حروف باشد.")
        return last_name
    
    def clean_registration_number(self):
        registration_number = self.cleaned_data.get("registration_number")
        if not registration_number.isdigit():
            raise ValidationError("شماره نظام پزشکی باید فقط شامل اعداد باشد")
        return registration_number

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model  = Doctor
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "specialization",
            "registration_number",
            "image",
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r"^[A-Za-zا-ی\s]+$", first_name):
            raise ValidationError("نام باید فقط شامل حروف باشد.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r"^[A-Za-zا-ی\s]+$", last_name):
            raise ValidationError("نام خانوادگی فقط باید شامل حروف باشد.")
        return last_name
    
    def clean_registration_number(self):
        registration_number = self.cleaned_data.get("registration_number")
        if not registration_number.isdigit():
            raise ValidationError("شماره نظام پزشکی باید فقط شامل اعداد باشد")
        return registration_number
