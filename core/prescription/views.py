from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import PrescriptionHeader, Prescription
from reception.models import Reception
from base.views import (
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
)
from .filters import PrescriptionFilter
from .forms import PrescriptionItemForm
# Create your views here.
class PrescriptionListView(BaseListView):
    model = Prescription
    template_name = "prescription/list.html"
    context_object_name = "prescription"
    filterset_class = PrescriptionFilter
    permission_required = "prescription.view_prescription"


class PrescriptionCreateView(BaseCreateView):
    model = Prescription
    fields = [
        "diagnosis",
        "medication",
        "instructions",
    ]
    template_name = "prescription/create.html"
    app_name = "prescription"
    url_name = "detail"
    permission_required = "prescription.add_prescription"

    def get_initial(self):
        initial = super().get_initial()
        initial["reception"] = self.kwargs["pk"]
        return initial

    def form_valid(self, form):
        form.instance.reception_id = self.kwargs["pk"]
        return super().form_valid(form)


class PrescriptionCreateWithoutPkView(BaseCreateView):
    model = Prescription
    fields = "__all__"
    template_name = "prescription/create.html"
    app_name = "prescription"
    url_name = "detail"
    permission_required = "prescription.add_prescription"


class PrescriptionDetailView(BaseDetailView):
    model = Prescription
    template_name = "prescription/detail.html"
    context_object_name = "prescription"
    permission_required = "prescription.view_prescription"

    def post(self, request, *args, **kwargs):
        form = PrescriptionItemForm(request.POST)
        prescription = self.get_object()
        if form.is_valid():
            prescription_id = prescription.id
            prescription = Prescription.objects.get(id=prescription_id)
            prescription_item = form.save(commit=False)
            prescription_item.prescription = prescription
            prescription_item.save()
        return super().get(request, *args, **kwargs)


class PrescriptionUpdateView(BaseUpdateView):
    model = Prescription
    fields = "__all__"
    template_name = "prescription/update.html"
    app_name = "prescription"
    url_name = "detail"
    permission_required = "prescription.change_prescription"


class PrescriptionDeleteView(BaseDeleteView):
    model = Prescription
    app_name = "prescription"
    url_name = "list"
    permission_required = "prescription.delete_prescription"


# Prescription Header Views here.
class PrescriptionHeaderCreateView(BaseCreateView):
    model = PrescriptionHeader
    fields = {"member_of", "specialization", "phone_number", "address"}
    template_name = "prescription/create.html"
    app_name = "doctor"
    url_name = "detail"
    permission_required = "prescription.add_prescriptionheader"

    def get_initial(self):
        initial = super().get_initial()
        initial["doctor"] = self.kwargs["pk"]
        return initial

    def form_valid(self, form):
        # Set the client for the reception
        form.instance.doctor_id = self.kwargs[
            "pk"
        ]  # Assuming client's pk is passed in the URL
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.kwargs["pk"]}
        )


class PrescriptionHeaderUpdateView(BaseUpdateView):
    model = PrescriptionHeader
    fields = {"member_of", "specialization", "phone_number", "address"}
    template_name = "prescription/update.html"
    app_name = "doctor"
    url_name = "detail"
    permission_required = "prescription.update_prescriptionheader"

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.doctor_id}
        )


