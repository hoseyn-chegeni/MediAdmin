from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client
from planner.models import Session


@receiver(post_save, sender=Client)
def update_last_reception_date(sender, instance, created, **kwargs):
    if created and instance.initial_session:
        session = Session.objects.get(id = instance.initial_session.id)
        session.client = instance
        session.save()
        
