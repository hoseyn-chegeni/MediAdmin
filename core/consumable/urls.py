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
    ConsumableCategoryCreateView,
    ConsumableCategoryDeleteView,
    ConsumableCategoryDetailView,
    ConsumableCategoryListView,
    ConsumableCategoryUpdateView,
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
    # CONSUMABLE CATEGORY VIEWS
    path("category/list/", ConsumableCategoryListView.as_view(), name="category_list"),
    path(
        "category/detail/<int:pk>/",
        ConsumableCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "category/create/",
        ConsumableCategoryCreateView.as_view(),
        name="category_create",
    ),
    path(
        "category/update/<int:pk>/",
        ConsumableCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category/delete/<int:pk>/",
        ConsumableCategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
