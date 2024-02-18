from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Consumable, ConsumableCategory
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
    url_name = "detail"


class ConsumableUpdateView(BaseUpdateView):
    model = Consumable
    fields = "__all__"
    template_name = "asset/update.html"
    app_name = "asset"
    url_name = "detail"


class ConsumableDeleteView(BaseDeleteView):
    model = Consumable
    template_name = "asset/delete.html"
    app_name = "asset"
    url_name = "list"


# Consumable Category Views here.
class ConsumableListView(BaseListView):
    model = ConsumableCategory
    template_name = "asset/category/list.html"
    context_object_name = "category"
    filterset_class = 0


class ConsumableDetailView(BaseDetailView):
    model = ConsumableCategory
    template_name = "asset/category/detail.html"
    context_object_name = "category"


class ConsumableCreateView(BaseCreateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "asset/category/create.html"
    app_name = "asset"
    url_name = "category_detail"


class ConsumableUpdateView(BaseUpdateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "asset/category/update.html"
    app_name = "asset"
    url_name = "category_detail"


class ConsumableDeleteView(BaseDeleteView):
    model = ConsumableCategory
    template_name = "asset/category/delete.html"
    app_name = "asset"
    url_name = "category_list"
