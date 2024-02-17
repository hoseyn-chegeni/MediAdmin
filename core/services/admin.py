from django.contrib import admin
from .models import Service, ServiceConsumable

# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceConsumable)