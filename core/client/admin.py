from django.contrib import admin
from .models import Client, ClientGallery, ClientAttachment

# Register your models here.
admin.site.register(Client)
admin.site.register (ClientGallery)
admin.site.register (ClientAttachment)

