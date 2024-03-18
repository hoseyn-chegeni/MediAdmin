from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PackageAppointment, Appointment
from services.models import ServicePackage
from django.utils.timezone import timedelta

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
                date=appointment_date
            )
            appointment_date += timedelta(days=service_package.gap_with_next_service)