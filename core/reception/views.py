from base.views import (
    BaseCreateView,
    BaseListView,
    BaseDetailView,
    BaseDeleteView,
    BaseUpdateView,
)
from .models import Reception
from .filters import ReceptionFilter
from django.urls import reverse_lazy
from client.models import Client
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from booking.models import Appointment
from asset.models import Consumable
from kavenegar import *
from os import getenv
from tasks.models import Task
from consumable.models import Inventory
from financial.models import ConsumablePrice

# Create your views here.
class ReceptionListView(BaseListView):
    model = Reception
    template_name = "reception/list.html"
    context_object_name = "reception"
    filterset_class = ReceptionFilter
    permission_required = "reception.view_reception"


class ReceptionCreateView(BaseCreateView):
    model = Reception
    fields = [
        "reason",
        "payment_type",
        "payment_status",
        "client",
        "service",
        "invoice_attachment",
    ]
    template_name = "reception/create.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.add_reception"

    def form_valid(self, form):
        # Set the client for the reception
        form.instance.created_by = self.request.user
        form.instance.status = "WAITE"
        service = form.instance.service
        if service.check_consumable_inventory == True:
            for i in service.serviceconsumable_set.all():
                if i.consumable.quantity < int(i.dose):
                    Task
                    form.add_error(
                        "service",
                        f"Not enough {i.consumable.name} available for the {service.name} service.",
                    )
                    return super().form_invalid(form)
        return super().form_valid(form)


class ReceptionDetailView(BaseDetailView):
    model = Reception
    template_name = "reception/detail.html"
    context_object_name = "reception"
    permission_required = "reception.view_reception"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reception = self.get_object()
        context["financial"] = reception.financial
        return context


class ReceptionCreateViewUsingProfile(BaseCreateView):
    model = Reception
    fields = ["reason", "payment_type", "payment_status", "service"]
    template_name = "reception/create_profile.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.add_reception"

    def get_initial(self):
        initial = super().get_initial()
        # Set the initial client value to the client whose profile page the user is on
        initial["client"] = self.kwargs[
            "pk"
        ]  # Assuming client's pk is passed in the URL
        return initial

    def form_valid(self, form):
        # Set the client for the reception
        form.instance.created_by = self.request.user
        form.instance.status = "WAITE"
        service = form.instance.service
        if service.check_consumable_inventory == True:
            for i in service.serviceconsumable_set.all():
                if i.consumable.quantity < int(i.dose):
                    Task
                    form.add_error(
                        "service",
                        f"Not enough {i.consumable.name} available for the {service.name} service.",
                    )
                    return super().form_invalid(form)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context


class ReceptionDeleteView(BaseDeleteView):
    model = Reception
    app_name = "reception"
    url_name = "list"
    permission_required = "reception.delete_reception"


class CompleteReceptionView(SuccessMessageMixin, View):
    success_message = "اتمام پذیرش انجام شد."

    def get(self, request, pk):
        reception = Reception.objects.get(pk=pk)
        if reception:
            reception.status = "DONE"
            reception.save()
            messages.success(self.request, self.success_message)
        # Construct the URL for the client detail page
        reception_detail_url = reverse("reception:detail", kwargs={"pk": pk})
        return HttpResponseRedirect(reception_detail_url)


class ReceptionUpdateView(BaseUpdateView):
    model = Reception
    fields = [
        "client",
        "service",
        "reason",
        "payment_type",
        "payment_status",
    ]
    template_name = "reception/update.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.change_reception"


class ReceptionWithAppointmentCreateView(BaseCreateView):
    model = Reception
    fields = ["reason", "payment_type", "payment_status"]
    template_name = "reception/create_with_appointment.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.add_reception"

    def form_valid(self, form):
        appointment = Appointment.objects.get(id=self.kwargs["pk"])
        # Set the client for the reception
        form.instance.created_by = self.request.user
        form.instance.status = "WAITE"
        form.instance.client = appointment.client
        form.instance.service = appointment.service
        form.instance.appointment = appointment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = Appointment.objects.get(id=self.kwargs["pk"])
        context["client"] = Client.objects.get(id=appointment.client.id)
        return context
