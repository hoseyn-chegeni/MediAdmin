from django.db import models


# Create your models here.


class Prescription(models.Model):
    reception = models.ForeignKey("reception.Reception", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    jalali_date = models.CharField(max_length=255)
    medication = models.TextField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"Prescription for {self.reception.client} by Dr. {self.reception.service.doctor}"


class PrescriptionHeader(models.Model):
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE)
    member_of = models.CharField(max_length=255)  # به طور مثال عضو هییت علمی
    specialization = models.CharField(max_length=100)  # متبحر در
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey("TemporaryPrescription", on_delete=models.CASCADE)
    medicine = models.CharField(max_length=255)  # نام دارو
    quantity = models.PositiveIntegerField()  #  تعداد
    consumption_time = models.CharField(max_length=255)  #  زمان مصرف
    consumption_dose = models.CharField(max_length=255)  #   مقدار مصرف
    how_to_use = models.CharField(max_length=255)  # طریقه مصرف
    repeat_interval = models.CharField(max_length=255)  # فاصله زمانی تکرار
    repeat_period = models.PositiveIntegerField()  # دوره تکراز


class TemporaryPrescription(models.Model):
    reception = models.ForeignKey("reception.Reception", on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )
