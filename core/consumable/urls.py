from django.urls import path
from .views import (
    ConsumableCreateView,
    ConsumableListView,
    ConsumableDeleteView,
    ConsumableDetailView,
    ConsumableUpdateView,
    InventoryCreateView,
    InventoryDeleteView,
    InventoryDetailView,
    InventoryListView,
    InventoryUpdateView,
)

app_name = "consumable"


urlpatterns = [
    # CONSUMABLE URLS...
    path("list/", ConsumableListView.as_view(), name="list"),
    path("detail/<int:pk>/", ConsumableDetailView.as_view(), name="detail"),
    path("create/", ConsumableCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ConsumableUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ConsumableDeleteView.as_view(), name="delete"),
    # INVENTORY URLS...
    path("inventory_list/", InventoryListView.as_view(), name="inventory_list"),
    path(
        "inventory_detail/<int:pk>/",
        InventoryDetailView.as_view(),
        name="inventory_detail",
    ),
    path("inventory_create/", InventoryCreateView.as_view(), name="inventory_create"),
    path(
        "inventory_update/<int:pk>/",
        InventoryUpdateView.as_view(),
        name="inventory_update",
    ),
    path(
        "inventory_delete/<int:pk>/",
        InventoryDeleteView.as_view(),
        name="inventory_delete",
    ),
]
