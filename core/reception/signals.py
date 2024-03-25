from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reception
from datetime import date
from kavenegar import *
from os import getenv
from logs.models import ClientSMSLog
import re


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
def send_sms(sender, instance, created, **kwargs):
    if created:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            params = {
                "sender": "2000500666",  # optional
                "receptor": "09356822312",  # multiple mobile number, split by comma
                "message": "همراه گرامی سرکار خانم  سپیده باقری نوبت شما برای سرویس بوتاکس  دکتر چگنی در تاریخ ۱۴۰۳/۰۱/۱۵ ثبت گردید لطفا در تاریخ اعلام شده در مطب حضور داشته باشید",
            }
            response = api.sms_send(params)
            print(response)
            ClientSMSLog.objects.create(
                client=instance.client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی پذیرش",
                message_body=params["message"],
                status=response["status"],
                response=response,
            )

        except APIException as e:
            print(e)
            response_text = str(e)
            matched_numbers = re.findall(r"\[([\d]+)\]", response_text)
            if matched_numbers:
                extracted_number = matched_numbers[0]
            else:
                extracted_number = None
            ClientSMSLog.objects.create(
                client=instance.client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی پذیرش",
                message_body=params["message"],
                status="Field",
                response=extracted_number,
            )
        except HTTPException as e:
            print(e)
            response_text = str(e)
            matched_numbers = re.findall(r"\[([\d]+)\]", response_text)
            if matched_numbers:
                extracted_number = matched_numbers[0]
            else:
                extracted_number = None

            ClientSMSLog.objects.create(
                client=instance.client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی پذیرش",
                message_body=params["message"],
                status="Field",
                response=extracted_number,
            )
