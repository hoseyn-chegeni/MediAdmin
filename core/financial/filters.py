import django_filters
from django_filters import FilterSet ,   DateFilter
from .models import Financial
from .models import OfficeExpenses
from django import forms
class FinancialFilter(FilterSet):

    class Meta:
        model = Financial
        fields = {
            "id": ["exact"],
        }




class OfficeExpensesFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    date = DateFilter(
        field_name="created_at",
        label="Date (yyyy-mm-dd)",
        method="filter_by_date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    subject = django_filters.CharFilter(lookup_expr='icontains')
    recipient_name = django_filters.CharFilter(lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name='id')
    
    def filter_by_date(self, queryset, name, value):
        return queryset.filter(created_at__date=value)
    class Meta:
        model = OfficeExpenses
        fields = ['user', 'date', 'subject', 'recipient_name', 'id']
