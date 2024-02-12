import django_filters
from django_filters import FilterSet
from .models import Reception
from django.db import models


class ReceptionFilter(FilterSet):

    class Meta:
        model = Reception
        fields = {
            "id": ["exact"],
            "client": ["exact"],
        }

