from django.urls import path
from .views import (
    SupplierCreateView,
    SupplierDeleteView,
    SupplierDetailView,
    SupplierListView,
    SupplierUpdateView,
    EquipmentCreateView,
    EquipmentDeleteView,
    EquipmentDetailView,
    EquipmentListView,
    EquipmentUpdateView,
)

app_name = "asset"

urlpatterns = [
    # SUPPLIER
    path("supplier/list/", SupplierListView.as_view(), name="supplier_list"),
    path(
        "supplier/detail/<int:pk>/",
        SupplierDetailView.as_view(),
        name="supplier_detail",
    ),
    path("supplier/create/", SupplierCreateView.as_view(), name="supplier_create"),
    path(
        "supplier/update/<int:pk>/",
        SupplierUpdateView.as_view(),
        name="supplier_update",
    ),
    path(
        "supplier/delete/<int:pk>/",
        SupplierDeleteView.as_view(),
        name="supplier_delete",
    ),
    # EQUIPMENT URLS.
    path("equipment/list/", EquipmentListView.as_view(), name="equipment_list"),
    path(
        "equipment/detail/<int:pk>/",
        EquipmentDetailView.as_view(),
        name="equipment_detail",
    ),
    path("equipment/create/", EquipmentCreateView.as_view(), name="equipment_create"),
    path(
        "equipment/update/<int:pk>/",
        EquipmentUpdateView.as_view(),
        name="equipment_update",
    ),
    path(
        "equipment/delete/<int:pk>/",
        EquipmentDeleteView.as_view(),
        name="equipment_delete",
    ),
]
