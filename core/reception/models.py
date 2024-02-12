from django.db import models

class Reception(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    PAYMENT_TYPE_CHOICES = (
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('INSURANCE', 'Insurance'),
        ('OTHER', 'Other'),
    )
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    PAYMENT_STATUS_CHOICES = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('UNPAID', 'Unpaid'),
    )
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    prescription = models.TextField()

    def __str__(self):
        return f'Reception for {self.client.first_name} {self.client.last_name}'
