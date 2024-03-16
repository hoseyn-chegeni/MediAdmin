from django.urls import path
from .views import (
    ServiceCreateView,
    ServiceDetailView,
    ServiceLDeleteView,
    ServiceListView,
    ServiceUpdateView,
    ServiceConsumableCreateView,
    ServiceConsumableDeleteView,
    SuspendServiceListView,
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
)

app_name = "services"

urlpatterns = [
    path("list/", ServiceListView.as_view(), name="list"),
    path("suspend_list/", SuspendServiceListView.as_view(), name="suspend_list"),
    path("detail/<int:pk>/", ServiceDetailView.as_view(), name="detail"),
    path("create/", ServiceCreateView.as_view(), name="create"),
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
        "services/<int:service_id>/receptions/",
        WaitingQueueView.as_view(),
        name="queue",
    ),
    # SERVICE CATEGORY URLS.
    path("category_list/", ServiceCategoryListView.as_view(), name="category_list"),
    path(
        "category_detail/<int:pk>/",
        ServiceCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "category_create/", ServiceCategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category_update/<int:pk>/",
        ServiceCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category_delete/<int:pk>/",
        ServiceCategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path(
        "category_suspend/<int:pk>/",
        SuspendServiceCategoryView.as_view(),
        name="category_suspend",
    ),
    path(
        "category_reactive/<int:pk>/",
        ReactiveServiceCategoryView.as_view(),
        name="category_reactive",
    ),
]
