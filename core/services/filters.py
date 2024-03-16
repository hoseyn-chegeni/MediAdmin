from django_filters import FilterSet
from .models import Service, ServiceCategory
from django_filters import FilterSet, CharFilter
from reception.models import Reception


class ServicesFilter(FilterSet):

    class Meta:
        model = Service
        fields = {
            "id": ["exact"],
            "doctor": ["exact"],
            "category": ["exact"],
            "name": ["exact"],
        }


class QueueFilter(FilterSet):

    # Filter by client case ID
    case_id = CharFilter(
        field_name="client__case_id", label="Case ID", lookup_expr="exact"
    )

    # Filter by client national ID
    national_id = CharFilter(
        field_name="client__national_id", label="National ID", lookup_expr="exact"
    )

    # Filter by client name
    name = CharFilter(label="Client Name", method="filter_by_name")

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(client__first_name__icontains=value) | queryset.filter(
            client__last_name__icontains=value
        )

    class Meta:
        model = Reception
        fields = ["id", "case_id", "national_id", "name"]


class ServiceCategoryFilter(FilterSet):

    class Meta:
        model = ServiceCategory
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }