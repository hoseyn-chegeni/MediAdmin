# filters.py
import django_filters
from .models import Reception
from django.utils import timezone
from calendar import monthrange
from django_filters import FilterSet, ChoiceFilter, DateFilter, CharFilter
from datetime import datetime, timedelta
from django import forms

class ReceptionFilter(FilterSet):

    # Filter by date
    date = DateFilter(field_name='created_at', label='Date (yyyy-mm-dd)', method='filter_by_date', widget=forms.DateInput(attrs={'type': 'date'}))

    # Filter by date range (today, this week, this month)
    date_range = ChoiceFilter(label='Date Range', method='filter_by_date_range', choices=(
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
    ))

    # Filter by client case ID
    case_id = CharFilter(field_name='client__case_id', label='Case ID', lookup_expr='exact')

    # Filter by client national ID
    national_id = CharFilter(field_name='client__national_id', label='National ID', lookup_expr='exact')

    # Filter by client name
    name = CharFilter(label='Client Name', method='filter_by_name')

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(client__first_name__icontains=value) | queryset.filter(client__last_name__icontains=value)

    def filter_by_date(self, queryset, name, value):
        return queryset.filter(created_at__date=value)
    

    def filter_by_date_range(self, queryset, name, value):
        today = datetime.now().date()
        if value == 'today':
            return queryset.filter(created_at__date=today)
        elif value == 'this_week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(created_at__date__range=[start_of_week, end_of_week])
        elif value == 'this_month':
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(month=start_of_month.month+1, day=1) - timedelta(days=1)
            return queryset.filter(created_at__date__range=[start_of_month, end_of_month])

    class Meta:
        model = Reception
        fields = ['service', 'date', 'date_range', 'case_id', 'national_id', 'name']
