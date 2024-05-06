import django_filters
from .models import Session
from django.db import models
from django_jalali.admin.filters import JDateFieldListFilter

from base.filters import BaseFilter


class SessionFilters(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")
    day_date = django_filters.CharFilter(field_name='day__mock_date', method="filter_by_day_date")

    class Meta:
        model = Session
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "client": ["exact"],
            "national_id": ["exact"],

        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
    
    def filter_by_day_date(self, queryset, name, value):
        return queryset.filter(day__mock_date=value)