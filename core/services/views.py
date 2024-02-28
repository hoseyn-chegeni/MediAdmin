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


# Create your views here.
class ServiceListView(BaseListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    filterset_class = ServicesFilter


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

        return context


class ServiceUpdateView(BaseUpdateView):
    model = Service
    fields = "__all__"
    template_name = "services/update.html"
    app_name = "services"
    url_name = "detail"


class ServiceLDeleteView(BaseDeleteView):
    model = Service
    template_name = "services/delete.html"
    app_name = "services"
    url_name = "list"


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
    template_name = "services/consumable_delete.html"
    app_name = "services"
    url_name = "list"
