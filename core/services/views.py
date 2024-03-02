from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Service, ServiceConsumable
from reception.models import Reception
from .filters import ServicesFilter
from django.urls import reverse_lazy
from insurance.models import InsuranceService
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View


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


class ServiceDetailView(BaseDetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "services"

    def get_context_data(self, **kwargs):
        service = self.get_object()
        context = super().get_context_data(**kwargs)
        context["consumable"] = ServiceConsumable.objects.filter(service_id=service.id)

        reception = Reception.objects.filter(service_id=service.id)
        context["reception"] = reception
        context["num_reception"] = reception.count()

        context["insurance"] = InsuranceService.objects.filter(service_id=service.id)

        return context


class ServiceUpdateView(BaseUpdateView):
    model = Service
    fields = "__all__"
    template_name = "services/update.html"
    app_name = "services"
    url_name = "detail"


class ServiceLDeleteView(BaseDeleteView):
    model = Service
    app_name = "services"
    url_name = "list"


class SuspendServiceView(View):
    def get(self, request, pk):
        user = Service.objects.get(pk=pk)
        if user:
            user.is_active = False
            messages.success(
                self.request, f"Service Suspended '{user.name}' successfully!"
            )
            user.save()
        return HttpResponseRedirect(reverse_lazy("services:list"))
    
    
class ReactiveServiceView(View):
    def get(self, request, pk):
        user = Service.objects.filter(pk=pk).first()
        if user:
            user.is_active = True
            messages.success(
                self.request, f"Service Reactive '{user.name}' successfully!"
            )
            user.save()
        return HttpResponseRedirect(reverse_lazy("services:suspend_list"))


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



