from django.db import models


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
    category = models.ForeignKey('ServiceCategory', on_delete = models.SET_NULL, blank = True, null = True)
    duration = models.PositiveIntegerField()  # Duration in minutes
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    equipment_supplies = models.TextField(blank=True, null=True)
    preparation_instructions = models.TextField(blank=True, null=True)
    documentation_requirements = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    therapeutic_measures = models.TextField(blank=True)  # اقدمات درمانی
    recommendations = models.TextField(blank=True)  # توصیه ها
    # suggested_prescription = 0
    appointment_per_day = models.PositiveIntegerField(default=3)
    off_days = models.ManyToManyField("OffDay", blank=True)

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
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name