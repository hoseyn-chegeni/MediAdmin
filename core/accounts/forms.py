from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "phone_number",
        )

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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number
