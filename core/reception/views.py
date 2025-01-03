from django.shortcuts import redirect
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
from kavenegar import *
from tasks.models import Task
from planner.models import Session, JalaliDateHandler
from prescription.models import TemporaryPrescription, Prescription
from datetime import date
from .forms import ReceptionCreateForm,ReceptionUpdateForm, ReceptionWithClientIDCreateForm

# Create your views here.
class ReceptionListView(BaseListView):
    model = Reception
    template_name = "reception/list.html"
    context_object_name = "reception"
    filterset_class = ReceptionFilter
    permission_required = "reception.view_reception"


class ReceptionCreateView(BaseCreateView):
    model = Reception
    form_class = ReceptionCreateForm
    template_name = "reception/create.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.add_reception"

    def form_valid(self, form):
        # Set the client for the reception
        jalali = JalaliDateHandler.objects.get(date=date.today())
        form.instance.created_by = self.request.user
        form.instance.status = "WAITE"
        service = form.instance.service
        form.instance.jalali_date = jalali.jalali_date
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

        if TemporaryPrescription.objects.filter(reception_id=reception.id).exists():
            context["temp_prescription"] = TemporaryPrescription.objects.get(
                reception_id=reception.id
            )
        else:
            context["temp_prescription"] = None

        if Prescription.objects.filter(reception_id=reception.id).exists():
            context["prescription"] = Prescription.objects.get(
                reception_id=reception.id
            )
        else:
            context["prescription"] = None

        return context


class ReceptionCreateViewUsingProfile(BaseCreateView):
    model = Reception
    form_class = ReceptionWithClientIDCreateForm
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
        form.instance.client = Client.objects.get(id=self.kwargs["pk"])
        jalali = JalaliDateHandler.objects.get(date=date.today())
        form.instance.created_by = self.request.user
        form.instance.status = "WAITE"
        service = form.instance.service
        form.instance.jalali_date = jalali.jalali_date
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
    form_class = ReceptionUpdateForm
    template_name = "reception/update.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.change_reception"


class ReceptionWithSessionCreateView(BaseCreateView):
    model = Reception
    fields = ["reason", "payment_type", "payment_status"]
    template_name = "reception/create_with_appointment.html"
    app_name = "reception"
    url_name = "detail"
    permission_required = "reception.add_reception"

    def form_valid(self, form):
        session = Session.objects.get(id=self.kwargs["pk"])
        # Set the client for the reception
        form.instance.created_by = self.request.user
        form.instance.status = "WAITE"
        form.instance.client = session.client
        form.instance.service = session.service
        form.instance.session = session
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = Session.objects.get(id=self.kwargs["pk"])
        context["client"] = Client.objects.get(id=session.client.id)
        return context


class DeleteSelectedReceptionView(View):
    def post(self, request):
        if request.method == "POST":
            reception_ids = request.POST.getlist(
                "reception_ids"
            )  # Get the list of selected user IDs from the form
            Reception.objects.filter(
                id__in=reception_ids
            ).delete()  # Delete selected users
        return redirect("reception:list")
