import django_filters
from .models import Client, ClientAttachment
from django.db import models
from reception.models import Reception
from base.filters import BaseFilter
from financial.models import Financial


class ClientFilters(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Client
        fields = {
            "id": ["exact"],
            "case_id": ["exact"],
            "national_id": ["exact"],
            "is_vip": ["exact"],
            "gender": ["exact"],
            "insurance": ["exact"],
            "phone_number": ["exact"],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )


class ClientReceptionHistoryFilter(BaseFilter):

    class Meta:
        model = Reception
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "status": ["exact"],
        }


class ClientFinancialHistoryFilter(BaseFilter):

    class Meta:
        model = Financial
        fields = {
            "id": ["exact"],
            "invoice_number": ["exact"],
        }


class ClientAttachmentsFilter(BaseFilter):

    class Meta:
        model = ClientAttachment
        fields = {
            "id": ["exact"],
            "title": ["exact"],
            "type": ["exact"],

        }
