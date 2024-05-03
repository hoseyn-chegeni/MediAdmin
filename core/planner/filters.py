import django_filters
from .models import Session
from django.db import models

from base.filters import BaseFilter



class SessionFilters(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")

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
