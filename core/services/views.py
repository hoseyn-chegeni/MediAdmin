from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Service, ServiceConsumable, ServiceCategory, Package
from reception.models import Reception
from .filters import ServicesFilter, QueueFilter, ServiceCategoryFilter, PackageFilter
from django.urls import reverse_lazy
from insurance.models import InsuranceService
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from datetime import date
from client.models import Client


# Create your views here.
class ServiceListView(BaseListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    filterset_class = ServicesFilter

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active=True)


class SuspendServiceListView(BaseListView):
    model = Service
    template_name = "services/suspend_list.html"
    context_object_name = "services"
    filterset_class = ServicesFilter

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active=False)


class ServiceCreateView(BaseCreateView):
    model = Service
    fields = "__all__"
    template_name = "services/create.html"
    app_name = "services"
    url_name = "detail"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ServiceDetailView(BaseDetailView):
    model = Service
    template_name = "services/detail.html"

    def get_context_data(self, **kwargs):
        service = self.get_object()
        context = super().get_context_data(**kwargs)
        context["consumable"] = ServiceConsumable.objects.filter(service_id=service.id)

        reception = Reception.objects.filter(service_id=service.id)
        context["reception"] = reception
        context["num_reception"] = reception.count()

        context["insurance"] = InsuranceService.objects.filter(service_id=service.id)

        client_ids = (
            service.reception_set.all().values_list("client", flat=True).distinct()
        )
        clients = Client.objects.filter(
            id__in=client_ids
        )  # Get Client objects using the IDs
        context["clients"] = clients

        return context


class ServiceUpdateView(BaseUpdateView):
    model = Service
    fields = [
        "name",
        "doctor",
        "description",
        "category",
        "duration",
        "price",
        "is_active",
        "preparation_instructions",
        "documentation_requirements",
        "therapeutic_measures",
        "recommendations",
    ]
    template_name = "services/update.html"
    app_name = "services"
    url_name = "detail"


class ServiceAppointmentConfigView(BaseUpdateView):
    model = Service
    fields = ["appointment_per_day", "off_days"]
    template_name = "services/appointment_config.html"
    app_name = "services"
    url_name = "detail"


class ServiceLDeleteView(BaseDeleteView):
    model = Service
    app_name = "services"
    url_name = "list"


class SuspendServiceView(View):
    def get(self, request, pk):
        service = Service.objects.get(pk=pk)
        if service:
            service.is_active = False
            messages.success(self.request, f"سرویس {service.name} غیرفعال شد!")
            service.save()
        return HttpResponseRedirect(
            reverse_lazy("services:detail", kwargs={"pk": service.pk})
        )


class ReactiveServiceView(View):
    def get(self, request, pk):
        service = Service.objects.filter(pk=pk).first()
        if service:
            service.is_active = True
            messages.success(self.request, f"سرویس {service.name} مجددا فعال شد !")
            service.save()
        return HttpResponseRedirect(
            reverse_lazy("services:detail", kwargs={"pk": service.pk})
        )


# ServiceConsumable Views here.
class ServiceConsumableCreateView(BaseCreateView):
    model = ServiceConsumable
    fields = [
        "consumable",
        "dose",
        "note",
    ]
    template_name = "services/consumable_create.html"

    def form_valid(self, form):
        form.instance.service = Service.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("services:detail", kwargs={"pk": self.kwargs["pk"]})


class ServiceConsumableDeleteView(BaseDeleteView):
    model = ServiceConsumable
    app_name = "services"
    url_name = "list"


class WaitingQueueView(BaseListView):
    template_name = "services/queue.html"
    context_object_name = "receptions"
    filterset_class = QueueFilter

    def get_queryset(self):
        # Retrieve the service object based on the provided service_id in the URL
        service_id = self.kwargs["service_id"]
        service = Service.objects.get(id=service_id)
        # Get today's date
        today = date.today()
        # Filter receptions for the service for today with status 'WAITE'
        receptions_for_service_today = Reception.objects.filter(
            service=service, date=today, status="WAITE"
        )
        return receptions_for_service_today

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = Service.objects.get(id=self.kwargs["service_id"])
        return context


# SERVICE CATEGORY VIEWS.
class ServiceCategoryListView(BaseListView):
    model = ServiceCategory
    template_name = "services/category/list.html"
    context_object_name = "category"
    filterset_class = ServiceCategoryFilter


class ServiceCategoryCreateView(BaseCreateView):
    model = ServiceCategory
    fields = [
        "name",
        "description",
        "is_active",
    ]
    template_name = "services/category/create.html"
    app_name = "services"
    url_name = "category_detail"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ServiceCategoryDetailView(BaseDetailView):
    model = ServiceCategory
    template_name = "services/category/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_category = self.get_object()
        services = service_category.service_set.all()
        context["services"] = services

        doctors = set([service.doctor for service in services if service.doctor])
        context["doctors"] = doctors

        return context


class ServiceCategoryUpdateView(BaseUpdateView):
    model = ServiceCategory
    fields = [
        "name",
        "description",
        "is_active",
    ]
    template_name = "services/category/update.html"
    app_name = "services"
    url_name = "category_detail"


class ServiceCategoryDeleteView(BaseDeleteView):
    model = ServiceCategory
    app_name = "services"
    url_name = "category_list"


class SuspendServiceCategoryView(View):
    def get(self, request, pk):
        category = ServiceCategory.objects.get(pk=pk)
        if category:
            category.is_active = False
            messages.success(
                self.request, f"دسته بندی سرویس {category.name} غیرفعال شد!"
            )
            category.save()
        return HttpResponseRedirect(
            reverse_lazy("services:category_detail", kwargs={"pk": category.pk})
        )


class ReactiveServiceCategoryView(View):
    def get(self, request, pk):
        category = ServiceCategory.objects.filter(pk=pk).first()
        if category:
            category.is_active = True
            messages.success(
                self.request, f"دسته بندی سرویس {category.name} مجددا فعال شد !"
            )
            category.save()
        return HttpResponseRedirect(
            reverse_lazy("services:category_detail", kwargs={"pk": category.pk})
        )


# PACKAGE VIEWS HERE.
class PackageListView(BaseListView):
    model = Package
    template_name = "package/list.html"
    context_object_name = "package"
    filterset_class = PackageFilter


class PackageCreateView(BaseCreateView):
    model = Package
    fields = "__all__"
    template_name = "package/create.html"
    app_name = "services"
    url_name = "package_detail"


class PackageDetailView(BaseDetailView):
    model = Package
    template_name = "package/detail.html"


class PackageUpdateView(BaseUpdateView):
    model = Package
    template_name = "package/update.html"
    fields = "__all__"
    app_name = "services"
    url_name = "package_detail"


class PackageDeleteView(BaseDeleteView):
    model = Package
    app_name = "services"
    url_name = "package_list"

class SuspendPackageView(View):
    def get(self, request, pk):
        package = Package.objects.get(pk=pk)
        if package:
            package.is_active = False
            messages.success(
                self.request, f" پکیج {package.name} غیرفعال شد!"
            )
            package.save()
        return HttpResponseRedirect(
            reverse_lazy("services:package_detail", kwargs={"pk": package.pk})
        )


class ReactivePackageView(View):
    def get(self, request, pk):
        package = Package.objects.filter(pk=pk).first()
        if package:
            package.is_active = True
            messages.success(
                self.request, f"پکیج {package.name} مجددا فعال شد !"
            )
            package.save()
        return HttpResponseRedirect(
            reverse_lazy("services:package_detail", kwargs={"pk": package.pk})
        )
