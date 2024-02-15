from django.shortcuts import render
from base.views import (
    BaseListView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
)
from .models import Insurance
from django.urls import reverse_lazy
from .filters import InsuranceFilter
from client.models import Client


# Create your views here.
class InsuranceListView(BaseListView):
    model = Insurance
    template_name = "insurance/list.html"
    context_object_name = "insurance"
    filterset_class = InsuranceFilter


class InsuranceCreateView(BaseCreateView):
    model = Insurance
    fields = "__all__"
    template_name = "insurance/create.html"
    app_name = "insurance"


class InsuranceDetailView(BaseDetailView):
    model = Insurance
    template_name = "insurance/detail.html"
    context_object_name = "insurance"

    def get_context_data(self, **kwargs):
        insurance = self.get_object()
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.filter(insurance_id=insurance.id)
        return context


class InsuranceUpdateView(BaseUpdateView):
    model = Insurance
    fields = "__all__"
    template_name = "insurance/update.html"
    app_name = "insurance"


class InsuranceDeleteView(BaseDeleteView):
    model = Insurance
    template_name = "insurance/delete.html"
    app_name = "insurance"
