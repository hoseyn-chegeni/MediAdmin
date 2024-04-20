from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    EditPersonalInfoView,
    EditHealthHistoryView,
    VipButtonView,
    RemoveVipButtonView,
    ClientReceptionsHistoryListView,
    ClientFinancialInstancesListView,
    ClientAppointmentListView,
    ClientSMSListView,
    DeleteSelectedClientView,
    ClientNationalIdSearchView,
    ClientCaseIdSearchView,
)

app_name = "client"

urlpatterns = [
    path("list/", ClientListView.as_view(), name="list"),
    path("detail/<int:pk>/", ClientDetailView.as_view(), name="detail"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("update/<int:pk>/", EditPersonalInfoView.as_view(), name="update"),
    path(
        "edit_health_history/<int:pk>/",
        EditHealthHistoryView.as_view(),
        name="edit_health_history",
    ),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete"),
    path("vip/<int:pk>/", VipButtonView.as_view(), name="vip"),
    path("remove_vip/<int:pk>/", RemoveVipButtonView.as_view(), name="remove_vip"),
    path(
        "client/<int:pk>/receptions/",
        ClientReceptionsHistoryListView.as_view(),
        name="client-receptions",
    ),
    path(
        "client/<int:pk>/financial/",
        ClientFinancialInstancesListView.as_view(),
        name="client-financial",
    ),
    path(
        "client/<int:pk>/appointment/",
        ClientAppointmentListView.as_view(),
        name="client-appointment",
    ),
    path(
        "client/<int:pk>/sms_log/",
        ClientSMSListView.as_view(),
        name="client-sms_log",
    ),
    path("delete/", DeleteSelectedClientView.as_view(), name="delete_selected_clients"),
    path(
        "national_id/search/",
        ClientNationalIdSearchView.as_view(),
        name="national_id_search",
    ),
    path("case_id/search/", ClientCaseIdSearchView.as_view(), name="case_id_search"),
]
