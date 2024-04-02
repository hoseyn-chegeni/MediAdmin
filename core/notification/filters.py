from django_filters import FilterSet
from  logs.models import ClientSMSLog




class ClientSMSLogFilter(FilterSet):
    class Meta:
        model = ClientSMSLog
        fields = {
            "id": ["exact"],
            "client": ["exact"],
            "subject": ["exact"],
            }

