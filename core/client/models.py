from django.db import models

# Create your models here.
class Client(models.Model):
    case_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
    )
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)