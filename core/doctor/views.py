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


# Create your views here.
class DoctorListView(BaseListView):
    model = Doctor
    template_name = "doctor/list.html"
    context_object_name = "doctor"
    filterset_class = DoctorFilter


class DoctorDetailView(BaseDetailView):
    model = Doctor
    template_name = "doctor/detail.html"
    context_object_name = "doctor"

    def get_context_data(self, **kwargs):
        doctor = self.get_object()
        context = super().get_context_data(**kwargs)
        
        # Try to get the prescription header for the doctor
        prescription_header = PrescriptionHeader.objects.filter(doctor_id=doctor.id).first()
        
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


class DoctorUpdateView(BaseUpdateView):
    model = Doctor
    fields = "__all__"
    template_name = "doctor/update.html"
    app_name = "doctor"
    url_name = "detail"


class DoctorDeleteView(BaseDeleteView):
    model = Doctor
    template_name = "doctor/delete.html"
    app_name = "doctor"
    url_name = "list"
