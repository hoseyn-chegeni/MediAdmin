import django_filters
from django_filters import FilterSet ,DateFilter, ChoiceFilter
from .models import Financial
from .models import OfficeExpenses
from django import forms
from datetime import datetime, timedelta


class FinancialFilter(FilterSet):

    class Meta:
        model = Financial
        fields = {
            "id": ["exact"],
        }




class OfficeExpensesFilter(django_filters.FilterSet):
    date = DateFilter(
        field_name="date",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    subject = django_filters.CharFilter(lookup_expr='icontains')
    recipient_name = django_filters.CharFilter(lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name='id')

    date_range = ChoiceFilter(
            label="Date Range",
            method="filter_by_date_range",
            choices=(
                ("today", "Today"),
                ("this_week", "This Week"),
                ("this_month", "This Month"),
            ),
        )
    

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


    def filter_by_date(self, queryset, name, value):
        return queryset.filter(date=value)
    class Meta:
        model = OfficeExpenses
        fields = ['user', 'date', 'subject', 'recipient_name', 'id','date_range']
