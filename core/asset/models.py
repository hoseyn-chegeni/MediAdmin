from django.db import models

# Create your models here.
from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    acquisition_date = models.DateField()  # تاریخ خرید
    warranty_expiry_date = models.DateField()
    location = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    last_maintenance_date = models.DateField(blank=True, null=True)  # بازدید دوره ای
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
