import random
import string
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Financial
from reception.models import Reception
from insurance.models import InsuranceService
from .models import Coupon


@receiver(post_save, sender=Reception)
def create_financial(sender, instance, created, **kwargs):
    if created:
        client_insurance = instance.client.insurance
        service = instance.service
        service_insurance_services = InsuranceService.objects.filter(
            service_id=service.id
        )

        if service_insurance_services.exists():
            for i in service_insurance_services:
                if i.insurance == client_insurance:
                    Financial.objects.create(
                        reception=instance,
                        invoice_number=f"INV-{instance.pk}",  # You can customize how the invoice number is generated
                        payment_status="UNPAID",  # Default payment status
                        payment_received_date=None,  # No payment received initially
                        valid_insurance=True,
                        insurance_range=i.percentage,
                    )
                    break
        else:
            Financial.objects.create(
                reception=instance,
                invoice_number=f"INV-{instance.pk}",  # You can customize how the invoice number is generated
                payment_status="UNPAID",  # Default payment status
                payment_received_date=None,  # No payment received initially
            )


@receiver(pre_save, sender=Coupon)
def generate_coupon_code(sender, instance, **kwargs):
    if not instance.code:
        # Generate a random code
        code_length = 8
        chars = string.ascii_uppercase + string.digits
        code = "".join(random.choice(chars) for _ in range(code_length))
        # Check if the generated code already exists
        while Coupon.objects.filter(code=code).exists():
            code = "".join(random.choice(chars) for _ in range(code_length))
        instance.code = code
