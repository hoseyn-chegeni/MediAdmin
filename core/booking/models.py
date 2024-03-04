from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext_lazy as _


# Create your models here.
def validate_current_month(value):
    today = timezone.now()
    if value.month != today.month or value.year != today.year:
        raise ValidationError("Date must be in the current month.")
    
def validate_max_appointments_per_day(value):
    # Count existing appointments for the given date
    existing_count = Appointment.objects.filter(date=value).count()
    if existing_count >= 3:
        raise ValidationError("Only three appointments are allowed per day.")


    
class Appointment(models.Model):
    service = models.ForeignKey('services.Service', on_delete = models.CASCADE)
    client = models.ForeignKey("client.Client", on_delete = models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'{self.service}, {self.client}, {self.date}'
    