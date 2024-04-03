import django_filters
from django_filters import FilterSet, ChoiceFilter, DateFilter
from .models import Client
from django.db import models
from datetime import datetime, timedelta
from reception.models import Reception
from base.filters import BaseFilter
from django import forms
from booking.models import Appointment
from logs.models import ClientSMSLog
from financial.models import  Financial

class ClientFilters(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Client
        fields = {
            "id": ["exact"],
            "case_id": ["exact"],
            "national_id": ["exact"],
            "is_vip": ["exact"],
            "gender": ['exact'],
            "insurance": ['exact'],
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

class ClientAppointmentFilter(FilterSet):
    # Filter by service

    # Filter by date
    date = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(date=value)

    class Meta:
        model = Appointment
        fields = [
            "service",
            "date",
        ]


class ClientSMSFilter(FilterSet):
    # Filter by service

    # Filter by date
    date = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(created_at__date=value)

    class Meta:
        model = ClientSMSLog
        fields = [
            "subject",
            "date",
        ]
