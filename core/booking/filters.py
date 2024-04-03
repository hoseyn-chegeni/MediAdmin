from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter
from .models import Appointment, PackageAppointment
from base.filters import BaseFilter
from django import forms
from datetime import datetime, timedelta

class AppointmentFilter(FilterSet):
    created_by_email = CharFilter(field_name='created_by__email', lookup_expr='exact')

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
            return queryset.filter(date=today)
        elif value == "this_week":
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(date__range=[start_of_week, end_of_week])
        elif value == "this_month":
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(
                month=start_of_month.month + 1, day=1
            ) - timedelta(days=1)
            return queryset.filter(
                date__range=[start_of_month, end_of_month]
            )


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
        model = Appointment
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "national_code": ["exact"],
            "client_name": ["exact"],   #این دو فیلد برای فیلتر بیمار هایی است که پرونده ندارند
        }

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
        

class PackageAppointmentFilter(FilterSet):
    created_by_email = CharFilter(field_name='created_by__email', lookup_expr='exact')

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


    def filter_by_created_at(self, queryset, name, value):
        return queryset.filter(created_at__date=value)

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(date=value)

    def filter_by_date_range(self, queryset, name, value):
        today = datetime.now().date()
        if value == "today":
            return queryset.filter(date=today)
        elif value == "this_week":
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(date__range=[start_of_week, end_of_week])
        elif value == "this_month":
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(
                month=start_of_month.month + 1, day=1
            ) - timedelta(days=1)
            return queryset.filter(
                date__range=[start_of_month, end_of_month]
            )


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
        model = PackageAppointment
        fields = {
            "id": ["exact"],
            "package": ["exact"],
            "national_code": ["exact"],
            "client_name": ["exact"],   #این دو فیلد برای فیلتر بیمار هایی است که پرونده ندارند
        }
