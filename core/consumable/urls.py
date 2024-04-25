from django.urls import path
from .views import (
    ConsumableCreateView,
    ConsumableListView,
    ConsumableDeleteView,
    ConsumableDetailView,
    ConsumableUpdateView,
    InventoryDeleteView,
    InventoryDetailView,
    InventoryUpdateView,
    ConsumableCategoryCreateView,
    ConsumableCategoryDeleteView,
    ConsumableCategoryDetailView,
    ConsumableCategoryListView,
    ConsumableCategoryUpdateView,
    SupplierCreateView,
    SupplierDeleteView,
    SupplierDetailView,
    SupplierListView,
    SupplierUpdateView,
    DeleteSelectedConsumableView,
    InventoryCreateWithPKView,
    DeleteSelectedSupplierView,
    DeleteSelectedCategoryView,
)

app_name = "consumable"


urlpatterns = [
    # CONSUMABLE URLS...
    path("list/", ConsumableListView.as_view(), name="list"),
    path("detail/<int:pk>/", ConsumableDetailView.as_view(), name="detail"),
    path("create/", ConsumableCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ConsumableUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ConsumableDeleteView.as_view(), name="delete"),
    path(
        "delete/",
        DeleteSelectedConsumableView.as_view(),
        name="delete_selected_consumable",
    ),
    # INVENTORY URLS...
    path(
        "inventory_detail/<int:pk>/",
        InventoryDetailView.as_view(),
        name="inventory_detail",
    ),
    path(
        "create/<int:pk>/",
        InventoryCreateWithPKView.as_view(),
        name="inventory_create_with_pk",
    ),
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
    path(
        "category/delete/",
        DeleteSelectedCategoryView.as_view(),
        name="delete_selected_category",
    ),
    # SUPPLIERS URLS
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
    path(
        "supplier/delete/",
        DeleteSelectedSupplierView.as_view(),
        name="delete_selected_supplier",
    ),
]
