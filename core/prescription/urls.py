from django.urls import path
from .views import (
    PrescriptionHeaderCreateView,
    PrescriptionHeaderUpdateView,
    PrescriptionCreateView,
    PrescriptionDeleteView,
    PrescriptionDetailView,
    PrescriptionUpdateView,
    PrescriptionListView,
    PrescriptionCreateWithoutPkView,
    PrescriptionItemUpdateView,
    PrescriptionItemDeleteView,
    TemporaryPrescriptionDetailView,
    CreateTemporaryPrescription,
    save_prescription,
)


app_name = "prescription"

urlpatterns = [
    path("list/", PrescriptionListView.as_view(), name="list"),
    path("create/", PrescriptionCreateWithoutPkView.as_view(), name="create_no_pk"),
    path("detail/<int:pk>/", PrescriptionDetailView.as_view(), name="detail"),
    path("create/<int:pk>/", PrescriptionCreateView.as_view(), name="create"),
    path("update/<int:pk>/", PrescriptionUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", PrescriptionDeleteView.as_view(), name="delete"),
    # Prescription Header Urls
    path(
        "create/<int:pk>/",
        PrescriptionHeaderCreateView.as_view(),
        name="header_create",
    ),
    path(
        "update/<int:pk>/", PrescriptionHeaderUpdateView.as_view(), name="header_update"
    ),
    path(
        "item/update/<int:pk>/",
        PrescriptionItemUpdateView.as_view(),
        name="item_update",
    ),
    path(
        "item/delete/<int:pk>/",
        PrescriptionItemDeleteView.as_view(),
        name="item_delete",
    ),
    path(
        "temp_detail/<int:pk>/",
        TemporaryPrescriptionDetailView.as_view(),
        name="temp_detail",
    ),
    path("prescription/save/<int:pk>/", save_prescription, name="save"),
    path('create_temp_prescription/<int:reception_id>/', CreateTemporaryPrescription.as_view(), name='create_temp_prescription'),

]
