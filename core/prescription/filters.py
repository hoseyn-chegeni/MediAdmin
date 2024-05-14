import django_filters
from django_filters import FilterSet, DateFilter
from .models import Prescription
from django.db import models
from base.filters import BaseFilter
from django import forms


class PrescriptionFilter(BaseFilter):

    date = DateFilter(
        field_name="date",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date_field",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_by_date_field(self, queryset, name, value):
        return queryset.filter(date=value)

    class Meta:
        model = Prescription
        fields = {
            "id": ["exact"],
            "reception": ["exact"],
            "medication": ["exact", "icontains"],
        }
