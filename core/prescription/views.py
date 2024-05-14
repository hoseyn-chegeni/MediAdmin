from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse_lazy
from .models import (
    PrescriptionHeader,
    Prescription,
    PrescriptionItem,
    TemporaryPrescription,
)
from django.urls import reverse
from base.views import (
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
)
from django.contrib import messages
from django.views.generic import DetailView

from .filters import PrescriptionFilter
from .forms import PrescriptionItemForm
from reception.models import Reception
from django.views.generic import View

# Create your views here.
class PrescriptionListView(BaseListView):
    model = Prescription
    template_name = "prescription/list.html"
    context_object_name = "prescription"
    filterset_class = PrescriptionFilter
    permission_required = "prescription.view_prescription"


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
    permission_required = "prescription.view_prescription"


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


class PrescriptionItemUpdateView(BaseUpdateView):
    model = PrescriptionItem
    fields = [
        'medicine','quantity','consumption_time','consumption_dose','how_to_use','repeat_interval','repeat_period',
    ]
    template_name = "prescription/item/update.html"
    permission_required = "prescription.change_prescription"

    def get_success_url(self):
        return reverse_lazy(
            f"prescription:temp_detail", kwargs={"pk": self.object.prescription.pk}
        )


class PrescriptionItemDeleteView(BaseDeleteView):
    model = PrescriptionItem
    permission_required = "prescription.delete_prescription"

    def get(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()

        # Perform the delete operation directly without displaying a confirmation template

        self.object.delete()
        messages.success(self.request, self.message)
        return HttpResponseRedirect(
            reverse_lazy(
                f"prescription:temp_detail", kwargs={"pk": self.object.prescription.pk}
            )
        )


##################
##################
##################
##################
##################
##################
##################



class TemporaryPrescriptionDetailView(DetailView):
    model = TemporaryPrescription
    template_name = "prescription/temp/detail.html"
    context_object_name = "prescription"
    permission_required = "prescription.view_temporaryprescription"

    def post(self, request, *args, **kwargs):
        prescription = self.get_object()

        if "medicine" in request.POST:
            form = PrescriptionItemForm(request.POST)
            if form.is_valid():
                prescription_item = form.save(commit=False)
                prescription_item.prescription = prescription
                prescription_item.save()

        if "note" in request.POST:
            self.save_prescription(prescription, request.POST.get("note"))

        return HttpResponseRedirect(
            reverse("prescription:temp_detail", args=[prescription.id])
        )

    def save_prescription(self, prescription, notes):
        main_prescription = Prescription.objects.create(
            reception=prescription.reception,
            medication="",
            notes=notes,
            created_by=prescription.created_by,
        )

        items = PrescriptionItem.objects.filter(prescription=prescription)
        medication_list = []
        for item in items:
            medication_list.append(
                f"{item.medicine} ({item.quantity}) - {item.consumption_time} - {item.consumption_dose} - {item.how_to_use} - {item.repeat_interval} - {item.repeat_period} \n"
            )

        main_prescription.medication = "\n".join(medication_list)
        main_prescription.save()


def save_prescription(request, pk):
    temp_prescription = get_object_or_404(TemporaryPrescription, pk=pk)
    note = request.POST.get("note", "")

    main_prescription = Prescription.objects.create(
        reception=temp_prescription.reception,
        medication="",
        notes=note,
        created_by=temp_prescription.created_by,
    )

    items = PrescriptionItem.objects.filter(prescription=temp_prescription)
    medication_list = []
    for item in items:
        medication_list.append(
            f"{item.medicine} ({item.quantity}) - {item.consumption_time} - {item.consumption_dose} - {item.how_to_use} - {item.repeat_interval} - {item.repeat_period} ///"
        )
        item.temporary_prescription = None
        item.save()

    main_prescription.medication = "\n".join(medication_list)
    main_prescription.save()

    temp_prescription.delete()

    return redirect("prescription:detail", pk=main_prescription.pk)



class CreateTemporaryPrescription(View):
    def get(self, request, reception_id):
        reception = get_object_or_404(Reception, pk=reception_id)
        
        # Create a new TemporaryPrescription instance
        temp_prescription = TemporaryPrescription.objects.create(
            reception=reception,
            notes='',  # Set default value for notes
            created_by=request.user  # Assuming the user is authenticated
        )

        # Redirect to the detail view of the newly created TemporaryPrescription
        return redirect('prescription:temp_detail', pk=temp_prescription.pk)