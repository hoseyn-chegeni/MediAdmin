from django.urls import path
from .views import (
    ConsumableCreateView,
    ConsumableDeleteView,
    ConsumableDetailView,
    ConsumableListView,
    ConsumableUpdateView,
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
)

app_name = "asset"

urlpatterns = [
    path("consumable/list/", ConsumableListView.as_view(), name="list"),
    path("consumable/detail/<int:pk>/", ConsumableDetailView.as_view(), name="detail"),
    path("consumable/create/", ConsumableCreateView.as_view(), name="create"),
    path("consumable/update/<int:pk>/", ConsumableUpdateView.as_view(), name="update"),
    path("consumable/delete/<int:pk>/", ConsumableDeleteView.as_view(), name="delete"),
    # CONSUMABLE CATEGORY
    path(
        "consumable/category/list/",
        ConsumableCategoryListView.as_view(),
        name="category_list",
    ),
    path(
        "consumable/category/detail/<int:pk>/",
        ConsumableCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "consumable/category/create/",
        ConsumableCategoryCreateView.as_view(),
        name="category_create",
    ),
    path(
        "consumable/category/update/<int:pk>/",
        ConsumableCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "consumable/category/delete/<int:pk>/",
        ConsumableCategoryDeleteView.as_view(),
        name="category_delete",
    ),
    #SUPPLIER
    path("supplier/list/", SupplierListView.as_view(), name="supplier_list"),
    path("supplier/detail/<int:pk>/", SupplierDetailView.as_view(), name="supplier_detail"),
    path("supplier/create/", SupplierCreateView.as_view(), name="supplier_create"),
    path("supplier/update/<int:pk>/", SupplierUpdateView.as_view(), name="supplier_update"),
    path("supplier/delete/<int:pk>/", SupplierDeleteView.as_view(), name="supplier_delete"),
]
