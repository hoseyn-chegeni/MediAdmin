from django.db import models

STATUS_CHOICES = (
    ("در انبار", "در انبار"),
    ("تمام شده", "تمام شده"),
    ("سفارش داده شده", "سفارش داده شده"),
    ("منقضی شده", "منقضی شده"),
)


# Create your models here.
class ConsumableV2(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "ConsumableCategory", on_delete=models.SET_NULL, blank=True, null=True
    )
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.SET_NULL, blank=True, null=True
    )
    unit = models.CharField(max_length=50)
    minimum_stock_level = models.PositiveIntegerField(default=0)
    usage_notes = models.TextField(blank=True)
    storage_notes = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="creator",
    )
    reorder_quantity = models.PositiveIntegerField(default=1)

    @property
    def quantity(self):
        total_quantity = self.inventory_set.aggregate(
            total_quantity=models.Sum("quantity")
        )["total_quantity"]
        return total_quantity if total_quantity is not None else 0

    def __str__(self):
        return self.name


class Inventory(models.Model):
    consumable = models.ForeignKey("ConsumableV2", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    supplier = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    expiration_date = models.DateField(null=True, blank=True)
    expiration_reminder = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.consumable.name


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
