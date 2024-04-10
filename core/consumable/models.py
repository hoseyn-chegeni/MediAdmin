from django.db import models

# Create your models here.
class ConsumableV2(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    minimum_stock_level = models.PositiveIntegerField(default=0)
    inventory_tracking_number = models.PositiveIntegerField(blank=True, null=True)
    expiration_reminder = models.PositiveIntegerField(default=1)
    usage_notes = models.TextField(blank=True)
    storage_notes = models.TextField(blank=True)
    # Additional Information
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True, related_name = 'creator'
    )

    def __str__(self):
        return self.name

class Inventory(models.Model):
    consumable = models.ForeignKey('ConsumableV2', on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    supplier = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

