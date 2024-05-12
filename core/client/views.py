from django.shortcuts import redirect, get_object_or_404
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseDetailView,
    BaseUpdateView,
)
from django.views.generic import ListView
from .models import Client, ClientGallery
from .filters import (
    ClientFilters,
    ClientReceptionHistoryFilter,
    ClientFinancialHistoryFilter,
)
from django.urls import reverse_lazy, reverse
from reception.models import Reception
from prescription.models import Prescription
from financial.models import Financial
from django.db.models import Sum
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from logs.models import ClientSMSLog
from planner.models import Session
from logs.models import ClientSMSLog
from notification.filters import ClientSMSLogFilter
from planner.models import Session


# Create your views here.
class ClientListView(BaseListView):
    model = Client
    template_name = "client/list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters
    permission_required = "client.view_client"


class ClientCreateView(BaseCreateView):
    model = Client
    fields = "__all__"
    template_name = "client/create.html"
    app_name = "client"
    url_name = "detail"
    permission_required = "client.add_client"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClientDetailView(BaseDetailView):
    model = Client
    template_name = "client/detail.html"
    context_object_name = "client"
    permission_required = "client.view_client"

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

        context["sms"] = ClientSMSLog.objects.filter(client_id=client.id).order_by(
            "-created_at"
        )[:5]
        context["sms_count"] = ClientSMSLog.objects.filter(client_id=client.id).count()
        appointment = Session.objects.filter(client_id=client.id)
        context["appointment"] = appointment.order_by("-created_at")[:5]
        context["appointment_count"] = appointment.count()
        return context


class ClientDeleteView(BaseDeleteView):
    model = Client
    app_name = "client"
    url_name = "list"
    permission_required = "client.delete_client"


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
    permission_required = "client.change_client"


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
    permission_required = "client.change_client"


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


class ClientReceptionsHistoryListView(BaseListView):
    model = Reception
    template_name = "client/client_receptions.html"
    filterset_class = ClientReceptionHistoryFilter
    permission_required = "client.view_client"

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
    filterset_class = ClientFinancialHistoryFilter
    permission_required = "client.view_client"

    def get_queryset(self):
        client_id = self.kwargs["pk"]
        return Financial.objects.filter(reception__client_id=client_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context


class ClientAppointmentListView(BaseListView):
    model = Session
    template_name = "client/client_appointment.html"
    filterset_class = 0
    permission_required = "client.view_client"

    def get_queryset(self):
        client_id = self.kwargs["pk"]
        return Session.objects.filter(client_id=client_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get reception history for the client
        context["client"] = Client.objects.get(id=self.kwargs["pk"])

        return context


class ClientSMSListView(BaseListView):
    model = ClientSMSLog
    template_name = "client/client_sms_log.html"
    filterset_class = ClientSMSLogFilter
    permission_required = "client.view_client"

    def get_queryset(self):
        client_id = self.kwargs["pk"]
        return ClientSMSLog.objects.filter(client_id=client_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context


class DeleteSelectedClientView(View):
    def post(self, request):
        if request.method == "POST":
            client_ids = request.POST.getlist(
                "client_ids"
            )  # Get the list of selected user IDs from the form
            Client.objects.filter(id__in=client_ids).delete()  # Delete selected users
        return redirect("client:list")


class CreateClintFromSessionView(BaseCreateView):
    model = Client
    fields = [
        "case_id",
        "fathers_name",
        "date_of_birth",
        "gender",
        "address",
        "marital_status",
        "emergency_contact_name",
        "emergency_contact_number",
        "surgeries",
        "allergies",
        "medical_history",
        "medications",
        "smoker",
        "disease",
        "insurance",
        "is_vip",
        "image",
    ]
    template_name = "client/create_from_session.html"
    permission_required = "client.add_client"

    def form_valid(self, form):
        session = Session.objects.get(id=self.kwargs["pk"])
        form.instance.first_name = session.first_name
        form.instance.last_name = session.last_name
        form.instance.national_id = session.national_id
        form.instance.phone_number = session.phone_number
        form.instance.initial_session = session
        return super().form_valid(form)

    def get_success_url(self):
        session = Session.objects.get(id=self.kwargs["pk"])
        return reverse_lazy(
            "planner:list",
            kwargs={"service_pk": session.service.id, "day_pk": session.day.id},
        )


class ClientGalleryListView(ListView):
    model = ClientGallery
    template_name = "client/gallery_list.html"
    context_object_name = "images"
    permission_required = "client.view_client"

    def get_queryset(self):
        return ClientGallery.objects.filter(client_id = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context

class ClientGalleryCreateView(BaseCreateView):
    model = ClientGallery
    fields = ['title','image',]
    template_name = "client/add_photo.html"
    permission_required = "client.add_client"


    def get_success_url(self):
        return reverse_lazy(
            f"client:gallery_list", kwargs={"pk": self.kwargs['pk']}
        )

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.client = Client.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context

class ClientGalleryUpdateView(BaseUpdateView):
    model = ClientGallery
    fields = ["title",]
    template_name = "client/update_photo.html"
    permission_required = "client.change_client"
    def get_success_url(self):
        return reverse_lazy(
            f"client:gallery_list", kwargs={"pk": self.kwargs['client_pk']}
        )

class ClientGalleryDeleteView(BaseDeleteView):
    pass