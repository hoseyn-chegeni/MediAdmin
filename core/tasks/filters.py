import django_filters
from .models import Task
from django.db import models
from base.filters import BaseFilter


class TaskFilter(BaseFilter):

    class Meta:
        model = Task
        fields = {
            "id": ["exact"],
            "title": ["exact"],
            "type": ["exact"],
            "status": ["exact"],
            "priority": ["exact"],
            "status": ["exact"],
            "assign_to": ["exact"],
        }
