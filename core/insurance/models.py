from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Insurance(models.Model):
    name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=50)
    insurance_company = models.CharField(max_length=100)
    deductible = models.DecimalField(max_digits=10, decimal_places=2)
    copay = models.DecimalField(max_digits=10, decimal_places=2)
    max_annual_coverage = models.DecimalField(max_digits=10, decimal_places=2)
    policy_type = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name
    

class InsuranceService(models.Model):
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    insurance = models.ForeignKey("Insurance", on_delete=models.CASCADE)
    percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.insurance}/{self.service}"
