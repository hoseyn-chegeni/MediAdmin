from django.db import models

# Create your models here.
from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    acquisition_date = models.CharField(max_length=255)  # تاریخ خرید
    warranty_expiry_date = models.DateField()
    location = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    in_use = models.BooleanField(default=False)

    description = models.TextField(blank=True, null=True)
    last_maintenance_date = models.CharField(
        max_length=255, blank=True, null=True
    )  # بازدید دوره ای
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Consumable(models.Model):
    name = models.TextField()
