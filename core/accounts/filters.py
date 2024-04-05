import django_filters
from django_filters import FilterSet, DateFilter, CharFilter
from .models import User
from logs.models import UserSMSLog, ClientSMSLog
from django import forms
from base.filters import BaseFilter


class UserFilter(BaseFilter):
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = User
        fields = {
            "id": ["exact"],
            "email": ["exact", "icontains"],
            "national_id": ["exact"],
            "is_active": ['exact'],
        }

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value) | queryset.filter(
            last_name__icontains=value
        )


class UserSentSMSFilter(FilterSet):
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


class UserSMSFilter(FilterSet):
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
        model = UserSMSLog
        fields = [
            "subject",
            "date",
        ]
