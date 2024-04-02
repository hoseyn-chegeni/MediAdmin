import django_filters
from django_filters import FilterSet
from .models import Insurance, InsuranceService
from django.db import models


class InsuranceFilter(FilterSet):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Insurance
        fields = {"id": ["exact"], "policy_number": ["exact"]}

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )

class InsuranceServiceFilter(FilterSet):
    class Meta:
        model = InsuranceService
        fields = {"id": ["exact"], "service": ["exact"],"insurance": ["exact"],}

