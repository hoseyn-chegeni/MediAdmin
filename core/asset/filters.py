from django_filters import FilterSet, DateFilter
from .models import Consumable, ConsumableCategory, Supplier, Equipment
from base.filters import BaseFilter
from django import forms


class ConsumableFilter(BaseFilter):

    class Meta:
        model = Consumable
        fields = {
            "id": ["exact"],
            "name": ["exact"],
            "category": ["exact"],
            "supplier": ["exact"],
        }


class ConsumableCategoryFilter(BaseFilter):

    class Meta:
        model = ConsumableCategory
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }


class SupplierFilter(BaseFilter):

    class Meta:
        model = Supplier
        fields = {
            "id": ["exact"],
            "name": ["exact"],
            "contact_person": ["exact"],
            "email": ["exact"],
            "phone_number": ["exact"],
            "city": ["exact", "icontains"],
        }


class EquipmentFilter(BaseFilter):

    acquisition_date = DateFilter(
        field_name="acquisition_date",
        label="Date (yyyy-mm-dd)",
        method="filter_by_acquisition_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_by_acquisition_date(self, queryset, name, value):
        return queryset.filter(acquisition_date=value)

    class Meta:
        model = Equipment
        fields = {
            "id": ["exact"],
            "name": ["exact"],
            "manufacturer": ["exact"],
            "serial_number": ["exact"],
            "location": ["exact"],
            "is_available": ["exact"],
        }
