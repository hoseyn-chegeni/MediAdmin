from django.urls import path 
from .views import ClientSMSDeleteView,ClientSMSDetailView, ClientSMSListView

app_name = 'notification'

urlpatterns = [ 
    path("sms_list/", ClientSMSListView.as_view(), name="sms_list"),
    path("sms_detail/<int:pk>/", ClientSMSDetailView.as_view(), name="sms_detail"),
    path("sms_delete/<int:pk>/", ClientSMSDeleteView.as_view(), name="sms_delete"),
]