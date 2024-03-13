from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reception
from datetime import date


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
        reception_number = Reception.objects.filter(date = today, service = instance.service).count()
        instance.reception_in_day = reception_number 
        instance.save()


 