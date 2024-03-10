from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reception

@receiver(post_save, sender=Reception)
def update_last_reception_date(sender, instance, created, **kwargs):
    if created:
        client = instance.client
        client.number_of_receptions += 1
        client.last_reception_date = instance.date
        client.last_reception_reason = f'{instance.service}/ {instance.reason}'
        client.save()
