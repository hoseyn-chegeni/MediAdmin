from django.contrib import admin
from .models import ConsumableV2, Inventory, Supplier, ConsumableCategory

# Register your models here.
admin.site.register(ConsumableV2)
admin.site.register(Inventory)
admin.site.register(Supplier)
admin.site.register(ConsumableCategory)
