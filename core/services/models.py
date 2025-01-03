from django.db import models
from datetime import date
from reception.models import Reception
from django.core.validators import MaxValueValidator

# Create your models here.

DAYS_OF_WEEK = (
    (1, "شنبه"),
    (2, "یک شنبه"),
    (3, "دو شنبه"),
    (4, "سه شنبه"),
    (5, "چهارشنبه"),
    (6, "پنج شنبه"),
    (7, "جمعه"),
)


class Service(models.Model):
    name = models.CharField(max_length=255)
    doctor = models.ForeignKey(
        "doctor.Doctor", on_delete=models.SET_NULL, blank=True, null=True
    )
    doctors_wage_percentage = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)]
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "ServiceCategory", on_delete=models.SET_NULL, blank=True, null=True
    )
    duration = models.PositiveIntegerField()  # Duration in minutes
    price = models.PositiveIntegerField(default=1)
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
    medical_equipment = models.ManyToManyField("asset.Equipment", blank=True)
    check_consumable_inventory = models.BooleanField(default=True)

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


class ServiceSpecification(models.Model):
    attribute_key = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=500)
    service = models.ForeignKey("services.Service", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.service.name


class OffDay(models.Model):
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)

    def __str__(self):
        return DAYS_OF_WEEK[self.day_of_week][1]


class ServiceConsumable(models.Model):
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    consumable = models.ForeignKey("consumable.ConsumableV2", on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.name}"


class Package(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    preparation_instructions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)
    attachment = models.FileField(upload_to="attachments", blank=True, null=True)

    @property
    def total_price(self):
        # Initialize total price
        total_price = 0

        # Iterate through all services in the package
        for service_package in self.servicepackage_set.all():
            service = service_package.service

            # Add price of the service
            total_price += service.price

            # Add price of consumables associated with the service
            for service_consumable in service.serviceconsumable_set.all():
                total_price += service_consumable.consumable.price

        return total_price

    @property
    def service_count(self):
        return self.servicepackage_set.count()

    def __str__(self):
        return self.name


# Package Steps
class ServicePackage(models.Model):
    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    gap_with_next_service = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.package} / {self.service}"
