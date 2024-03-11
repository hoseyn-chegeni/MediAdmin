from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseDetailView,
    BaseUpdateView,
)
from .models import Client
from .filters import ClientFilters, ReceptionFilter, FinancialFilter
from django.urls import reverse_lazy, reverse
from reception.models import Reception
from prescription.models import Prescription
from financial.models import Financial
from django.db.models import Sum
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# Create your views here.
class ClientListView(BaseListView):
    model = Client
    template_name = "client/list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters


class ClientCreateView(BaseCreateView):
    model = Client
    fields = "__all__"
    template_name = "client/create.html"
    app_name = "client"
    url_name = "detail"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClientDetailView(BaseDetailView):
    model = Client
    template_name = "client/detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        client = self.get_object()
        context = super().get_context_data(**kwargs)

        # Get reception history for the client
        context["reception_history"] = Reception.objects.filter(
            client_id=client.id
        ).order_by("-created_at")[:5]
        context["num_reception"] = Reception.objects.filter(client_id=client.id).count()

        # Get all prescriptions associated with the receptions
        context["num_prescriptions"] = Prescription.objects.filter(
            reception__client_id=client.id
        ).count()

        context["financial_instances"] = Financial.objects.filter(
            reception__client=client
        ).order_by("-created_at")[:5]
        context["num_financial_instances"] = Financial.objects.filter(
            reception__client=client
        ).count()

        total_amount_sum = Financial.objects.filter(reception__client=client).aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        context["total_amount_sum"] = total_amount_sum
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


class VipButtonView(SuccessMessageMixin, View):
    success_message = "تغییر وضغیت بیمار به حالت ویژه موفقیت آمیز بود"

    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        if client:
            client.is_vip = True
            client.save()
            messages.success(self.request, self.success_message)
        # Construct the URL for the client detail page
        client_detail_url = reverse("client:detail", kwargs={"pk": pk})
        return HttpResponseRedirect(client_detail_url)


class RemoveVipButtonView(View):
    success_message = "بیمار از حالت بیماران ویژه خارج شد"

    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        if client:
            client.is_vip = False
            client.save()
            messages.success(self.request, self.success_message)
        # Construct the URL for the client detail page
        client_detail_url = reverse("client:detail", kwargs={"pk": pk})
        return HttpResponseRedirect(client_detail_url)


class ClientReceptionsListView(BaseListView):
    model = Reception
    template_name = "client/client_receptions.html"
    filterset_class = ReceptionFilter

    def get_queryset(self):
        client_id = self.kwargs["pk"]
        return Reception.objects.filter(client_id=client_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get reception history for the client
        context["client"] = Client.objects.get(id=self.kwargs["pk"])

        return context


class ClientFinancialInstancesListView(BaseListView):
    model = Financial
    template_name = "client/client_financial.html"
    filterset_class = FinancialFilter

    def get_queryset(self):
        client_id = self.kwargs["pk"]
        return Financial.objects.filter(reception__client_id=client_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context
