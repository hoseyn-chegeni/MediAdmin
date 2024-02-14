from django.contrib import admin
from .models import Insurance

# Register your models here.
@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['name', 'policy_number', 'insurance_company', 'deductible', 'copay', 'max_annual_coverage', 'policy_type', 'created_at', 'updated_at']
    search_fields = ['name', 'policy_number', 'insurance_company', 'policy_type']
    list_filter = ['insurance_company', 'policy_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'policy_number', 'insurance_company', 'policy_type')
        }),
        ('Coverage Details', {
            'fields': ('deductible', 'copay', 'max_annual_coverage', 'notes')
        }),
        ('Date Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Hide this section by default
        })
    )