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
]
