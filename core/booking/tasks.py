from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Appointment
from kavenegar import KavenegarAPI, APIException, HTTPException
from os import getenv
from datetime import datetime


@shared_task
def send_sms_reminders():
    # Calculate the date for tomorrow
    timezone.now()

    # Query appointments scheduled for tomorrow
    appointments_tomorrow = Appointment.objects.filter(date=timezone.now())

    # Iterate over appointments and send reminders
    for appointment in appointments_tomorrow:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
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


@shared_task
def update_appointment_status():
    # Calculate the date one day ago
    one_day_ago = datetime.now() - timedelta(days=1)

    # Get all appointments that are one day old and have not been marked as done
    appointments_to_update = Appointment.objects.filter(
        date__lte=one_day_ago,
        status__in=[
            "WAITE",
        ],
    )

    # Update the status of each appointment to done
    for appointment in appointments_to_update:
        appointment.status = "عدم مراجعه"
        appointment.save()
