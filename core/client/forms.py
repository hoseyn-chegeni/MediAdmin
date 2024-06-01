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




class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "case_id",
            "first_name",
            "last_name",
            "fathers_name",
            "national_id",
            "date_of_birth",
            "gender",
            "phone_number",
            "address",
            "marital_status",
            "emergency_contact_name",
            "emergency_contact_number",
            "insurance",
        ]

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




def validate_no_special_characters(value):
    if re.search(r'[^a-zA-Z0-9\s]', value):
        raise ValidationError('این فیلد نمی‌تواند شامل کاراکترهای خاص باشد.')
    return value

class EditHealthHistoryForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "surgeries",
            "allergies",
            "medical_history",
            "medications",
            "smoker",
            "disease",
            "high_risk",
        ]

    def clean_surgeries(self):
        return validate_no_special_characters(self.cleaned_data.get('surgeries', ''))

    def clean_allergies(self):
        return validate_no_special_characters(self.cleaned_data.get('allergies', ''))

    def clean_medical_history(self):
        return validate_no_special_characters(self.cleaned_data.get('medical_history', ''))

    def clean_medications(self):
        return validate_no_special_characters(self.cleaned_data.get('medications', ''))

    def clean_smoker(self):
        return validate_no_special_characters(self.cleaned_data.get('smoker', ''))

    def clean_disease(self):
        return validate_no_special_characters(self.cleaned_data.get('disease', ''))

