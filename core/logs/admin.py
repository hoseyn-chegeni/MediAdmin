from django.contrib import admin
from .models import ClientSMSLog,UserSMSLog

# Register your models here.
admin.site.register(ClientSMSLog)
admin.site.register(UserSMSLog)