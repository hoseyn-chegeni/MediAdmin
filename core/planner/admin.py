from django.contrib import admin
from .models import WeekDay, Month,Day, Session
# Register your models here.
admin.site.register(Day)
admin.site.register(Month)
admin.site.register(WeekDay)
admin.site.register(Session)