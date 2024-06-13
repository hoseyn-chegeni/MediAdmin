from django.shortcuts import render, redirect
from .models import Doctor
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .filters import DoctorFilter
from prescription.models import PrescriptionHeader
from services.models import Service
from financial.models import Financial
from reception.models import Reception
from django.db.models import Sum
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count
from reception.filters import ReceptionFilter
from services.filters import ServicesFilter
from django.utils.timezone import now
from datetime import timedelta
from .forms import DoctorCreateForm,DoctorUpdateForm

# Create your views here.
class DoctorListView(BaseListView):
    model = Doctor
    template_name = "doctor/list.html"
    context_object_name = "doctor"
    filterset_class = DoctorFilter
    permission_required = "doctor.view_doctor"


class DoctorDetailView(BaseDetailView):
    model = Doctor
    template_name = "doctor/detail.html"
    context_object_name = "doctor"
    permission_required = "doctor.view_doctor"

    def get_context_data(self, **kwargs):
        doctor = self.get_object()
        context = super().get_context_data(**kwargs)

        context["service"] = Service.objects.filter(doctor_id=doctor.id).order_by(
            "-created_at"
        )[:5]
        context["num_service"] = Service.objects.filter(doctor_id=doctor.id).count()

        context["receptions"] = Reception.objects.filter(
            service__doctor=doctor
        ).order_by("-created_at")[:5]
        context["num_receptions"] = Reception.objects.filter(
            service__doctor=doctor
        ).count()

        # Try to get the prescription header for the doctor
        prescription_header = PrescriptionHeader.objects.filter(
            doctor_id=doctor.id
        ).first()
        if prescription_header is not None:
            context["prescription"] = prescription_header
        else:
            context["prescription"] = None

        # Calculate total wage of the doctor
        total_wage = (
            Financial.objects.filter(doctor=doctor).aggregate(Sum("doctors_wage"))[
                "doctors_wage__sum"
            ]
            or 0
        )
        context["total_wage"] = total_wage

        service_with_most_receptions = (
            doctor.service_set.annotate(reception_count=Count("reception"))
            .order_by("-reception_count")
            .first()
        )

        context["service_with_most_receptions"] = service_with_most_receptions
        return context


class DoctorCreateView( BaseCreateView):
    model = Doctor
    form_class = DoctorCreateForm
    template_name = "doctor/create.html"
    permission_required = "doctor.add_doctor"
    app_name = "doctor"
    url_name = "detail"
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DoctorUpdateView(BaseUpdateView):
    model = Doctor
    form_class = DoctorUpdateForm
    template_name = "doctor/update.html"
    app_name = "doctor"
    url_name = "detail"
    permission_required = "doctor.change_doctor"


class DoctorDeleteView(BaseDeleteView):
    model = Doctor
    app_name = "doctor"
    url_name = "list"
    permission_required = "doctor.delete_doctor"


class SuspendDoctorView(View):
    def get(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        if doctor:
            doctor.is_active = False
            messages.success(self.request, f"پزشک {doctor.get_full_name()} غیرفعال شد")
            doctor.save()
        return HttpResponseRedirect(
            reverse_lazy("doctor:detail", kwargs={"pk": doctor.pk})
        )


class ReactiveDoctorView(View):
    def get(self, request, pk):
        doctor = Doctor.objects.filter(pk=pk).first()
        if doctor:
            doctor.is_active = True
            messages.success(
                self.request, f"پزشک {doctor.get_full_name()} مجددا فعال شد "
            )
            doctor.save()
        return HttpResponseRedirect(
            reverse_lazy("doctor:detail", kwargs={"pk": doctor.pk})
        )


class DoctorReceptionHistoryListView(BaseListView):
    model = Reception
    context_object_name = "reception"
    template_name = "doctor/reception_history.html"
    permission_required = "doctor.view_doctor"
    filterset_class = ReceptionFilter

    def get_queryset(self):
        doctor_id = self.kwargs["pk"]
        return Reception.objects.filter(service__doctor_id=doctor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.get(id=self.kwargs["pk"])
        return context


class DoctorServicesListView(BaseListView):
    model = Service
    context_object_name = "services"
    template_name = "doctor/service.html"
    permission_required = "doctor.view_doctor"
    filterset_class = ServicesFilter

    def get_queryset(self):
        doctor_id = self.kwargs["pk"]
        return Service.objects.filter(doctor_id=doctor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.get(id=self.kwargs["pk"])
        return context


class DeleteSelectedDoctorsView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "doctor_ids"
            )  # Get the list of selected user IDs from the form
            Doctor.objects.filter(id__in=user_ids).delete()  # Delete selected users
        return redirect("doctor:list")


#############################
#############################
#############################
######## REPORT LIST ########
#############################
#############################
#############################


class NewDoctorsListView(BaseListView):
    model = Doctor
    template_name = "doctor/reports/new_list.html"
    context_object_name = "doctor"
    filterset_class = DoctorFilter
    permission_required = "doctor.view_doctor"

    def get_queryset(self):
        one_month_ago = now() - timedelta(days=30)
        return super().get_queryset().filter(created_at__gte=one_month_ago)
