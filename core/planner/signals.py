from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Session
from kavenegar import *
from os import getenv
from logs.models import ClientSMSLog


@receiver(post_save, sender=Session)
def send_service_session_creation_info(sender, instance, created, **kwargs):
    if created and instance.client:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            params = {
                "sender": "2000500666",  # optional
                "receptor": f"{instance.client.phone_number}",  # multiple mobile number, split by comma
                "message": f"همراه گرامی نوبت شما با موفقیت ثبت شد \n نام بیمار: {instance.client.get_full_name()} \n زمان نوبت:‌ {instance.day}  \nکد پیگیری: {instance.id} \n نام پزشک: {instance.service.doctor} \n نام مرکز: مطب دکتر باقری \n آدرس مرکز: تهران تهرانسر خیبان سی ام \n تلفن مرکز:‌ 021445823456",
            }
            response = api.sms_send(params)
            print(response)
            ClientSMSLog.objects.create(
                client=instance.client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی نوبت دهی",
                message_body=params["message"],
                status=response["status"],
                response=response,
            )
        except (APIException, HTTPException) as e:
            print(e)
            ClientSMSLog.objects.create(
                client=instance.client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی نوبت دهی",
                message_body=params["message"],
                status="Field",
                response=e,
            )
    elif created and not instance.client:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            params = {
                "sender": "2000500666",  # optional
                "receptor": f"{instance.phone_number}",  # multiple mobile number, split by comma
                "message": f"نام بیمار: {instance.get_full_name} \n زمان نوبت:‌ {instance.day}  \nکد پیگیری: {instance.id} \n نام پزشک: {instance.service.doctor} \n نام مرکز: مطب دکتر باقری \n آدرس مرکز: تهران تهرانسر خیبان سی ام \n تلفن مرکز:‌ 021445823456",
            }
            response = api.sms_send(params)
            print(response)
        except (APIException, HTTPException) as e:
                print(e)