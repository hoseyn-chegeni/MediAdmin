import django_filters
from django_filters import FilterSet
from .models import Prescription
from django.db import models


class PrescriptionFilter(FilterSet):

    class Meta:
        model = Prescription
        fields = {"id": ["exact"]}
