from django.db import models


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

    def __str__(self):
        return self.name
