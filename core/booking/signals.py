from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PackageAppointment, Appointment
from services.models import ServicePackage
from django.utils.timezone import timedelta
from .models import Appointment
from kavenegar import *
from os import getenv
from logs.models import ClientSMSLog


@receiver(post_save, sender=PackageAppointment)
def create_appointments(sender, instance, created, **kwargs):
    if created:
        # Retrieve the services associated with the package
        package_services = ServicePackage.objects.filter(package=instance.package)

        # Initialize initial date with the booking date
        appointment_date = instance.date

        # Create appointments for each service
        for service_package in package_services:
            service = service_package.service

            # Create the appointment
            Appointment.objects.create(
                service=service,
                client=instance.client,
                national_code=instance.national_code,
                name=instance.name,
                date=appointment_date,
                status="WAITE",
                has_package=True,
                package=instance,
            )
            appointment_date += timedelta(days=service_package.gap_with_next_service)


@receiver(post_save, sender=Appointment)
def send_service_appointment_creation_info(sender, instance, created, **kwargs):
    if created and instance.has_package == False:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            params = {
                "sender": "2000500666",  # optional
                "receptor": f"{instance.client.phone_number}",  # multiple mobile number, split by comma
                "message": f"{instance.client.get_full_name()} عزیز نوبت شما برای سرویس  {instance.service} برای تاریخ {instance.date} ایجاد شد لطفا در تاریخ اعلام شده در مطب حضور داشته باشید.",
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


@receiver(post_save, sender=PackageAppointment)
def send_package_appointment_creation_info(sender, instance, created, **kwargs):
    if created:
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            params = {
                "sender": "2000500666",  # optional
                "receptor": f"{instance.client.phone_number}",  # multiple mobile number, split by comma
                "message": f"{instance.client.get_full_name()} عزیز نوبت شما برای پکیچ  {instance.package} برای تاریخ {instance.date} ایجاد شد لطفا در تاریخ اعلام شده در مطب حضور داشته باشید.",
            }
            response = api.sms_send(params)
            print(response)
            ClientSMSLog.objects.create(
                client=instance.client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی نوبت دهی پکیج",
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
                subject="اطلاع رسانی نوبت دهی پکیح",
                message_body=params["message"],
                status="Field",
                response=e,
            )
