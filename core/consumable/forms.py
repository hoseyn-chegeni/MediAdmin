from django.core.exceptions import ValidationError
import re
from .models import ConsumableV2, ConsumableCategory, Supplier
from django import forms


class ConsumableCreationForm(forms.ModelForm):
    class Meta:
        model = ConsumableV2
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")

        name = self.cleaned_data.get("name")
        if ConsumableV2.objects.filter(name=name).exists():
            raise ValidationError("یک  محصول با این نام قبلاً ایجاد شده است.")
        return name


class ConsumableUpdateForm(forms.ModelForm):
    class Meta:
        model = ConsumableV2
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return name


class ConsumableCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ConsumableCategory
        fields = ["name", "note"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")

        name = self.cleaned_data.get("name")
        if ConsumableV2.objects.filter(name=name).exists():
            raise ValidationError("یک  دسته بندی با این نام قبلاً ایجاد شده است.")
        return name


class ConsumableCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = ConsumableCategory
        fields = ["name", "note"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return name


class SupplierCreateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "contact_person",
            "email",
            "phone_number",
            "address",
            "city",
            "notes",
        ]
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")

        name = self.cleaned_data.get("name")
        if ConsumableV2.objects.filter(name=name).exists():
            raise ValidationError("یک   تامین کننده با  با این نام در سیستم وجود دارد.")
        return name

    def clean_contact_person(self):
        contact_person = self.cleaned_data.get("contact_person")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", contact_person):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return contact_person

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number


class SupplierUpdateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "contact_person",
            "email",
            "phone_number",
            "address",
            "city",
            "notes",
        ]
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", name):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return name

    def clean_contact_person(self):
        contact_person = self.cleaned_data.get("contact_person")
        if not re.match(r"^[A-Za-z0-9ا-ی\s]+$", contact_person):
            raise ValidationError("نام باید فقط شامل حروف و اعداد باشد.")
        return contact_person

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise ValidationError("لطفا شماره تماس صحیح وارد نمایید")
        if len(phone_number) != 11:
            raise ValidationError("تعداد ارقام شماره همراه صحیح نمی باشد")
        return phone_number
