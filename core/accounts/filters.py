import django_filters
from django_filters import FilterSet
from .models import User
from django.db import models


class UserFilter(FilterSet):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = User
        fields = {
            "id": ["exact"],
            "email": ["exact", "icontains"],  # You can add multiple lookup types here
            # Add other fields if needed
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )
