from django.db import models

# Create your models here.
from django.db import models


class Consumable(models.Model):
    # General Information
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "ConsumableCategory", on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=50)
    minimum_stock_level = models.PositiveIntegerField(default=0)
    inventory_tracking_number = models.PositiveIntegerField(blank=True, null=True)

    # Purchase Information
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.SET_NULL, blank=True, null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(null=True, blank=True)

    # Usage Information
    usage_notes = models.TextField(blank=True)
    last_usage_date = models.DateField(null=True, blank=True)

    # Storage Information
    location = models.CharField(max_length=255)
    storage_notes = models.TextField(blank=True)

    # Financial Information
    depreciation_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text="in percentage"
    )
    disposal_method = models.CharField(max_length=100, blank=True)

    # Additional Information
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


class ConsumableCategory(models.Model):
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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
