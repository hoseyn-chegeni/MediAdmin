from django.db import models
from decimal import Decimal

# Create your models here.
class Financial(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    reception = models.OneToOneField('reception.Reception', on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    service_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    consumable_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=(
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial Payment'),
    ), default='UNPAID')
    payment_received_date = models.DateField(blank=True, null=True)
    tax_rate = Decimal('0.09')

    def save(self, *args, **kwargs):
        # Calculate service price
        self.service_price = self.reception.service.price
        
        # Calculate consumable prices
        consumable_prices = sum(sc.consumable.price for sc in self.reception.service.serviceconsumable_set.all())
        self.consumable_price = consumable_prices
        
        # Calculate total amount including tax
        total_amount_before_tax = self.service_price + self.consumable_price
        total_amount_after_tax = total_amount_before_tax * (1 + self.tax_rate)
        
        self.total_amount = total_amount_after_tax
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.reception.client}"