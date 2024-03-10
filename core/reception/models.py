from django.db import models


class Reception(models.Model):
    client = models.ForeignKey("client.Client", on_delete=models.CASCADE)
    service = models.ForeignKey(
        "services.Service", on_delete=models.SET_NULL, blank=True, null=True
    )
    STATUS_CHOICES = (("WAITE", "Waite"), ("DONE", "Done"))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=True, null=True
    )
    reason = models.CharField(max_length=255)
    PAYMENT_TYPE_CHOICES = (
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("INSURANCE", "Insurance"),
        ("OTHER", "Other"),
    )
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    PAYMENT_STATUS_CHOICES = (
        ("PAID", "Paid"),
        ("PENDING", "Pending"),
        ("UNPAID", "Unpaid"),
    )
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"Reception for {self.client.first_name} {self.client.last_name}"
    
