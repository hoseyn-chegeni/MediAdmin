from django.urls import path
from .views import (
    EquipmentCreateView,
    EquipmentDeleteView,
    EquipmentDetailView,
    EquipmentListView,
    EquipmentUpdateView,
    DeleteSelectedEquipmentView,
)

app_name = "asset"

urlpatterns = [
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
    path(
        "equipment/delete/",
        DeleteSelectedEquipmentView.as_view(),
        name="delete_selected_equipment",
    ),
]
