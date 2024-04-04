import django_filters
from django_filters import FilterSet, ChoiceFilter, DateFilter, CharFilter
from .models import Client
from django.db import models
from datetime import datetime, timedelta
from reception.models import Reception
from base.filters import BaseFilter
from django import forms
from booking.models import Appointment
from logs.models import ClientSMSLog
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


class ClientAppointmentFilter(FilterSet):
    created_by_email = CharFilter(field_name="created_by__email", lookup_expr="exact")

    date = DateFilter(
        field_name="date",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    created_at = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_created_at",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    # Filter by date range (today, this week, this month)
    date_range = ChoiceFilter(
        label="Date Range",
        method="filter_by_date_range",
        choices=(
            ("today", "Today"),
            ("this_week", "This Week"),
            ("this_month", "This Month"),
        ),
    )

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(date=value)

    def filter_by_created_at(self, queryset, name, value):
        return queryset.filter(created_at__date=value)

    def filter_by_date_range(self, queryset, name, value):
        today = datetime.now().date()
        if value == "today":
            return queryset.filter(created_at__date=today)
        elif value == "this_week":
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(created_at__date__range=[start_of_week, end_of_week])
        elif value == "this_month":
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(
                month=start_of_month.month + 1, day=1
            ) - timedelta(days=1)
            return queryset.filter(
                created_at__date__range=[start_of_month, end_of_month]
            )

    class Meta:
        model = Appointment
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "status": ["exact"],
            "package": ["exact"],
            "has_package": ["exact"],
        }
