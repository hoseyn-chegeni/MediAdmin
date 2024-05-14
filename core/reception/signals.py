from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reception
from datetime import date
from consumable.models import Inventory
from financial.models import ConsumablePrice
from tasks.models import Task
from planner.models import Session
from prescription.models import TemporaryPrescription


@receiver(post_save, sender=Reception)
def update_last_reception_date(sender, instance, created, **kwargs):
    if created:
        client = instance.client
        client.number_of_receptions += 1
        client.last_reception_date = instance.date
        client.last_reception_reason = f"{instance.service}/ {instance.reason}"
        client.save()


@receiver(post_save, sender=Reception)
def update_reception_number(sender, instance, created, **kwargs):
    if created:
        today = date.today()
        reception_number = Reception.objects.filter(
            date=today, service=instance.service
        ).count()
        instance.reception_in_day = reception_number
        instance.save()


@receiver(post_save, sender=Reception)
def update_appointment_status(sender, instance, created, **kwargs):
    if created and instance.session:
        session = Session.objects.get(id=instance.session.id)
        session.status = "پذیرش شده"
        session.save()


@receiver(post_save, sender=Reception)
def update_consumable_inventory(sender, instance, created, **kwargs):
    if created:
        valid_inventory = False
        for i in instance.service.serviceconsumable_set.all():

            inventory = Inventory.objects.filter(
                consumable_id=i.consumable.id, status="در انبار"
            ).order_by("expiration_date")
            for j in inventory:
                if j.quantity >= int(i.dose):
                    j.quantity = j.quantity - int(i.dose)
                    if j.quantity == 0:
                        j.status = "تمام شده"
                    j.save()
                    valid_inventory = True
                    ConsumablePrice.objects.create(
                        reception=instance,
                        consumable=j,
                        price=j.price * int(i.dose),
                        dose=int(i.dose),
                    )
                    break
            if valid_inventory == False:
                for i in instance.service.serviceconsumable_set.all():
                    inventory = Inventory.objects.filter(
                        consumable_id=i.consumable.id, status="در انبار"
                    ).order_by("expiration_date")
                    dose = int(i.dose)
                    for j in inventory:
                        if dose != 0 and dose > j.quantity:
                            dose = dose - j.quantity
                            j.quantity = 0
                            j.status = "تمام شده"
                            j.save()
                            ConsumablePrice.objects.create(
                                reception=instance,
                                consumable=j,
                                price=j.price * dose,
                                dose=dose,
                            )

                        elif dose != 0 and dose < j.quantity:

                            ConsumablePrice.objects.create(
                                reception=instance,
                                consumable=j,
                                price=j.price * (j.quantity - dose),
                                dose=dose,
                            )
                            j.quantity = j.quantity - dose
                            dose = 0
                            j.save()

            else:
                if i.consumable.quantity <= i.consumable.reorder_quantity:
                    Task.objects.create(
                        title=f"سفارش مجدد محصول {i.consumable}",
                        description=(
                            f"نیاز به شارژ مجدد محصول {i.consumable} می باشد. "
                            "لطفا در اسرع وقت نسبت به سفارش مجدد این محصول اقدام نمایید.\n"
                            "با سپاس"
                        ),
                        type="سفارش مجدد",
                        status="در انتظار بررسی",
                        priority="بالا",
                    )

