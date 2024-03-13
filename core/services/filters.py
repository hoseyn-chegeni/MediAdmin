import django_filters
from django_filters import FilterSet
from .models import Service
from django.db import models


class ServicesFilter(FilterSet):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Service
        fields = {
            "id": ["exact"],
            "doctor":['exact'],
            "category":['exact'],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
