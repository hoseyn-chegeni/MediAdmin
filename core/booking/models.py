from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
STATUS = (
    ("WAITE", "WAITE"),
    ("DONE", "DONE"),
    ("پذیرش شده", "پذیرش شده"),
    ("عدم مراجعه", "عدم مراجعه"),
)


def validate_current_month(value):
    pass


def validate_max_appointments_per_day(value):
    pass


class Appointment(models.Model):
    name = models.TextField()