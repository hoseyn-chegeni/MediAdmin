from django.shortcuts import redirect, get_object_or_404
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseListView,
    BaseDetailView,
    BaseUpdateView,
)
from django.views.generic import ListView, DeleteView
from .models import Client, ClientGallery, ClientAttachment
from .filters import (
    ClientFilters,
    ClientReceptionHistoryFilter,
    ClientFinancialHistoryFilter,
    ClientAttachmentsFilter,
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
from planner.models import Session, DeletedSession
from logs.models import ClientSMSLog
from notification.filters import ClientSMSLogFilter
from planner.models import Session
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count
from .forms import (
    ClientCreateForm,
    ClientUpdateForm,
    EditHealthHistoryForm,
    ClientCreateFromSessionForm,
    ClientGalleryUpdateForm,
    ClientGalleryCreateForm,
    ClientAttachmentCreateForm,
    ClientAttachmentUpdateForm,
)


# Create your views here.
class ClientListView(BaseListView):
    model = Client
    template_name = "client/list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters
    permission_required = "client.view_client"


class ClientCreateView(BaseCreateView):
    model = Client
    form_class = ClientCreateForm
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
    form_class = ClientUpdateForm
    template_name = "client/update.html"
    app_name = "client"
    url_name = "detail"
    permission_required = "client.change_client"


class EditHealthHistoryView(BaseUpdateView):
    model = Client
    template_name = "client/edit_health_history.html"
    form_class = EditHealthHistoryForm
    app_name = "client"
    url_name = "detail"
    permission_required = "client.change_client"


class VipButtonView(SuccessMessageMixin, View):
    success_message = "تغییر وضعیت بیمار به حالت ویژه موفقیت آمیز بود"

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
        context["deleted_session"] = DeletedSession.objects.filter(
            client_id=self.kwargs["pk"]
        )

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
            delete_client_count = Client.objects.filter(
                id__in=client_ids
            ).delete()  # Delete selected users
            messages.success(
                request, f"تعداد {delete_client_count[0]} بیمار با موفقیت حذف شدند."
            )
        return redirect("client:list")


class CreateClintFromSessionView(BaseCreateView):
    model = Client
    form_class = ClientCreateFromSessionForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session"] = Session.objects.get(id=self.kwargs["pk"])
        return context


# CLIENT PHOTO GALLERY
# CLIENT PHOTO GALLERY
# CLIENT PHOTO GALLERY
# CLIENT PHOTO GALLERY
# CLIENT PHOTO GALLERY
# CLIENT PHOTO GALLERY
# CLIENT PHOTO GALLERY


class ClientGalleryListView(ListView):
    model = ClientGallery
    template_name = "client/gallery/list.html"
    context_object_name = "images"
    permission_required = "client.view_client"

    def get_queryset(self):
        return ClientGallery.objects.filter(client_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context


class ClientGalleryCreateView(BaseCreateView):
    model = ClientGallery
    form_class = ClientGalleryCreateForm
    template_name = "client/gallery/create.html"
    permission_required = "client.add_client"

    def get_success_url(self):
        return reverse_lazy(f"client:gallery_list", kwargs={"pk": self.kwargs["pk"]})

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
    form_class = ClientGalleryUpdateForm
    template_name = "client/gallery/update.html"
    permission_required = "client.change_client"

    def get_success_url(self):
        return reverse_lazy(
            f"client:gallery_list", kwargs={"pk": self.kwargs["client_pk"]}
        )


class DeleteSelectedImagesView(View):
    def post(self, request, client_id):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "image_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = ClientGallery.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request, f"تعداد {deleted_users_count[0]} تصویر با موفقیت حذف شدند."
            )  # Add success message
        return redirect(
            reverse_lazy("client:gallery_list", kwargs={"pk": self.kwargs["client_id"]})
        )


# CLIENT ATTACHMENTS
# CLIENT ATTACHMENTS
# CLIENT ATTACHMENTS
# CLIENT ATTACHMENTS
# CLIENT ATTACHMENTS
# CLIENT ATTACHMENTS
# CLIENT ATTACHMENTS


class ClientAttachmentListView(BaseListView):
    model = ClientAttachment
    template_name = "client/attachment/list.html"
    context_object_name = "attachments"
    permission_required = "client.view_client"
    filterset_class = ClientAttachmentsFilter

    def get_queryset(self):
        return ClientAttachment.objects.filter(client_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context


class ClientAttachmentCreateView(BaseCreateView):
    model = ClientAttachment
    form_class = ClientAttachmentCreateForm
    template_name = "client/attachment/create.html"
    permission_required = "client.add_client"
    app_name = "client"
    url_name = "attachment_detail"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.client = Client.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.get(id=self.kwargs["pk"])
        return context

    def get_success_url(self):
        client = Client.objects.get(id=self.kwargs["pk"])
        return reverse_lazy("client:attachment_list", kwargs={"pk": client.id})


class ClientAttachmentUpdateView(BaseUpdateView):
    model = ClientAttachment
    form_class = ClientAttachmentUpdateForm
    template_name = "client/attachment/update.html"
    permission_required = "client.change_client"

    def get_success_url(self):
        attachment = self.get_object()
        return reverse_lazy(
            "client:attachment_list", kwargs={"pk": attachment.client.pk}
        )


class ClientAttachmentDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    message = "با موفقیت از سیستم حذف شد"
    permission_required = "client.view_client"
    model = ClientAttachment

    def get(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()

        # Perform the delete operation directly without displaying a confirmation template

        self.object.delete()
        messages.success(self.request, self.message)
        client_id = self.object.client.id  # Assuming self.object is the model instance
        url = reverse("client:attachment_list", kwargs={"pk": client_id})
        return HttpResponseRedirect(url)


class DeleteSelectedAttachmentsView(View):
    def post(self, request, client_id):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "attachment_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = ClientAttachment.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request, f"تعداد {deleted_users_count[0]} سند با موفقیت حذف شدند."
            )  # Add success message
        return redirect(
            reverse_lazy(
                "client:attachment_list", kwargs={"pk": self.kwargs["client_id"]}
            )
        )


#############################
#############################
#############################
######## REPORT LIST ########
#############################
#############################
#############################


class NewClientListView(BaseListView):
    model = Client
    template_name = "client/reports/new_list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters
    permission_required = "client.view_client"

    def get_queryset(self):
        one_month_ago = now() - timedelta(days=30)
        return super().get_queryset().filter(created_at__gte=one_month_ago)


class FollowUpClientListView(BaseListView):
    model = Client
    template_name = "client/reports/follow_up_list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters
    permission_required = "client.view_client"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(reception_count=Count("reception"))
            .filter(reception_count__gte=2)
        )


class SingleReceptionClientListView(BaseListView):
    model = Client
    template_name = "client/reports/single_reception_list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters
    permission_required = "client.view_client"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(reception_count=Count("reception"))
            .filter(reception_count__lte=1)
        )


class HighRiskClientListView(BaseListView):
    model = Client
    template_name = "client/reports/high_risk_list.html"
    context_object_name = "clients"
    filterset_class = ClientFilters
    permission_required = "client.view_client"

    def get_queryset(self):
        return super().get_queryset().exclude(high_risk__isnull=True)
