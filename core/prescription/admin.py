from django.contrib import admin
from .models import PrescriptionHeader, Prescription, PrescriptionItem, TemporaryPrescription

# Register your models here.
admin.site.register(PrescriptionHeader)
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(TemporaryPrescription)

