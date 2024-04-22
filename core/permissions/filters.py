import django_filters
from django_filters import FilterSet
from django.contrib.auth.models import Permission, Group



class PermissionFilters(FilterSet):

    class Meta:
        model = Permission
        fields = ["id", "name", "content_type", "codename",]


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Group
        fields = ['name']
