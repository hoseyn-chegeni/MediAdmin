from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Appointment
from kavenegar import KavenegarAPI, APIException, HTTPException
from os import getenv


@shared_task
def send_sms_reminders():
    # Calculate the date for tomorrow
    timezone.now()

    # Query appointments scheduled for tomorrow
    appointments_tomorrow = Appointment.objects.filter(date=timezone.now())

    # Iterate over appointments and send reminders
    for appointment in appointments_tomorrow:
        try:
            api = KavenegarAPI(
                "344A4E6B3857684B454236343856666C39497A41484D354C584F6C30436C626138506976354B6B4635634D3D"
            )
            message = "this is a test from celery "
            params = {
                "sender": "2000500666",
                "receptor": appointment.client.phone_number,
                "message": message,
            }
            response = api.sms_send(params)
            print("done")
        except (APIException, HTTPException) as e:
            print("field")
