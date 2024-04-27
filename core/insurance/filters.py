import django_filters
from django_filters import FilterSet
from .models import Insurance, InsuranceService
from django.db import models
from base.filters import BaseFilter


class InsuranceFilter(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Insurance
        fields = {
            "id": ["exact"],
            "insurance_company": ["exact"],
            "policy_number": ["exact"],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )


class InsuranceServiceFilter(FilterSet):
    class Meta:
        model = InsuranceService
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "insurance": ["exact"],
        }
