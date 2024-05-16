from django.urls import path
from .views import (
    UserImportView,
    EquipmentImportView,
    ClientImportView,
    ConsumableImportView,
    SupplierImportView,
    DoctorImportView,
    InsuranceImportView,
    ReceptionImportView,
    ServiceImportView,
)

app_name = "import"

urlpatterns = [
    path("user/", UserImportView.as_view(), name="user"),
    path("equipment/", EquipmentImportView.as_view(), name="equipment"),
    path("client/", ClientImportView.as_view(), name="client"),
    path("consumable/", ConsumableImportView.as_view(), name="consumable"),
    path("supplier/", SupplierImportView.as_view(), name="supplier"),
    path("doctor/", DoctorImportView.as_view(), name="doctor"),
    path("insurance/", InsuranceImportView.as_view(), name="insurance"),
    path("reception/", ReceptionImportView.as_view(), name="reception"),
    path("service/", ServiceImportView.as_view(), name="service"),
]
