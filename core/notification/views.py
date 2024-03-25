from django.shortcuts import render
from base.views import BaseListView, BaseDetailView,BaseDeleteView
from logs.models import ClientSMSLog
from .forms import SMSSendForm
from logs.models import ClientSMSLog
from kavenegar import *
from os import getenv
from django.views.generic import FormView
from django.urls import reverse_lazy
from client.models import Client


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




class SMSSendView(FormView):
    template_name = 'notification/send_sms.html'
    form_class = SMSSendForm
    success_url = reverse_lazy('notification:sms_list')

    def form_valid(self, form):
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            client = Client.objects.get(id = self.kwargs['pk'])
            message = form.cleaned_data['message']
            params = {
                "sender": "2000500666",  # optional
                "receptor": client.phone_number,  # assuming the phone_number field exists in your Client model
                "message": message,
            }
            response = api.sms_send(params)
            ClientSMSLog.objects.create(
                client=client,
                sender_number=params["sender"],
                receiver_number=params["receptor"],
                subject="اطلاع رسانی پذیرش",
                message_body=message,
                status=response["status"],
                response=response,
            )
        except (APIException, HTTPException) as e:
            # Handle exceptions
            ClientSMSLog.objects.create(
            client=client,
            sender_number=params["sender"],
            receiver_number=params["receptor"],
            subject="اطلاع رسانی پذیرش",
            message_body=message,
            status="Field",
            response=e,
            )
        return super().form_valid(form)