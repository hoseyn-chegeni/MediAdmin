from django.contrib import admin
from .models import ClientSMSLog, UserSMSLog, UserActionLog

# Register your models here.
admin.site.register(ClientSMSLog)
admin.site.register(UserSMSLog)
admin.site.register(UserActionLog)
