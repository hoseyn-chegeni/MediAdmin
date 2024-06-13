from django.shortcuts import render, redirect
from base.views import (
    BaseListView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
)
from .models import Insurance, InsuranceService
from django.urls import reverse, reverse_lazy
from .filters import InsuranceFilter, InsuranceServiceFilter
from client.models import Client
from django.contrib import messages
from django.views.generic import View
from .forms import InsuranceUpdateForm, InsuranceCreateForm

# Create your views here.
class InsuranceListView(BaseListView):
    model = Insurance
    template_name = "insurance/list.html"
    context_object_name = "insurance"
    filterset_class = InsuranceFilter
    permission_required = "insurance.view_insurance"


class InsuranceCreateView(BaseCreateView):
    model = Insurance
    form_class = InsuranceCreateForm
    template_name = "insurance/create.html"
    app_name = "insurance"
    url_name = "detail"
    permission_required = "insurance.add_insurance"


class InsuranceDetailView(BaseDetailView):
    model = Insurance
    template_name = "insurance/detail.html"
    permission_required = "insurance.view_insurance"

    def get_context_data(self, **kwargs):
        insurance = self.get_object()
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.filter(insurance_id=insurance.id)
        context["service"] = InsuranceService.objects.filter(insurance_id=insurance.id)
        return context


class InsuranceUpdateView(BaseUpdateView):
    model = Insurance
    form_class = InsuranceUpdateForm
    template_name = "insurance/update.html"
    app_name = "insurance"
    url_name = "detail"
    permission_required = "insurance.change_insurance"


class InsuranceDeleteView(BaseDeleteView):
    model = Insurance
    app_name = "insurance"
    url_name = "list"
    permission_required = "insurance.delete_insurance"


class DeleteSelectedInsuranceView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist("insurance_ids")
            deleted_users_count = Insurance.objects.filter(id__in=user_ids).delete()
            messages.success(
                request, f"تعداد {deleted_users_count[0]} بیمه با موفقیت حذف شدند."
            )
        return redirect("insurance:list")


# ServiceInsurance Views here.
class ServiceInsuranceCreateView(BaseCreateView):
    model = InsuranceService
    fields = [
        "service",
        "percentage",
        "notes",
    ]
    template_name = "insurance/services/create.html"
    app_name = "insurance"
    url_name = "service_insurance_detail"
    permission_required = "insurance.add_insuranceservice"

    def form_valid(self, form):
        form.instance.insurance = Insurance.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("insurance:detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["insurance"] = Insurance.objects.get(id=self.kwargs["pk"])
        return context


class ServiceInsuranceUpdateView(BaseUpdateView):
    model = InsuranceService
    fields = "__all__"
    template_name = "insurance/services/update.html"
    app_name = "insurance"
    url_name = "service_insurance_detail"
    permission_required = "insurance.change_insuranceservice"


class DeleteSelectedServiceInsuranceView(View):
    def post(self, request, pk):
        if request.method == "POST":
            service_insurance_ids = request.POST.getlist("service_insurance_ids")
            deleted_count, _ = InsuranceService.objects.filter(
                id__in=service_insurance_ids
            ).delete()
            messages.success(
                request, f"تعداد {deleted_count} سرویس از پوشش این بیمه خارج شدند"
            )

        return redirect(
            reverse("insurance:detail", kwargs={"pk": self.kwargs["pk"]})
        )  # Redirect to the detail URL with the appropriate kwargs
