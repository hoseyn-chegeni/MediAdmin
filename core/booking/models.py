from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
STATUS = (
    ("WAITE", "WAITE"),
    ("DONE", "DONE"),
)

class Appointment(models.Model):
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    client = models.ForeignKey(
        "client.Client", on_delete=models.CASCADE, blank=True, null=True
    )
    national_code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True)
    has_package = models.BooleanField(default=False)
    package = models.ForeignKey(
        "PackageAppointment", on_delete=models.CASCADE, blank=True, null=True
    )
    created_by = models.ForeignKey('accounts.User', on_delete = models.SET_NULL, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service}, {self.client}, {self.date}"


class PackageAppointment(models.Model):
    package = models.ForeignKey("services.Package", on_delete=models.CASCADE)
    client = models.ForeignKey(
        "client.Client", on_delete=models.CASCADE, blank=True, null=True
    )
    national_code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True)

    @property
    def completion_percentage(self):
        # Calculate the total number of appointments for this package
        total_appointments = self.appointment_set.count()

        # Calculate the number of appointments with a status of "done"
        done_appointments = self.appointment_set.filter(status="DONE").count()

        # Calculate the percentage
        if total_appointments == 0:
            return 0
        else:
            return (done_appointments / total_appointments) * 100

    def __str__(self):
        return f"{self.package}, {self.client}, {self.date}"





def validate_current_month(value):
    pass


def validate_max_appointments_per_day(value):
    pass