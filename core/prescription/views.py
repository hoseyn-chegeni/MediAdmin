from django.shortcuts import render
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

# Create your views here.
class PrescriptionListView(BaseListView):
    model = Prescription
    template_name = "prescription/list.html"
    context_object_name = "prescription"
    filterset_class = PrescriptionFilter


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

    def get_initial(self):
        initial = super().get_initial()
        initial["reception"] = self.kwargs["pk"]
        return initial

    def form_valid(self, form):
        form.instance.reception_id = self.kwargs[
            "pk"
        ]  
        return super().form_valid(form)
    

class PrescriptionCreateWithoutPkView(BaseCreateView):
    model = Prescription
    fields = '__all__'
    template_name = "prescription/create.html"
    app_name = "prescription"
    url_name = "detail"

class PrescriptionDetailView(BaseDetailView):
    model = Prescription
    template_name = "prescription/detail.html"
    context_object_name = "prescription"


class PrescriptionUpdateView(BaseUpdateView):
    model = Prescription
    fields = "__all__"
    template_name = "prescription/update.html"
    app_name = "prescription"
    url_name = "detail"


class PrescriptionDeleteView(BaseDeleteView):
    model = Prescription
    template_name = "prescription/delete.html"
    app_name = "prescription"
    url_name = "list"


# Prescription Header Views here.
class PrescriptionHeaderCreateView(BaseCreateView):
    model = PrescriptionHeader
    fields = {"member_of", "specialization", "phone_number", "address"}
    template_name = "prescription/create.html"
    app_name = "doctor"
    url_name = "detail"

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

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.doctor_id}
        )
