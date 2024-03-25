from django.shortcuts import render
from base.views import BaseListView, BaseDetailView,BaseDeleteView
from logs.models import ClientSMSLog
from .forms import SMSSendForm, BulkSMSSendForm
from logs.models import ClientSMSLog
from kavenegar import *
from os import getenv
from django.views.generic import FormView
from django.urls import reverse_lazy
from client.models import Client
import re


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
    




class BulkSMSSendView(FormView):
    template_name = 'notification/send_bulk_sms.html'
    form_class = BulkSMSSendForm
    success_url = reverse_lazy('notification:sms_list')

    def form_valid(self, form):
        try:
            api = KavenegarAPI(getenv("KAVENEGAR_API_KEY"))
            clients = []
            for i in form.cleaned_data['clients']:
                clients.append(str(i.phone_number))
            message = form.cleaned_data['message']
            sender = "2000500666"  # optional
            for client in clients:
                params = {
                    "sender": sender,
                    "receptor": clients,
                    "message": message,
                }
                response = api.sms_send(params)
                for i in clients:
                    ClientSMSLog.objects.create(
                        client=clients,
                        sender_number=sender,
                        receiver_number=i.phone_number,
                        subject="اطلاع رسانی پذیرش",
                        message_body=message,
                        status=response["status"],
                        response=response,
                    )
        except (APIException, HTTPException) as e:
            print(e)
            for i in form.cleaned_data['clients']:
                ClientSMSLog.objects.create(
                    client=i,
                    sender_number=sender,
                    receiver_number=i.phone_number,
                    subject="اطلاع رسانی پذیرش",
                    message_body=message,
                    status="Field",
                    response=e,
            )
        return super().form_valid(form)