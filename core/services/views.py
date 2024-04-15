from django.shortcuts import redirect
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Service, ServiceConsumable, ServiceCategory, Package, ServicePackage
from reception.models import Reception
from .filters import ServicesFilter, QueueFilter, ServiceCategoryFilter, PackageFilter
from django.urls import reverse_lazy
from insurance.models import InsuranceService
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from datetime import date
from client.models import Client
from django.views.generic import FormView
from .forms import ServiceSelectionForm
from doctor.models import Doctor


# Create your views here.
class ServiceListView(BaseListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    filterset_class = ServicesFilter
    permission_required = "services.view_service"


class ServiceCreateView(BaseCreateView):
    model = Service
    fields = "__all__"
    template_name = "services/create.html"
    app_name = "services"
    url_name = "detail"
    permission_required = "services.add_service"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ServiceDetailView(BaseDetailView):
    model = Service
    template_name = "services/detail.html"
    permission_required = "services.view_service"

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
        "medical_equipment",
        "doctors_wage_percentage",
    ]
    template_name = "services/update.html"
    app_name = "services"
    url_name = "detail"
    permission_required = "services.change_service"


class ServiceAppointmentConfigView(BaseUpdateView):
    model = Service
    fields = ["appointment_per_day", "off_days", "check_consumable_inventory"]
    template_name = "services/appointment_config.html"
    app_name = "services"
    url_name = "detail"
    permission_required = "services.change_service"


class ServiceLDeleteView(BaseDeleteView):
    model = Service
    app_name = "services"
    url_name = "list"
    permission_required = "services.delete_service"


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


class DeleteSelectedServicesView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "service_ids"
            )  # Get the list of selected user IDs from the form
            Service.objects.filter(id__in=user_ids).delete()  # Delete selected users
        return redirect("services:list")


# ServiceConsumable Views here.
class ServiceConsumableCreateView(BaseCreateView):
    model = ServiceConsumable
    fields = [
        "consumable",
        "dose",
        "note",
    ]
    template_name = "services/consumable_create.html"
    permission_required = "services.view_serviceconsumable"

    def form_valid(self, form):
        form.instance.service = Service.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("services:detail", kwargs={"pk": self.kwargs["pk"]})


class ServiceConsumableDeleteView(BaseDeleteView):
    model = ServiceConsumable
    app_name = "services"
    url_name = "list"
    permission_required = "services.delete_serviceconsumable"


class WaitingQueueView(BaseListView):
    model = Reception
    template_name = "services/queue.html"
    context_object_name = "receptions"
    filterset_class = QueueFilter
    permission_required = "reception.view_reception"

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
    permission_required = "services.view_servicecategory"


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
    permission_required = "services.add_servicecategory"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ServiceCategoryDetailView(BaseDetailView):
    model = ServiceCategory
    template_name = "services/category/detail.html"
    permission_required = "services.view_servicecategory"

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
    permission_required = "services.change_servicecategory"


class ServiceCategoryDeleteView(BaseDeleteView):
    model = ServiceCategory
    app_name = "services"
    url_name = "category_list"
    permission_required = "services.delete_servicecategory"


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
    permission_required = "services.view_package"


class PackageCreateView(BaseCreateView):
    model = Package
    fields = "__all__"
    template_name = "package/create.html"
    app_name = "services"
    url_name = "package_detail"
    permission_required = "services.add_package"


class PackageDetailView(BaseDetailView):
    model = Package
    template_name = "package/detail.html"
    permission_required = "services.view_package"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = self.get_object()
        services = package.servicepackage_set.all().select_related(
            "service"
        )  # Retrieve associated services
        context["services"] = services
        doctors = set()
        for service_package in package.servicepackage_set.all():
            doctors.add(service_package.service.doctor)
        context["doctors"] = doctors

        return context


class PackageUpdateView(BaseUpdateView):
    model = Package
    template_name = "package/update.html"
    fields = "__all__"
    app_name = "services"
    url_name = "package_detail"
    permission_required = "services.change_package"


class PackageDeleteView(BaseDeleteView):
    model = Package
    app_name = "services"
    url_name = "package_list"
    permission_required = "services.delete_package"


class SuspendPackageView(View):
    def get(self, request, pk):
        package = Package.objects.get(pk=pk)
        if package:
            package.is_active = False
            messages.success(self.request, f" پکیج {package.name} غیرفعال شد!")
            package.save()
        return HttpResponseRedirect(
            reverse_lazy("services:package_detail", kwargs={"pk": package.pk})
        )


class ReactivePackageView(View):
    def get(self, request, pk):
        package = Package.objects.filter(pk=pk).first()
        if package:
            package.is_active = True
            messages.success(self.request, f"پکیج {package.name} مجددا فعال شد !")
            package.save()
        return HttpResponseRedirect(
            reverse_lazy("services:package_detail", kwargs={"pk": package.pk})
        )


# Package Steps Here.
class ServicePackageCreateView(BaseCreateView):
    model = ServicePackage
    fields = ["service", "gap_with_next_service"]
    template_name = "package/steps/create.html"
    permission_required = "services.view_servicepackage"

    def form_valid(self, form):
        # Get the package object from the URL parameter
        package_id = self.kwargs["pk"]
        package = Package.objects.get(pk=package_id)
        form.instance.package = package

        # Validate the gap_with_next_service field
        gap_with_next_service = form.cleaned_data.get("gap_with_next_service")
        if gap_with_next_service is not None and gap_with_next_service <= 0:
            form.add_error(
                "gap_with_next_service",
                "فاصله زمانی با سرویس بعدی باید یک عدد صحیح مثبت باشد.",
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("services:package_detail", kwargs={"pk": self.kwargs["pk"]})


class ServicePackageUpdateView(BaseUpdateView):
    model = ServicePackage
    fields = [
        "gap_with_next_service",
    ]
    template_name = "package/steps/update.html"
    permission_required = "services.change_servicepackage"

    def get_success_url(self):
        # Redirect to the package detail page after updating the service
        package = (
            self.get_object().package.id
        )  # Assuming Service has a ForeignKey to Package
        return reverse_lazy("services:package_detail", kwargs={"pk": package})


class ServicePackageDeleteView(BaseDeleteView):
    model = ServicePackage
    permission_required = "services.delete_servicepackage"

    def get_success_url(self):
        package = self.get_object().package.id
        return reverse_lazy("services:package_detail", kwargs={"pk": package})


# Update Service Price
class UpdateServicePricesView(FormView):
    template_name = "services/bulk_update.html"
    form_class = ServiceSelectionForm
    success_url = reverse_lazy(
        "services:list"
    )  # Change this to the appropriate success URL

    def form_valid(self, form):
        services = form.cleaned_data["services"]
        percentage_change = form.cleaned_data["percentage_change"]

        for service in services:
            # Calculate the new price based on the percentage change
            new_price = service.price * (1 + percentage_change / 100)
            # Update the service price
            service.price = new_price
            service.save()

        messages.success(self.request, "افزایش فیمت با موفقیت انجام شد")
        return super().form_valid(form)


class AddServiceUsingDoctorProfileView(BaseCreateView):
    model = Service
    fields = [
        "name",
        "doctors_wage_percentage",
        "description",
        "category",
        "duration",
        "price",
        "preparation_instructions",
        "documentation_requirements",
        "is_active",
        "therapeutic_measures",
        "recommendations",
        "appointment_per_day",
        "off_days",
        "medical_equipment",
    ]
    template_name = "services/create_from_doctor_profile.html"
    app_name = "services"
    url_name = "detail"
    permission_required = "services.add_services"

    def get_initial(self):
        initial = super().get_initial()
        # Set the initial client value to the client whose profile page the user is on
        initial["client"] = self.kwargs[
            "pk"
        ]  # Assuming client's pk is passed in the URL
        return initial

    def form_valid(self, form):
        # Set the client for the reception
        form.instance.created_by = self.request.user
        form.instance.doctor_id = self.kwargs[
            "pk"
        ]  # Assuming client's pk is passed in the URL
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.get(id=self.kwargs["pk"])
        return context
