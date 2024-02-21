import django_filters
from django_filters import FilterSet
from .models import Client
from django.db import models


class ClientFilters(FilterSet):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Client
        fields = {
            "id": ["exact"],
            "case_id": ["exact"],
            "national_id": ["exact"],
            "is_vip": ["exact"],

        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
