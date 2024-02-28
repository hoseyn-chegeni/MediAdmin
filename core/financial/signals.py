from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Financial
from reception.models import Reception


@receiver(post_save, sender=Reception)
def create_financial(sender, instance, created, **kwargs):
    if created:
        Financial.objects.create(
            reception=instance,
            invoice_number=f"INV-{instance.pk}",  # You can customize how the invoice number is generated
            payment_status="UNPAID",  # Default payment status
            payment_received_date=None,  # No payment received initially
        )
