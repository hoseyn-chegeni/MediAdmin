from django.contrib import admin
from .models import Client, ClientGallery, ClientAttachment

# Register your models here.

from django_jalali.admin.filters import JDateFieldListFilter

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


class BarAdmin(admin.ModelAdmin):
    list_filter = (("date_of_birth", JDateFieldListFilter),)


admin.site.register(Client, BarAdmin)
admin.site.register(ClientGallery)
admin.site.register(ClientAttachment)
