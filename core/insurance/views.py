from django.shortcuts import render
from base.views import (
    BaseListView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
)
from .models import Insurance, InsuranceService
from django.urls import reverse_lazy
from .filters import InsuranceFilter, InsuranceServiceFilter
from client.models import Client


# Create your views here.
class InsuranceListView(BaseListView):
    model = Insurance
    template_name = "insurance/list.html"
    context_object_name = "insurance"
    filterset_class = InsuranceFilter
    permission_required = "insurance.view_insurance"


class InsuranceCreateView(BaseCreateView):
    model = Insurance
    fields = "__all__"
    template_name = "insurance/create.html"
    app_name = "insurance"
    url_name = "detail"
    permission_required = "insurance.add_insurance"


class InsuranceDetailView(BaseDetailView):
    model = Insurance
    template_name = "insurance/detail.html"
    context_object_name = "insurance"
    permission_required = "insurance.view_insurance"

    def get_context_data(self, **kwargs):
        insurance = self.get_object()
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.filter(insurance_id=insurance.id)
        context["service"] = InsuranceService.objects.filter(insurance_id=insurance.id)
        return context


class InsuranceUpdateView(BaseUpdateView):
    model = Insurance
    fields = "__all__"
    template_name = "insurance/update.html"
    app_name = "insurance"
    url_name = "detail"
    permission_required = "insurance.change_insurance"


class InsuranceDeleteView(BaseDeleteView):
    model = Insurance
    app_name = "insurance"
    url_name = "list"
    permission_required = "insurance.delete_insurance"


# ServiceInsurance Views here.
class ServiceInsuranceListView(BaseListView):
    model = InsuranceService
    template_name = "service_insurance/list.html"
    context_object_name = "insurance"
    filterset_class = InsuranceServiceFilter
    permission_required = "insurance.view_insuranceservice"


class ServiceInsuranceCreateView(BaseCreateView):
    model = InsuranceService
    fields = "__all__"
    template_name = "service_insurance/create.html"
    app_name = "insurance"
    url_name = "service_insurance_detail"
    permission_required = "insurance.add_insuranceservice"


class ServiceInsuranceUpdateView(BaseUpdateView):
    model = InsuranceService
    fields = "__all__"
    template_name = "service_insurance/update.html"
    app_name = "insurance"
    url_name = "service_insurance_detail"
    permission_required = "insurance.change_insuranceservice"


class ServiceInsuranceDetailView(BaseDetailView):
    model = InsuranceService
    template_name = "service_insurance/detail.html"
    context_object_name = "insurance"
    permission_required = "insurance.view_insuranceservice"


class ServiceInsuranceDeleteView(BaseDeleteView):
    model = InsuranceService
    app_name = "insurance"
    url_name = "list"
    permission_required = "insurance.delete_insuranceservice"
