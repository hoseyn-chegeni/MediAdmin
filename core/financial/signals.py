from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Financial
from reception.models import Reception
from insurance.models import InsuranceService


@receiver(post_save, sender=Reception)
def create_financial(sender, instance, created, **kwargs):
    if created:
        client_insurance = instance.client.insurance
        service = instance.service
        service_insurance_services = InsuranceService.objects.filter(service=service)

    if service_insurance_services:
        for i in service_insurance_services:
            if i.id == client_insurance.id:
                Financial.objects.create(
                    reception=instance,
                    invoice_number=f"INV-{instance.pk}",  # You can customize how the invoice number is generated
                    payment_status="UNPAID",  # Default payment status
                    payment_received_date=None,  # No payment received initially
                    valid_insurance=True,
                    insurance_range=i.percentage,
                )
    else:
        Financial.objects.create(
            reception=instance,
            invoice_number=f"INV-{instance.pk}",  # You can customize how the invoice number is generated
            payment_status="UNPAID",  # Default payment status
            payment_received_date=None,  # No payment received initially
        )