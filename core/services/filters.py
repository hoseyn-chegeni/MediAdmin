import django_filters
from django_filters import FilterSet
from .models import Service
from django.db import models


class ServicesFilter(FilterSet):

    class Meta:
        model = Service
        fields = {
            "id": ["exact"],
            "doctor": ["exact"],
            "category": ["exact"],
            "name": ["exact"],
        }
