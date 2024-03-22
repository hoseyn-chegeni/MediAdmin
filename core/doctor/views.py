from django.shortcuts import render
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
        services = Service.objects.filter(doctor_id=doctor.id)
        context["service"] = services
        context["num_service"] = services.count()

        financial_instances = Financial.objects.filter(
            reception__service__doctor=doctor
        )
        context["financial_instances"] = financial_instances
        context["num_financial_instances"] = financial_instances.count()
        context["total_amount_sum"] = Financial.objects.filter(
            reception__service__doctor=doctor
        ).aggregate(Sum("total_amount"))["total_amount__sum"]

        receptions = Reception.objects.filter(service__doctor=doctor)
        context["receptions"] = receptions
        context["num_receptions"] = receptions.count()

        # Try to get the prescription header for the doctor
        prescription_header = PrescriptionHeader.objects.filter(
            doctor_id=doctor.id
        ).first()

        # Check if a prescription header exists
        if prescription_header is not None:
            context["prescription"] = prescription_header
        else:
            context["prescription"] = None

        return context


class DoctorCreateView(BaseCreateView):
    model = Doctor
    fields = "__all__"
    template_name = "doctor/create.html"
    app_name = "doctor"
    url_name = "detail"
    permission_required = "doctor.add_doctor"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DoctorUpdateView(BaseUpdateView):
    model = Doctor
    fields = ['first_name','last_name','email','phone_number','address','specialization','registration_number','image']
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
            messages.success(self.request, f"Doctor suspended successfully!")
            doctor.save()
        return HttpResponseRedirect(reverse_lazy("doctor:list"))


class ReactiveDoctorView(View):
    def get(self, request, pk):
        doctor = Doctor.objects.filter(pk=pk).first()
        if doctor:
            doctor.is_active = True
            messages.success(self.request, f"Doctor Reactive successfully!")
            doctor.save()
        return HttpResponseRedirect(reverse_lazy("doctor:suspend_list"))
