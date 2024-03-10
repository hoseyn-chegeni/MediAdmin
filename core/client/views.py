from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseDetailView,
    BaseUpdateView,
)
from .models import Client
from .filters import ClientFilters
from django.urls import reverse_lazy
from reception.models import Reception
from prescription.models import Prescription
from financial.models import Financial
from django.db.models import Sum
from django.views import View
from django.http import HttpResponseRedirect



# Create your views here.
class ClientListView(BaseListView):
    model = Client
    template_name = "client/list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_vip=False)
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class VipClientListView(BaseListView):
    model = Client
    template_name = "client/vip_list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_vip=True)


class ClientCreateView(BaseCreateView):
    model = Client
    fields = "__all__"
    template_name = "client/create.html"
    app_name = "client"
    url_name = "detail"

    


class ClientDetailView(BaseDetailView):
    model = Client
    template_name = "client/detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        client = self.get_object()
        context = super().get_context_data(**kwargs)

        # Get reception history for the client
        reception_history = Reception.objects.filter(client_id=client.id)
        context["reception_history"] = reception_history
        context["num_reception"] = reception_history.count()

        # Get all prescriptions associated with the receptions
        prescriptions = Prescription.objects.filter(reception__client_id=client.id)
        context["prescriptions"] = prescriptions
        context["num_prescriptions"] = prescriptions.count()

        context["financial_instances"] = Financial.objects.filter(
            reception__client=client
        )
        context["num_financial_instances"] = Financial.objects.filter(
            reception__client=client
        ).count()
        context["total_amount_sum"] = Financial.objects.filter(
            reception__client=client
        ).aggregate(Sum("total_amount"))["total_amount__sum"]

        return context


class ClientDeleteView(BaseDeleteView):
    model = Client
    app_name = "client"
    url_name = "list"


class EditPersonalInfoView(BaseUpdateView):
    model = Client
    fields = [
        "case_id",
        "first_name",
        "last_name",
        "fathers_name",
        "national_id",
        "date_of_birth",
        "gender",
        "phone_number",
        "address",
        "marital_status",
        "emergency_contact_name",
        "emergency_contact_number",
        "insurance",
    ]
    template_name = "client/update.html"
    app_name = "client"
    url_name = "detail"


class EditHealthHistoryView(BaseUpdateView):
    model = Client
    template_name = "client/edit_health_history.html"
    fields = [
        "surgeries",
        "allergies",
        "medical_history",
        "medications",
        "smoker",
        "disease",
    ]
    app_name = "client"
    url_name = "detail"


class VipButtonView(View):
    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        if client:
            client.is_vip = True
            client.save()
        return HttpResponseRedirect(reverse_lazy("client:list"))


class RemoveVipButtonView(View):
    def get(self, request, pk):
        client = Client.objects.filter(pk=pk).first()
        if client:
            client.is_vip = False
            client.save()
        return HttpResponseRedirect(reverse_lazy("client:vip_list"))


class ClientReceptionsListView(BaseListView):
    model = Reception
    template_name = 'client/client_receptions.html'

    def get_queryset(self):
        client_id = self.kwargs['pk']
        return Reception.objects.filter(client_id=client_id)
    
class ClientFinancialInstancesListView(BaseListView):
    model = Financial
    template_name = 'client/client_financial.html'

    def get_queryset(self):
        client_id = self.kwargs['pk']
        return Financial.objects.filter(reception__client_id=client_id)