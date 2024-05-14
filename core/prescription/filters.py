import django_filters
from .models import Prescription
from base.filters import BaseFilter


class PrescriptionFilter(BaseFilter):
    reception_id = django_filters.NumberFilter(field_name='reception__id')
    name = django_filters.CharFilter(method="filter_by_name")
    reception_client_national_id = django_filters.CharFilter(field_name='reception__client__national_id', lookup_expr='icontains')
    reception_client_id = django_filters.NumberFilter(field_name='reception__client__id')
    reception_service_doctor = django_filters.CharFilter(field_name='reception__service__doctor', lookup_expr='icontains')
    reception_date = django_filters.DateFilter(field_name='reception__date')

    class Meta:
        model = Prescription
        fields = [
            'id',
        ]



    def filter_by_name(self, queryset, name, value):
        return queryset.filter(reception__client__first_name__icontains=value) | queryset.filter(
            reception__client__last_name__icontains=value
        )