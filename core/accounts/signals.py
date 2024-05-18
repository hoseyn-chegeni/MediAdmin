from django.db.models.signals import post_save
from django.dispatch import receiver
from kavenegar import *
from os import getenv
from logs.models import UserSMSLog
from .models import User


# @receiver(post_save, sender=User)
# def send_sms_after_create_account(sender, instance, created, **kwargs):
#     if created:
#         try:
#             api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
#             params = {
#                 "sender": "2000500666",  # optional
#                 "receptor": instance.phone_number,  # multiple mobile number, split by comma
#                 "message": f"{instance.get_full_name()} عزیز حساب کاربری شما با موفقیت در تاریخ {instance.created_at.date()} ایجاد شد.",
#             }
#             response = api.sms_send(params)
#             print(response)
#             UserSMSLog.objects.create(
#                 user=instance,
#                 sender_number=params["sender"],
#                 receiver_number=params["receptor"],
#                 subject="اطلاع رسانی ایجاد حساب کاربری",
#                 message_body=params["message"],
#                 status=response["status"],
#                 response=response,
#             )
#         except (APIException, HTTPException) as e:
#             print(e)
#             UserSMSLog.objects.create(
#                 user=instance,
#                 sender_number=params["sender"],
#                 receiver_number=params["receptor"],
#                 subject="اطلاع رسانی ایجاد حساب کاربری",
#                 message_body=params["message"],
#                 status="Field",
#                 response=e,
#             )
