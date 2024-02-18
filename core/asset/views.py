from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Consumable, ConsumableCategory, Supplier
from .filters import ConsumableFilter, ConsumableCategoryFilter, SupplierFilter


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
    url_name = Supplier


# Consumable Category Views here.
class ConsumableCategoryListView(BaseListView):
    model = ConsumableCategory
    template_name = "asset/category/list.html"
    context_object_name = "category"
    filterset_class = ConsumableCategoryFilter


class ConsumableCategoryDetailView(BaseDetailView):
    model = ConsumableCategory
    template_name = "asset/category/detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        category = self.get_object()
        context = super().get_context_data(**kwargs)
        context["consumable"] = Consumable.objects.filter(category_id=category.id)
        return context


class ConsumableCategoryCreateView(BaseCreateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "asset/category/create.html"
    app_name = "asset"
    url_name = "category_detail"


class ConsumableCategoryUpdateView(BaseUpdateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "asset/category/update.html"
    app_name = "asset"
    url_name = "category_detail"


class ConsumableCategoryDeleteView(BaseDeleteView):
    model = ConsumableCategory
    template_name = "asset/category/delete.html"
    app_name = "asset"
    url_name = "category_list"


# Supplier views here.
class SupplierListView(BaseListView):
    model = Supplier
    template_name = "asset/supplier/list.html"
    context_object_name = "supplier"
    filterset_class = SupplierFilter


class SupplierDetailView(BaseDetailView):
    model = Supplier
    template_name = "asset/supplier/detail.html"
    context_object_name = "supplier"


class SupplierCreateView(BaseCreateView):
    model = Supplier
    fields = "__all__"
    template_name = "asset/supplier/create.html"
    app_name = "asset"
    url_name = "supplier_detail"


class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    fields = "__all__"
    template_name = "asset/supplier/update.html"
    app_name = "asset"
    url_name = "supplier_detail"


class SupplierDeleteView(BaseDeleteView):
    model = Supplier
    template_name = "asset/supplier/delete.html"
    app_name = "asset"
    url_name = "supplier_list"
