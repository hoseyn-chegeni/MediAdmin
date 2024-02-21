from django.shortcuts import render
from django.urls import reverse_lazy
from .models import PrescriptionHeader
from base.views import BaseCreateView, BaseUpdateView
# Create your views here.

class PrescriptionHeaderCreateView(BaseCreateView):
    model = PrescriptionHeader
    fields = {
        "member_of","specialization","phone_number","address"
    }
    template_name = "prescription/create.html"
    app_name = "doctor"
    url_name = "detail"

    def get_initial(self):
        initial = super().get_initial()
        initial["doctor"] = self.kwargs[
            "pk"
        ]
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
    fields = {
        "member_of","specialization","phone_number","address"
    }
    template_name = "prescription/update.html"
    app_name = "doctor"
    url_name = "detail"




    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk":self.object.doctor_id}
        )
