import django_filters
from django_filters import FilterSet
from .models import Consumable
from django.db import models


class ConsumableFilter(FilterSet):

    class Meta:
        model = Consumable
        fields = {
            "id": ["exact"],
            "name": ["exact"],
        }
