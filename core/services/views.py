from django.shortcuts import render
from base.views import BaseCreateView,BaseDeleteView,BaseDetailView,BaseListView,BaseUpdateView
from .models import Service
from .filters import ServicesFilter


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


class ServiceDetailView(BaseDetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "services"

class ServiceUpdateView(BaseUpdateView):
    model = Service
    fields = "__all__"
    template_name = "services/update.html"
    app_name = "services"

class ServiceLDeleteView(BaseDeleteView):
    model = Service
    template_name = "services/delete.html"
    app_name = "services"


