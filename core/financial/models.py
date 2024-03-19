from django.db import models
from decimal import Decimal
from datetime import date


# Create your models here.
class Financial(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    reception = models.OneToOneField("reception.Reception", on_delete=models.CASCADE)
    valid_insurance = models.BooleanField(default=False)
    insurance_range = models.PositiveIntegerField(default=0)
    tax = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    coupon = models.ForeignKey("Coupon", on_delete=models.SET_NULL, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            if self.coupon and self.coupon.amount and self.coupon.valid_from <= date.today() <= self.coupon.valid_to:
                # Apply discount based on coupon amount
                self.discount = self.coupon.amount
                # Calculate service price and consumable prices
                self.service_price = self.reception.service.price
                self.consumable_price = sum(
                    sc.consumable.price
                    for sc in self.reception.service.serviceconsumable_set.all()
                )
                total_amount_before_tax = self.service_price + self.consumable_price
                total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
                self.tax = total_amount_after_tax - total_amount_before_tax
                total_amount_with_insurance = total_amount_after_tax - (
                    total_amount_after_tax
                    * (Decimal(str(self.insurance_range)) / Decimal(100))
                )
                self.total_amount = total_amount_after_tax
                self.insurance_amount = total_amount_after_tax - total_amount_with_insurance
                self.final_amount = total_amount_with_insurance - self.coupon.amount
            elif self.coupon and self.coupon.percentage  and  self.coupon.valid_from <= date.today() <= self.coupon.valid_to:
                           # Apply discount based on coupon amount
                self.discount = self.coupon.percentage
                # Calculate service price and consumable prices
                self.service_price = self.reception.service.price
                self.consumable_price = sum(
                    sc.consumable.price
                    for sc in self.reception.service.serviceconsumable_set.all()
                )
                total_amount_before_tax = self.service_price + self.consumable_price
                total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
                self.tax = total_amount_after_tax - total_amount_before_tax
                total_amount_with_insurance = total_amount_after_tax - (
                    total_amount_after_tax
                    * (Decimal(str(self.insurance_range)) / Decimal(100))
                )
                self.total_amount = total_amount_after_tax
                self.insurance_amount = total_amount_after_tax - total_amount_with_insurance
                self.final_amount =total_amount_with_insurance -  (total_amount_with_insurance  * (Decimal(str(self.discount)) / Decimal(100)))
            else:
                self.service_price = self.reception.service.price
                self.consumable_price = sum(
                    sc.consumable.price
                    for sc in self.reception.service.serviceconsumable_set.all()
                )
                total_amount_before_tax = self.service_price + self.consumable_price
                total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
                self.tax = total_amount_after_tax - total_amount_before_tax
                total_amount_with_insurance = total_amount_after_tax - (
                    total_amount_after_tax
                    * (Decimal(str(self.insurance_range)) / Decimal(100))
                )
                self.total_amount = total_amount_after_tax
                self.insurance_amount = total_amount_after_tax - total_amount_with_insurance
                self.final_amount = total_amount_with_insurance

        if "service_price" in kwargs.get("update_fields", []) or "consumable_price" in kwargs.get("update_fields", []):
            # Recalculate total amount including tax
            total_amount_before_tax = self.service_price + self.consumable_price
            total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
            self.total_amount = total_amount_after_tax

        super().save(*args, **kwargs)

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



class Coupon(models.Model): #BASED ON AMOUNT
    name = models.CharField(max_length = 255)
    code = models.CharField(max_length=20, unique=True, blank = True, null = True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank = True, null = True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return self.name

