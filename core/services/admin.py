from django.contrib import admin
from .models import (
    Service,
    ServiceConsumable,
    OffDay,
    ServiceCategory,
    Package,
    ServicePackage,
    ServiceSpecification
)

# Register your models here.
admin.site.register(ServiceConsumable)
admin.site.register(OffDay)
admin.site.register(ServiceCategory)
admin.site.register(Package)
admin.site.register(ServicePackage)


class ServiceSpecification(admin.TabularInline):
    model = ServiceSpecification

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'doctor', 'category', 'price', 'is_active']  # Fields to display in the list view
    list_filter = ['doctor', 'category', 'is_active']  # Fields for filtering the list
    search_fields = ['name', 'description']  # Fields for searching

    fieldsets = (
        (None, {
            'fields': ('name', 'doctor', 'category', 'price', 'is_active')
        }),
        ('Details', {
            'fields': ('description', 'duration', 'preparation_instructions', 'documentation_requirements')
        }),
        ('Additional Information', {
            'fields': ('doctors_wage_percentage', 'appointment_per_day', 'medical_equipment', 'off_days')
        }),
    )  # Divide fields into sections in the admin form
    inlines = [
        ServiceSpecification,
    ]
admin.site.register(Service, ServiceAdmin)

