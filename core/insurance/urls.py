from django.urls import path
from .views import (
    InsuranceCreateView,
    InsuranceDetailView,
    InsuranceListView,
    InsuranceDeleteView,
    InsuranceUpdateView,
    ServiceInsuranceCreateView,
    ServiceInsuranceDeleteView,
    ServiceInsuranceDetailView,
    ServiceInsuranceUpdateView,
    ServiceInsuranceListView,
    DeleteSelectedInsuranceView
)

app_name = "insurance"

urlpatterns = [
    path("list/", InsuranceListView.as_view(), name="list"),
    path("detail/<int:pk>/", InsuranceDetailView.as_view(), name="detail"),
    path("create/", InsuranceCreateView.as_view(), name="create"),
    path("update/<int:pk>/", InsuranceUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", InsuranceDeleteView.as_view(), name="delete"),
    path("delete/", DeleteSelectedInsuranceView.as_view(), name="delete_selected_insurance"),

    # SERVICE INSURANCE
    path(
        "service_insurance_list/",
        ServiceInsuranceListView.as_view(),
        name="service_insurance_list",
    ),
    path(
        "service_insurance_detail/<int:pk>/",
        ServiceInsuranceDetailView.as_view(),
        name="service_insurance_detail",
    ),
    path(
        "service_insurance_create/<int:pk>/",
        ServiceInsuranceCreateView.as_view(),
        name="service_insurance_create",
    ),
    path(
        "service_insurance_update/<int:pk>/",
        ServiceInsuranceUpdateView.as_view(),
        name="service_insurance_update",
    ),
    path(
        "service_insurance_delete/<int:pk>/",
        ServiceInsuranceDeleteView.as_view(),
        name="service_insurance_delete",
    ),
]
