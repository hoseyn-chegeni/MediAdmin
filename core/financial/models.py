from django.db import models
from decimal import Decimal
from datetime import date
from django.db.models import Sum


# Create your models here.
class Financial(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    reception = models.OneToOneField("reception.Reception", on_delete=models.CASCADE)
    valid_insurance = models.BooleanField(default=False)
    insurance_range = models.PositiveIntegerField(default=0)

    discount = models.PositiveIntegerField(default=0)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_issued = models.DateField(auto_now_add=True)

    service_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    service_tax = models.PositiveIntegerField(default=0, blank=True, null=True)
    service_price_final = models.PositiveIntegerField(default=0, blank=True, null=True)

    consumable_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    consumable_tax = models.PositiveIntegerField(default=0, blank=True, null=True)
    consumable_price_final = models.PositiveIntegerField(
        default=0, blank=True, null=True
    )

    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    final_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ("پرداخت شده", "پرداخت شده"),
            ("پرداخت نشده", "پرداخت نشده"),
        ),
        default="پرداخت نشده",
    )
    payment_received_date = models.DateField(blank=True, null=True)
    tax_rate = Decimal("0.1")
    doctor = models.ForeignKey(
        "doctor.Doctor", on_delete=models.SET_NULL, blank=True, null=True
    )
    doctors_wage = models.PositiveIntegerField(default=0)
    revenue = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.SET_NULL, blank=True, null=True
    )
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.reception.client}"


class OfficeExpenses(models.Model):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="office_expenses",
    )
    date = models.DateField()
    subject = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_name = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="attachments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.date} - {self.subject}"


class Coupon(models.Model):  # BASED ON AMOUNT
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.name


class ConsumablePrice(models.Model):
    reception = models.ForeignKey("reception.Reception", on_delete=models.CASCADE)
    consumable = models.ForeignKey("consumable.Inventory", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    dose = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.reception}, {self.consumable}, {self.price}"

    @property
    def tax_amount(self):
        # Calculate 10% tax on the price
        return self.price * 0.1

    @property
    def final_amount(self):
        # Add tax to the price to get the final amount
        return self.price + self.tax_amount
