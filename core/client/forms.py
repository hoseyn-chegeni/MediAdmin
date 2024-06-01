from django import forms
from django.core.exceptions import ValidationError
from .models import Client
import re

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def clean_case_id(self):
        case_id = self.cleaned_data.get('case_id')
        if case_id and not case_id.isdigit():
            raise ValidationError('شناسه پرونده باید یک عدد مثبت باشد.')
        return case_id

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if re.search(r'[^a-zA-Z\s]', first_name):
            raise ValidationError('نام نباید شامل کاراکترهای خاص یا اعداد باشد.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if re.search(r'[^a-zA-Z\s]', last_name):
            raise ValidationError('نام خانوادگی نباید شامل کاراکترهای خاص یا اعداد باشد.')
        return last_name

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if not national_id.isdigit():
            raise ValidationError('کد ملی باید عدد باشد.')
        return national_id

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise ValidationError('شماره تلفن باید یک عدد 11 رقمی باشد.')
        return phone_number

    def clean_emergency_contact_name(self):
        emergency_contact_name = self.cleaned_data.get('emergency_contact_name')
        if re.search(r'[^a-zA-Z\s]', emergency_contact_name):
            raise ValidationError('نام شخص تماس اضطراری نباید شامل کاراکترهای خاص یا اعداد باشد.')
        return emergency_contact_name

    def clean_emergency_contact_number(self):
        emergency_contact_number = self.cleaned_data.get('emergency_contact_number')
        if not emergency_contact_number.isdigit():
            raise ValidationError('شماره تماس اضطراری باید عدد باشد.')
        return emergency_contact_number

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional cross-field validation here if necessary
        return cleaned_data