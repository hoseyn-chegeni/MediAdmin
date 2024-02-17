from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Consumable
from .filters import ConsumableFilter


# Create your views here.
class ConsumableListView(BaseListView):
    model = Consumable
    template_name = "asset/list.html"
    context_object_name = "consumable"
    filterset_class = ConsumableFilter


class ConsumableDetailView(BaseDetailView):
    model = Consumable
    template_name = "asset/detail.html"
    context_object_name = "consumable"


class ConsumableCreateView(BaseCreateView):
    model = Consumable
    fields = "__all__"
    template_name = "asset/create.html"
    app_name = "asset"


class ConsumableUpdateView(BaseUpdateView):
    model = Consumable
    fields = "__all__"
    template_name = "asset/update.html"
    app_name = "asset"


class ConsumableDeleteView(BaseDeleteView):
    model = Consumable
    template_name = "asset/delete.html"
    app_name = "asset"
