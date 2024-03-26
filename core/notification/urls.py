from django.urls import path
from .views import (
    ClientSMSDeleteView,
    ClientSMSDetailView,
    ClientSMSListView,
    SMSSendView,
    BulkSMSSendView,
)

app_name = "notification"

urlpatterns = [
    path("sms_list/", ClientSMSListView.as_view(), name="sms_list"),
    path("sms_detail/<int:pk>/", ClientSMSDetailView.as_view(), name="sms_detail"),
    path("sms_delete/<int:pk>/", ClientSMSDeleteView.as_view(), name="sms_delete"),
    path("send_sms/<int:pk>/", SMSSendView.as_view(), name="send_sms"),
    path("send_bulk/", BulkSMSSendView.as_view(), name="send_bulk_sms"),
]
