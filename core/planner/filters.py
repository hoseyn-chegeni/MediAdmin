import django_filters
from .models import Session
from django.db import models
from base.filters import BaseFilter


class SessionFilters(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")
    day_date = django_filters.CharFilter(field_name='day__mock_date', method="filter_by_day_date")
    client_id = django_filters.NumberFilter(field_name='client__id')
    doctor = django_filters.CharFilter(method="filter_by_doctor")
    has_client = django_filters.BooleanFilter(method="filter_by_has_client")


    class Meta:
        model = Session
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "national_id": ["exact"],
            "status": ["exact"],


        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
    
    def filter_by_day_date(self, queryset, name, value):
        return queryset.filter(day__mock_date=value)
    
    def filter_by_has_client(self, queryset, name, value):
        if value:
            return queryset.exclude(client__isnull=True)
        else:
            return queryset.filter(client__isnull=True)
        
    def filter_by_doctor(self, queryset, name, value):
        return queryset.filter(
            models.Q(service__doctor__first_name__icontains=value) |
            models.Q(service__doctor__last_name__icontains=value)
        )
