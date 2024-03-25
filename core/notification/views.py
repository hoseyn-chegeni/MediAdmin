from django.shortcuts import render
from base.views import BaseListView, BaseDetailView,BaseDeleteView
from logs.models import ClientSMSLog

# Create your views here.
class ClientSMSListView(BaseListView):
    model = ClientSMSLog
    template_name = "notification/list.html"
    context_object_name = "sms"
    filterset_class = 0
    permission_required = "logs.view_ClientSMSLog"


class ClientSMSDetailView(BaseDetailView):
    model = ClientSMSLog
    template_name = "notification/detail.html"
    context_object_name = "sms"
    permission_required = "logs.view_ClientSMSLog"

class ClientSMSDeleteView(BaseDeleteView):
    model = ClientSMSLog
    app_name = "notification"
    url_name = "sms_list"
    permission_required ="logs.delete_ClientSMSLog"
