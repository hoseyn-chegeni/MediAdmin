from django.urls import path
from .views import (
    ServiceCreateView,
    ServiceDetailView,
    ServiceLDeleteView,
    ServiceListView,
    ServiceUpdateView,
    ServiceConsumableCreateView,
    ServiceConsumableDeleteView,
    SuspendServiceView,
    ReactiveServiceView,
    ServiceAppointmentConfigView,
    WaitingQueueView,
    ServiceCategoryCreateView,
    ServiceCategoryDeleteView,
    ServiceCategoryDetailView,
    ServiceCategoryListView,
    ServiceCategoryUpdateView,
    SuspendServiceCategoryView,
    ReactiveServiceCategoryView,
    PackageCreateView,
    PackageDeleteView,
    PackageDetailView,
    PackageListView,
    PackageUpdateView,
    SuspendPackageView,
    ReactivePackageView,
    ServicePackageCreateView,
    ServicePackageUpdateView,
    ServicePackageDeleteView,
    UpdateServicePricesView,
    DeleteSelectedServicesView,
    DeleteSelectedPackageView,
    DeleteSelectedServiceCategoryView,
    ServiceCreateWithDocIDView,
)

app_name = "services"

urlpatterns = [
    path("list/", ServiceListView.as_view(), name="list"),
    path("detail/<int:pk>/", ServiceDetailView.as_view(), name="detail"),
    path("create/", ServiceCreateView.as_view(), name="create"),
    path(
        "create_with_doc_id/<int:pk>/",
        ServiceCreateWithDocIDView.as_view(),
        name="create_with_doc_id",
    ),
    path("update/<int:pk>/", ServiceUpdateView.as_view(), name="update"),
    path(
        "appointment_config/<int:pk>/",
        ServiceAppointmentConfigView.as_view(),
        name="appointment_config",
    ),
    path("delete/<int:pk>/", ServiceLDeleteView.as_view(), name="delete"),
    path(
        "create_service_consumable/<int:pk>/",
        ServiceConsumableCreateView.as_view(),
        name="service_consumable_create",
    ),
    path(
        "delete_service_consumable/<int:pk>/",
        ServiceConsumableDeleteView.as_view(),
        name="service_consumable_delete",
    ),
    path("suspend/<int:pk>/", SuspendServiceView.as_view(), name="suspend"),
    path("reactive/<int:pk>/", ReactiveServiceView.as_view(), name="reactive"),
    path(
        "<int:service_id>/receptions/",
        WaitingQueueView.as_view(),
        name="queue",
    ),
    path(
        "delete/", DeleteSelectedServicesView.as_view(), name="delete_selected_services"
    ),
    # SERVICE CATEGORY URLS.
    path("category/list/", ServiceCategoryListView.as_view(), name="category_list"),
    path(
        "category_detail/<int:pk>/",
        ServiceCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "category/create/", ServiceCategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/update/<int:pk>/",
        ServiceCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category/delete/<int:pk>/",
        ServiceCategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path(
        "category_suspend/<int:pk>/",
        SuspendServiceCategoryView.as_view(),
        name="category_suspend",
    ),
    path(
        "category/reactive/<int:pk>/",
        ReactiveServiceCategoryView.as_view(),
        name="category_reactive",
    ),
    path(
        "category/delete/",
        DeleteSelectedServiceCategoryView.as_view(),
        name="delete_selected_category",
    ),
    # PACKAGE URLS.
    path("package_list/", PackageListView.as_view(), name="package_list"),
    path(
        "package_detail/<int:pk>/", PackageDetailView.as_view(), name="package_detail"
    ),
    path("package_create/", PackageCreateView.as_view(), name="package_create"),
    path(
        "package_update/<int:pk>/", PackageUpdateView.as_view(), name="package_update"
    ),
    path(
        "package_delete/<int:pk>/", PackageDeleteView.as_view(), name="package_delete"
    ),
    path(
        "package_suspend/<int:pk>/",
        SuspendPackageView.as_view(),
        name="package_suspend",
    ),
    path(
        "package_reactive/<int:pk>/",
        ReactivePackageView.as_view(),
        name="package_reactive",
    ),
    path(
        "package/delete/",
        DeleteSelectedPackageView.as_view(),
        name="delete_selected_package",
    ),
    # PACKAGE STEPS URLS.
    path(
        "package/<int:pk>/add_service/",
        ServicePackageCreateView.as_view(),
        name="add_service_to_package",
    ),
    path(
        "package/<int:pk>/update_service/",
        ServicePackageUpdateView.as_view(),
        name="update_service_package",
    ),
    path(
        "package/<int:pk>/delete_service/",
        ServicePackageDeleteView.as_view(),
        name="delete_service_from_package",
    ),
    # Update Service Price
    path(
        "update-service-prices/",
        UpdateServicePricesView.as_view(),
        name="update_service_prices",
    ),
]
