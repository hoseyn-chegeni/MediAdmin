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

    def get_success_url(self):
        return reverse_lazy("client:detail", kwargs={"pk": self.object.pk})


class ClientDetailView(BaseDetailView):
    model = Client
    template_name = "client/detail.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        client = self.get_object()
        context = super().get_context_data(**kwargs)
        context["reception_history"] = Reception.objects.filter(client_id=client.id)
        return context


class ClientDeleteView(BaseDeleteView):
    model = Client
    template_name = "client/delete.html"
    success_url = reverse_lazy("client:list")


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
    ]
    template_name = "client/update.html"

    def get_success_url(self):
        return reverse_lazy("client:detail", kwargs={"pk": self.object.pk})


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

    def get_success_url(self):
        return reverse_lazy("client:detail", kwargs={"pk": self.object.pk})
