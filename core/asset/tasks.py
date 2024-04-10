from celery import shared_task
from datetime import timedelta
from datetime import datetime
from .models import Consumable
from tasks.models import Task


@shared_task
def check_consumable_expiration():
    consumable = Consumable.objects.all()

    # Create a task for each expired or about to expire consumable
    for i in consumable:
        reminder_days = i.expiration_reminder
        expiration_date = i.expiration_date

        reminder_date = expiration_date - timedelta(days=reminder_days)

        # Create a reminder task if the reminder date is one day ago
        if reminder_date == datetime.now().date():
            Task.objects.create(
                title=f"Expiration reminder for {i}",
                description=f"Reminder: The consumable {i} will expire in {reminder_days} days.",
                type="expire",
                status="در انتظار بررسی",
                priority="بالا",
            )
