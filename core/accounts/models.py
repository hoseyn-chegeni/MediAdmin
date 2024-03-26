from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", blank=True, null=True
    )
    national_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15, verbose_name="Phone Number", blank=True, null=True
    )
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="images", default="images/default.png", blank=True, null=True
    )
    login_attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
