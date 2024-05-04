from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Session
from kavenegar import KavenegarAPI, APIException, HTTPException
from os import getenv
from datetime import datetime


@shared_task
def send_sms_reminders():
    # Calculate the date for tomorrow
    date = datetime.now() + timedelta(days=1)

    # Query appointments scheduled for tomorrow
    appointments_tomorrow = Session.objects.filter(day__date = date)

    # Iterate over appointments and send reminders
    for appointment in appointments_tomorrow:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            message = "همراه گرامی لطفا فردا در ساعت تایین شده در مطب حضور داشته باشید"
            if appointment.client:
                params = {
                    "sender": "2000500666",
                    "receptor": appointment.client.phone_number,
                    "message": message,
                }
            else:
                params = {
                    "sender": "2000500666",
                    "receptor": appointment.phone_number,
                    "message": message,
                }
            response = api.sms_send(params)
            print(e)
        except (APIException, HTTPException) as e:
            print(e)


@shared_task
def update_appointment_status():
    # Calculate the date one day ago
    one_day_ago = datetime.now() - timedelta(days=1)

    # Get all appointments that are one day old and have not been marked as done
    appointments_to_update = Session.objects.filter(
        day__date__lte=one_day_ago,
        status="در انتظار",   
    )

    # Update the status of each appointment to done
    for appointment in appointments_to_update:
        appointment.status = "عدم مراجعه"
        appointment.save()
