from django.urls import path
from .views import UserImportView, EquipmentImportView, ClientImportView

app_name = "import"

urlpatterns = [
    path("user/", UserImportView.as_view(), name="user"),
    path("equipment/", EquipmentImportView.as_view(), name="equipment"),
    path("client/", ClientImportView.as_view(), name="client"),

]
