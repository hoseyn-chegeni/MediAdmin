from  django.urls import path
from .views import UserImportView, EquipmentImportView

app_name = 'import'

urlpatterns = [
        path("user/", UserImportView.as_view(), name="user"),
        path("equipment/", EquipmentImportView.as_view(), name="equipment"),


]