from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from .models import ConsumableV2, Inventory, ConsumableCategory
from django.views.generic import ListView


# Create your views here.
# Consumable Views.
class ConsumableListView(ListView):
    model = ConsumableV2
    template_name = "consumable/list.html"
    context_object_name = "consumable"


class ConsumableDetailView(BaseDetailView):
    model = ConsumableV2
    template_name = "consumable/detail.html"
    context_object_name = "consumable"
    permission_required = "consumable.view_consumablev2"

    def get_context_data(self, **kwargs):
        consumable = self.get_object()
        context = super().get_context_data(**kwargs)
        context["inventory"] = Inventory.objects.filter(consumable_id=consumable.id)
        context["first_inventory"] = (
            Inventory.objects.filter(consumable_id=consumable.id)
            .order_by("expiration_date")
            .first()
        )
        return context


class ConsumableCreateView(BaseCreateView):
    model = ConsumableV2
    fields = "__all__"
    template_name = "consumable/create.html"
    app_name = "consumable"
    url_name = "detail"
    permission_required = "consumable.add_consumablev2"


class ConsumableUpdateView(BaseUpdateView):
    model = ConsumableV2
    fields = "__all__"
    template_name = "consumable/update.html"
    app_name = "consumable"
    url_name = "detail"
    permission_required = "consumable.change_consumablev2"


class ConsumableDeleteView(BaseDeleteView):
    model = ConsumableV2
    app_name = "consumable"
    url_name = "list"
    permission_required = "consumable.delete_consumablev2"


# Inventory Views.


class InventoryListView(ListView):
    model = Inventory
    template_name = "consumable/inventory/list.html"
    context_object_name = "inventory"


class InventoryCreateView(BaseCreateView):
    model = Inventory
    fields = "__all__"
    template_name = "consumable/inventory/create.html"
    app_name = "consumable"
    url_name = "inventory_detail"
    permission_required = "consumable.add_inventory"


class InventoryDetailView(BaseDetailView):
    model = Inventory
    template_name = "consumable/inventory/detail.html"
    context_object_name = "inventory"
    permission_required = "consumable.view_inventory"


class InventoryUpdateView(BaseUpdateView):
    model = Inventory
    fields = "__all__"
    template_name = "consumable/inventory/update.html"
    app_name = "consumable"
    url_name = "inventory_detail"
    permission_required = "consumable.change_inventory"


class InventoryDeleteView(BaseDeleteView):
    model = Inventory
    app_name = "consumable"
    url_name = "inventory_list"
    permission_required = "consumable.delete_inventory"


# Consumable Category Views here.
class ConsumableCategoryListView(BaseListView):
    model = ConsumableCategory
    template_name = "consumable/category/list.html"
    context_object_name = "category"
    filterset_class = 0
    permission_required = "consumable.view_consumablecategory"


class ConsumableCategoryDetailView(BaseDetailView):
    model = ConsumableCategory
    template_name = "consumable/category/detail.html"
    context_object_name = "category"
    permission_required = "consumable.view_consumablecategory"

    def get_context_data(self, **kwargs):
        category = self.get_object()
        context = super().get_context_data(**kwargs)
        context["consumable"] = ConsumableV2.objects.filter(category_id=category.id)
        return context


class ConsumableCategoryCreateView(BaseCreateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "consumable/category/create.html"
    app_name = "consumable"
    url_name = "category_detail"
    permission_required = "consumable.add_consumablecategory"


class ConsumableCategoryUpdateView(BaseUpdateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "consumable/category/update.html"
    app_name = "consumable"
    url_name = "category_detail"
    permission_required = "consumable.change_consumablecategory"


class ConsumableCategoryDeleteView(BaseDeleteView):
    model = ConsumableCategory
    app_name = "consumable"
    url_name = "category_list"
    permission_required = "consumable.delete_consumablecategory"
