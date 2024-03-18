from django.db import models
from datetime import date
from reception.models import Reception
from booking.models import Appointment

# Create your models here.

DAYS_OF_WEEK = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
)


class Service(models.Model):
    name = models.CharField(max_length=255)
    doctor = models.ForeignKey(
        "doctor.Doctor", on_delete=models.SET_NULL, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "ServiceCategory", on_delete=models.SET_NULL, blank=True, null=True
    )
    duration = models.PositiveIntegerField()  # Duration in minutes
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_instructions = models.TextField(blank=True, null=True)
    documentation_requirements = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    therapeutic_measures = models.TextField(blank=True)  # اقدمات درمانی
    recommendations = models.TextField(blank=True)  # توصیه ها
    # suggested_prescription = 0
    appointment_per_day = models.PositiveIntegerField(default=3)
    off_days = models.ManyToManyField("OffDay", blank=True)

    @property
    def today_reception_count(self):
        # Get today's date
        today = date.today()
        # Filter receptions for today and this service
        receptions_today = self.reception_set.filter(date=today)
        # Count the number of receptions
        return receptions_today.count()

    @property
    def total_reception_count(self):
        return Reception.objects.filter(service=self).count()

    @property
    def appointment_count_today(self):
        today = date.today()
        return Appointment.objects.filter(service=self, date=today).count()

    @property
    def waiting_receptions_today(self):
        today = date.today()
        return self.reception_set.filter(date=today, status="WAITE").count()

    @property
    def client_count(self):
        # Retrieve the IDs of clients who have used this service
        client_ids = (
            self.reception_set.all().values_list("client", flat=True).distinct()
        )
        # Count the number of unique client IDs
        return len(client_ids)

    def __str__(self):
        return self.name


class OffDay(models.Model):
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)

    def __str__(self):
        return DAYS_OF_WEEK[self.day_of_week][1]


class ServiceConsumable(models.Model):
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    consumable = models.ForeignKey("asset.Consumable", on_delete=models.CASCADE)
    dose = models.CharField(max_length=10, blank=True, null=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.service}.{self.consumable}"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    @property
    def number_of_services(self):
        return self.service_set.count()

    @property
    def total_receptions(self):
        total = 0
        for service in self.service_set.all():
            total += service.total_reception_count
        return total

    @property
    def receptions_today(self):
        today = date.today()
        total = 0
        for service in self.service_set.all():
            total += service.reception_set.filter(date=today).count()
        return total

    @property
    def number_of_appointments(self):
        today = date.today()
        # Get all services related to this category
        services = self.service_set.all()
        # Count appointments for all related services
        appointments_count = Appointment.objects.filter(
            service__in=services, date=today
        ).count()
        return appointments_count

    def __str__(self):
        return f"{self.name}"


class Package(models.Model):
    name = models.CharField(max_length=255)
    services = models.ManyToManyField(Service)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    preparation_instructions = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField()  # Duration in minutes
    therapeutic_measures = models.TextField(blank=True)  # اقدمات درمانی
    recommendations = models.TextField(blank=True)  # توصیه ها
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def calculate_price(self):
        total_price = 0
        # Iterate over services in the package
        for service in self.services.all():
            # Add the price of the service to the total price
            total_price += service.price
            # Iterate over related consumables for the service
            for service_consumable in service.serviceconsumable_set.all():
                # Add the price of the consumable to the total price
                total_price += service_consumable.consumable.price
        return total_price