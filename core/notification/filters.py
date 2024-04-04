from django_filters import CharFilter
from logs.models import ClientSMSLog
from base.filters import BaseFilter


class ClientSMSLogFilter(BaseFilter):
    case_id = CharFilter(
        field_name="client__case_id", label="Case ID", lookup_expr="exact"
    )

    # Filter by client national ID
    national_id = CharFilter(
        field_name="client__national_id", label="National ID", lookup_expr="exact"
    )

    # Filter by client name
    name = CharFilter(label="Client Name", method="filter_by_name")

    class Meta:
        model = ClientSMSLog
        fields = {
            "id": ["exact"],
            "sender_number": ["exact"],
            "subject": ["exact"],
            "sender_number": ["exact"],
            "status": ["exact"],
        }
