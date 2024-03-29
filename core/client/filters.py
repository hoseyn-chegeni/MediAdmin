import django_filters
from django_filters import FilterSet, ChoiceFilter, DateFilter
from .models import Client
from django.db import models
from datetime import datetime, timedelta
from reception.models import Reception
from services.models import Service
from django import forms
from booking.models import Appointment
from logs.models import ClientSMSLog


class ClientFilters(FilterSet):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Client
        fields = {
            "id": ["exact"],
            "case_id": ["exact"],
            "national_id": ["exact"],
            "is_vip": ["exact"],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value)
        )


class ReceptionFilter(FilterSet):
    # Filter by service

    # Filter by date
    date = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
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
        model = Reception
        fields = ["service", "date", "date_range"]


class FinancialFilter(FilterSet):
    # Filter by date
    date = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
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
        model = Reception
        fields = ["date", "date_range"]


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
