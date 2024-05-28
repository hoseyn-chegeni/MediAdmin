from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


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
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number