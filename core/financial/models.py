from django.db import models

# Create your models here.
class Financial(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    reception = models.ForeignKey('reception.Reception', on_delete = models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=(
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial Payment'),
    ), default='UNPAID')
    payment_received_date = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calculate total amount
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.reception.client}"