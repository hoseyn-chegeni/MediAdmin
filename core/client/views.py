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
    app_name = "client"


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
    app_name = "client"


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
