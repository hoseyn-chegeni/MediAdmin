# filters.py
import django_filters
from .models import Reception
from django.utils import timezone
from calendar import monthrange

class ReceptionFilter(django_filters.FilterSet):
    date_range = django_filters.ChoiceFilter(
        label='Filter by Date',
        method='filter_by_date_range',
        choices=(
            ('this_day', 'This Day'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
        )
    )

    def filter_by_date_range(self, queryset, name, value):
        today = timezone.now().date()
        if value == 'this_day':
            return queryset.filter(created_at__date=today)
        elif value == 'this_week':
            start_of_week = today - timezone.timedelta(days=today.weekday())
            end_of_week = start_of_week + timezone.timedelta(days=6)
            return queryset.filter(created_at__date__range=[start_of_week, end_of_week])
        elif value == 'this_month':
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(day=monthrange(today.year, today.month)[1])
            return queryset.filter(created_at__date__range=[start_of_month, end_of_month])
        return queryset

