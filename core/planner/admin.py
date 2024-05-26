from django.contrib import admin
from .models import WeekDay, Month, Day, Session, DeletedSession, JalaliDateHandler

# Register your models here.
from django.contrib import admin

from django_jalali.admin.filters import JDateFieldListFilter

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


class BarAdmin(admin.ModelAdmin):
    list_filter = (("date", JDateFieldListFilter),)


class HandlerAdmin(admin.ModelAdmin):
    list_filter = (("jalali_date", JDateFieldListFilter),)


admin.site.register(Day, BarAdmin)
admin.site.register(Month)
admin.site.register(WeekDay)
admin.site.register(Session)
admin.site.register(DeletedSession)
admin.site.register(JalaliDateHandler, HandlerAdmin)
