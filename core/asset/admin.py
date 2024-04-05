from django.contrib import admin
from .models import Consumable, Supplier, Equipment

# Register your models here.
admin.site.register(Consumable)
admin.site.register(Supplier)
admin.site.register(Equipment)
