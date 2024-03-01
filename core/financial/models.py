from django.db import models
from decimal import Decimal


# Create your models here.
class Financial(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    reception = models.OneToOneField("reception.Reception", on_delete=models.CASCADE)
    valid_insurance = models.BooleanField(default=False)
    insurance_range = models.PositiveIntegerField(default=0)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_issued = models.DateField(auto_now_add=True)
    service_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    consumable_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
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
            ("PAID", "Paid"),
            ("UNPAID", "Unpaid"),
            ("PARTIAL", "Partial Payment"),
        ),
        default="UNPAID",
    )
    payment_received_date = models.DateField(blank=True, null=True)
    tax_rate = Decimal("0.09")

    def save(self, *args, **kwargs):
        # If the financial instance is being created for the first time
        if not self.pk:
            # Calculate service price and consumable prices
            self.service_price = self.reception.service.price
            self.consumable_price = sum(
                sc.consumable.price
                for sc in self.reception.service.serviceconsumable_set.all()
            )
            total_amount_before_tax = self.service_price + self.consumable_price
            total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
            total_amount_with_insurance = total_amount_after_tax - (
                total_amount_after_tax
                * (Decimal(str(self.insurance_range)) / Decimal(100))
            )
            self.total_amount = total_amount_after_tax
            self.insurance_amount = total_amount_after_tax - total_amount_with_insurance
            self.final_amount = total_amount_with_insurance
        # Check if service price or consumable price has been modified
        if "service_price" in kwargs.get(
            "update_fields", []
        ) or "consumable_price" in kwargs.get("update_fields", []):
            # Recalculate total amount including tax
            total_amount_before_tax = self.service_price + self.consumable_price
            total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
            self.total_amount = total_amount_after_tax

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.reception.client}"
