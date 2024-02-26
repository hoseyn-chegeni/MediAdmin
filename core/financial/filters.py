import django_filters
from django_filters import FilterSet
from .models import Financial
from django.db import models


class FinancialFilter(FilterSet):

    class Meta:
        model = Financial
        fields = {
            "id": ["exact"],
        }


