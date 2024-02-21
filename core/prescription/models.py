from django.db import models

# Create your models here.
class PrescriptionHeader(models.Model):
    doctor = models.ForeignKey("doctor.Doctor", on_delete = models.CASCADE)
    member_of = models.CharField(max_length = 255) # به طور مثال عضو هییت علمی
    specialization = models.CharField(max_length = 100) # متبحر در
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f'{self.doctor.first_name} {self.doctor.last_name}'