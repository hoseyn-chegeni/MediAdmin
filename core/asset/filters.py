from django_filters import FilterSet, DateFilter
from .models import Equipment
from base.filters import BaseFilter
from django import forms


class EquipmentFilter(BaseFilter):

    acquisition_date = DateFilter(
        field_name="acquisition_date",
        label="acquisition_date (yyyy-mm-dd)",
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
