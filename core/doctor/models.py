from django.db import models

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.User',on_delete = models.SET_NULL, blank = True, null = True )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
