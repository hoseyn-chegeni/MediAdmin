import random
import string
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Financial
from reception.models import Reception
from .models import Coupon
from decimal import Decimal
from .models import ConsumablePrice


@receiver(post_save, sender=Reception)
def create_financial(sender, instance, created, **kwargs):
    if created:
        total_consumable_price = 0
        total_consumable_tax = 0
        total_consumable_price_final = 0

        for i in ConsumablePrice.objects.filter(reception_id=instance.id):
            total_consumable_price_final = total_consumable_price_final + i.final_amount
            total_consumable_tax = total_consumable_tax + i.tax_amount
            total_consumable_price = total_consumable_price + i.price

        wage = instance.service.price * (
            Decimal(str(instance.service.doctors_wage_percentage)) / Decimal(100)
        )
        revenue = instance.service.price - wage

        Financial.objects.create(
            reception=instance,
            jalali_date_issued = instance.jalali_date,
            invoice_number=f"INV-{instance.pk}",
            payment_status=instance.payment_status,
            payment_received_date=None,
            valid_insurance=True,
            attachment=instance.invoice_attachment,
            doctors_wage=wage,
            revenue=revenue,
            doctor=instance.service.doctor,
            service_price=instance.service.price,
            service_tax=instance.service.price * 0.1,
            service_price_final=instance.service.price + (instance.service.price * 0.1),
            consumable_price=total_consumable_price,
            consumable_tax=total_consumable_tax,
            consumable_price_final=total_consumable_price_final,
            total_amount=instance.service.price + total_consumable_price,
            final_amount=total_consumable_price_final
            + (instance.service.price + (instance.service.price * 0.1)),
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
