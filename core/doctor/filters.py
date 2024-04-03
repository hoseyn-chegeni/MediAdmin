from django_filters import FilterSet, CharFilter
from .models import Doctor
from django.db.models import Q
from base.filters import BaseFilter


class DoctorFilter(BaseFilter):
    name = CharFilter(method="filter_by_name")

    class Meta:
        model = Doctor
        fields = {
            "id": ["exact"],
            "email": ["icontains"],
            "specialization": ["icontains"],
            "registration_number": ["exact"],
            "is_active": ["exact"],
            "phone_number": ["exact"],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )
