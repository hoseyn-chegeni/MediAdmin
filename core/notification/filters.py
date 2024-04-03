from django_filters import FilterSet
from logs.models import ClientSMSLog
from base.models import BaseFilter

class ClientSMSLogFilter(BaseFilter):
    class Meta:
        model = ClientSMSLog
        fields = {
            'id':['exact'],
            'sender_number':['exact'],
            'subject':['exact'],
            'sender_number':['exact'],
            'status':['exact'],
        }