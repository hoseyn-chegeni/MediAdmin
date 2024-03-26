from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Consumable, ConsumableCategory, Supplier, Equipment
from .filters import ConsumableFilter, ConsumableCategoryFilter, SupplierFilter


# Create your views here.
class ConsumableListView(BaseListView):
    model = Consumable
    template_name = "asset/list.html"
    context_object_name = "consumable"
    filterset_class = ConsumableFilter
    permission_required = "asset.view_consumable"


class ConsumableDetailView(BaseDetailView):
    model = Consumable
    template_name = "asset/detail.html"
    context_object_name = "consumable"
    permission_required = "asset.view_consumable"


class ConsumableCreateView(BaseCreateView):
    model = Consumable
    fields = "__all__"
    template_name = "asset/create.html"
    app_name = "asset"
    url_name = "detail"
    permission_required = "asset.add_consumable"


class ConsumableUpdateView(BaseUpdateView):
    model = Consumable
    fields = "__all__"
    template_name = "asset/update.html"
    app_name = "asset"
    url_name = "detail"
    permission_required = "asset.change_consumable"


class ConsumableDeleteView(BaseDeleteView):
    model = Consumable
    app_name = "asset"
    url_name = Supplier
    permission_required = "asset.delete_consumable"


class UpdateInventoryTrackingNumberViews(BaseUpdateView):
    model = Consumable
    fields = ["inventory_tracking_number"]
    template_name = "asset/update_inventory_tracking_number.html"
    app_name = "asset"
    url_name = "detail"
    permission_required = "asset.change_consumable"


# Consumable Category Views here.
class ConsumableCategoryListView(BaseListView):
    model = ConsumableCategory
    template_name = "asset/category/list.html"
    context_object_name = "category"
    filterset_class = ConsumableCategoryFilter
    permission_required = "asset.view_consumablecategory"


class ConsumableCategoryDetailView(BaseDetailView):
    model = ConsumableCategory
    template_name = "asset/category/detail.html"
    context_object_name = "category"
    permission_required = "asset.view_consumablecategory"

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
    permission_required = "asset.add_consumablecategory"


class ConsumableCategoryUpdateView(BaseUpdateView):
    model = ConsumableCategory
    fields = "__all__"
    template_name = "asset/category/update.html"
    app_name = "asset"
    url_name = "category_detail"
    permission_required = "asset.change_consumablecategory"


class ConsumableCategoryDeleteView(BaseDeleteView):
    model = ConsumableCategory
    app_name = "asset"
    url_name = "category_list"
    permission_required = "asset.delete_consumablecategory"


# Supplier views here.
class SupplierListView(BaseListView):
    model = Supplier
    template_name = "asset/supplier/list.html"
    context_object_name = "supplier"
    filterset_class = SupplierFilter
    permission_required = "asset.view_supplier"


class SupplierDetailView(BaseDetailView):
    model = Supplier
    template_name = "asset/supplier/detail.html"
    context_object_name = "supplier"
    permission_required = "asset.view_supplier"

    def get_context_data(self, **kwargs):
        supplier = self.get_object()
        context = super().get_context_data(**kwargs)
        context["consumable"] = Consumable.objects.filter(supplier_id=supplier.id)
        return context


class SupplierCreateView(BaseCreateView):
    model = Supplier
    fields = "__all__"
    template_name = "asset/supplier/create.html"
    app_name = "asset"
    url_name = "supplier_detail"
    permission_required = "asset.add_supplier"


class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    fields = "__all__"
    template_name = "asset/supplier/update.html"
    app_name = "asset"
    url_name = "supplier_detail"
    permission_required = "asset.change_supplier"


class SupplierDeleteView(BaseDeleteView):
    model = Supplier
    app_name = "asset"
    url_name = "supplier_list"
    permission_required = "asset.delete_supplier"


# Medical Equipment Views Here.
class EquipmentListView(BaseListView):
    model = Equipment
    template_name = "asset/equipment/list.html"
    context_object_name = "equipment"
    filterset_class = 0
    permission_required = "asset.view_equipment"


class EquipmentDetailView(BaseDetailView):
    model = Equipment
    template_name = "asset/equipment/detail.html"
    permission_required = "asset.view_equipment"


class EquipmentCreateView(BaseCreateView):
    model = Equipment
    fields = "__all__"
    template_name = "asset/equipment/create.html"
    app_name = "asset"
    url_name = "equipment_detail"
    permission_required = "asset.add_equipment"


class EquipmentUpdateView(BaseUpdateView):
    model = Equipment
    fields = "__all__"
    template_name = "asset/equipment/update.html"
    app_name = "asset"
    url_name = "equipment_detail"
    permission_required = "asset.change_equipment"


class EquipmentDeleteView(BaseDeleteView):
    model = Equipment
    app_name = "asset"
    url_name = "equipment_list"
    permission_required = "asset.delete_equipment"
