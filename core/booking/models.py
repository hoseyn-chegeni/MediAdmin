from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
STATUS = (
    ("WAITE", "WAITE"),
    ("DONE", "DONE"),
    ("پذیرش شده", "پذیرش شده"),
    ("عدم مراجعه", "عدم مراجعه"),
)


class PackageAppointment(models.Model):
    package = models.ForeignKey("services.Package", on_delete=models.CASCADE)
    client = models.ForeignKey(
        "client.Client", on_delete=models.CASCADE, blank=True, null=True
    )
    national_code = models.CharField(max_length=100, blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True)
    prepayment = models.PositiveIntegerField(default=0)

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

    @property
    def final_price(self):
        # Calculate the final price by subtracting prepayment from total_price
        return self.package.total_price - self.prepayment

    def __str__(self):
        return f"{self.package}, {self.client}, {self.date}"


def validate_current_month(value):
    pass


def validate_max_appointments_per_day(value):
    pass
