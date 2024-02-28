from django.contrib import admin
from .models import PrescriptionHeader, Prescription

# Register your models here.
admin.site.register(PrescriptionHeader)
admin.site.register(Prescription)
