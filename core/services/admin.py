from django.contrib import admin
from .models import Service, ServiceConsumable, OffDay

# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceConsumable)
admin.site.register(OffDay)
