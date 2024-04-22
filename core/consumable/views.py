from django.shortcuts import render, redirect
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from .models import ConsumableV2, Inventory, ConsumableCategory, Supplier
from django.views.generic import ListView
from .filters import ConsumableFilter, ConsumableCategoryFilter, SupplierFilter
from django.views import View
from django.contrib import messages
from django.db.models import Q
# Create your views here.
# Consumable Views.


class ConsumableListView(BaseListView):
    model = ConsumableV2
    template_name = "consumable/list.html"
    context_object_name = "consumable"
    filterset_class = ConsumableFilter
    permission_required = "consumable.view_consumablev2"


class ConsumableDetailView(BaseDetailView):
    model = ConsumableV2
    template_name = "consumable/detail.html"
    context_object_name = "consumable"
    permission_required = "consumable.view_consumablev2"

    def get_context_data(self, **kwargs):
        consumable = self.get_object()
        context = super().get_context_data(**kwargs)
        context["inventory"] = Inventory.objects.filter(consumable_id=consumable.id, status =  "در انبار")
        context["expired"] = Inventory.objects.filter(
            Q(status="تمام شده") | Q(status="منقضی شده"),
            consumable_id=consumable.id
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

class DeleteSelectedConsumableView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "consumable_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = ConsumableV2.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request, f"تعداد {deleted_users_count[0]} مواد مصرفی با موفقیت حذف شدند."
            )  # Add success message
        return redirect("consumable:list")



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
    filterset_class = ConsumableCategoryFilter
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


# Supplier views here.
class SupplierListView(BaseListView):
    model = Supplier
    template_name = "consumable/supplier/list.html"
    context_object_name = "supplier"
    filterset_class = SupplierFilter
    permission_required = "consumable.view_supplier"


class SupplierDetailView(BaseDetailView):
    model = Supplier
    template_name = "consumable/supplier/detail.html"
    context_object_name = "supplier"
    permission_required = "consumable.view_supplier"

    def get_context_data(self, **kwargs):
        supplier = self.get_object()
        context = super().get_context_data(**kwargs)
        context["consumable"] = ConsumableV2.objects.filter(supplier_id=supplier.id)
        return context


class SupplierCreateView(BaseCreateView):
    model = Supplier
    fields = "__all__"
    template_name = "consumable/supplier/create.html"
    app_name = "consumable"
    url_name = "supplier_detail"
    permission_required = "consumable.add_supplier"


class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    fields = "__all__"
    template_name = "consumable/supplier/update.html"
    app_name = "consumable"
    url_name = "supplier_detail"
    permission_required = "consumable.change_supplier"


class SupplierDeleteView(BaseDeleteView):
    model = Supplier
    app_name = "consumable"
    url_name = "supplier_list"
    permission_required = "consumable.delete_supplier"

