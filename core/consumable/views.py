from django.shortcuts import render, redirect, HttpResponseRedirect
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
from django.db.models import Q, F, Sum
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.utils.timezone import now
from datetime import timedelta
from .forms import (
    ConsumableCreationForm,
    ConsumableUpdateForm,
    ConsumableCategoryUpdateForm,
    ConsumableCategoryCreateForm,
    SupplierUpdateForm,
    SupplierCreateForm
)

# Create your views here.


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
        context["inventory"] = Inventory.objects.filter(
            consumable_id=consumable.id, status="در انبار"
        )
        context["expired"] = Inventory.objects.filter(
            Q(status="تمام شده") | Q(status="منقضی شده"), consumable_id=consumable.id
        )
        return context


class ConsumableCreateView(BaseCreateView):
    model = ConsumableV2
    form_class = ConsumableCreationForm
    template_name = "consumable/create.html"
    app_name = "consumable"
    url_name = "detail"
    permission_required = "consumable.add_consumablev2"


class ConsumableUpdateView(BaseUpdateView):
    model = ConsumableV2
    form_class = ConsumableUpdateForm
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
                request,
                f"تعداد {deleted_users_count[0]} مواد مصرفی با موفقیت حذف شدند.",
            )  # Add success message
        return redirect("consumable:list")


# Inventory Views.


class InventoryDetailView(BaseDetailView):
    model = Inventory
    template_name = "consumable/inventory/detail.html"
    permission_required = "consumable.view_inventory"


class InventoryUpdateView(BaseUpdateView):
    model = Inventory
    fields = [
        "quantity",
        "status",
        "supplier",
        "price",
        "purchase_date",
        "purchase_cost",
        "description",
        "image",
        "expiration_date",
        "expiration_reminder",
    ]
    template_name = "consumable/inventory/update.html"
    app_name = "consumable"
    url_name = "inventory_detail"
    permission_required = "consumable.change_inventory"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory = self.get_object()
        context["consumable"] = ConsumableV2.objects.get(id=inventory.consumable.id)
        return context


class InventoryDeleteView(DeleteView):
    model = Inventory
    permission_required = "consumable.delete_inventory"
    message = "موجودی با موفقیت حذف شد"

    def get(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()

        # Perform the delete operation directly without displaying a confirmation template

        self.object.delete()
        messages.success(self.request, self.message)
        return HttpResponseRedirect(
            reverse_lazy("consumable:detail", kwargs={"pk": self.object.consumable.pk})
        )


class InventoryCreateWithPKView(BaseCreateView):
    model = Inventory
    fields = [
        "quantity",
        "supplier",
        "price",
        "purchase_date",
        "purchase_cost",
        "description",
        "image",
        "expiration_date",
        "expiration_reminder",
    ]
    template_name = "consumable/inventory/create_with_pk.html"
    permission_required = "consumable.delete_inventory"

    def form_valid(self, form):
        form.instance.consumable_id = self.kwargs["pk"]
        form.instance.status = "در انبار"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("consumable:detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consumable"] = ConsumableV2.objects.get(id=self.kwargs["pk"])
        return context


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
    form_class = ConsumableCategoryCreateForm
    template_name = "consumable/category/create.html"
    app_name = "consumable"
    url_name = "category_detail"
    permission_required = "consumable.add_consumablecategory"


class ConsumableCategoryUpdateView(BaseUpdateView):
    model = ConsumableCategory
    form_class = ConsumableCategoryUpdateForm
    template_name = "consumable/category/update.html"
    app_name = "consumable"
    url_name = "category_detail"
    permission_required = "consumable.change_consumablecategory"


class ConsumableCategoryDeleteView(BaseDeleteView):
    model = ConsumableCategory
    app_name = "consumable"
    url_name = "category_list"
    permission_required = "consumable.delete_consumablecategory"


class DeleteSelectedCategoryView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "category_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = ConsumableCategory.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request, f"تعداد {deleted_users_count[0]} دسته بندی با موفقیت حذف شدند."
            )  # Add success message
        return redirect("consumable:category_list")


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
    permission_required = "consumable.view_supplier"

    def get_context_data(self, **kwargs):
        supplier = self.get_object()
        context = super().get_context_data(**kwargs)
        context["inventory"] = Inventory.objects.filter(supplier_id=supplier.id)
        return context


class SupplierCreateView(BaseCreateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = "consumable/supplier/create.html"
    app_name = "consumable"
    url_name = "supplier_detail"
    permission_required = "consumable.add_supplier"


class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    form_class = SupplierUpdateForm
    template_name = "consumable/supplier/update.html"
    app_name = "consumable"
    url_name = "supplier_detail"
    permission_required = "consumable.change_supplier"


class SupplierDeleteView(BaseDeleteView):
    model = Supplier
    app_name = "consumable"
    url_name = "supplier_list"
    permission_required = "consumable.delete_supplier"


class DeleteSelectedSupplierView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "supplier_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = Supplier.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request,
                f"تعداد {deleted_users_count[0]} تامین کننده با موفقیت حذف شدند.",
            )  # Add success message
        return redirect("consumable:supplier_list")


#############################
#############################
#############################
######## REPORT LIST ########
#############################
#############################
#############################


class LowStockItemListView(BaseListView):
    model = ConsumableV2
    template_name = "consumable/reports/low_stock_list.html"
    context_object_name = "consumables"
    filterset_class = ConsumableFilter
    permission_required = "consumable.view_consumablev2"

    def get_queryset(self):
        # Annotate each consumable with the current quantity in stock
        return (
            super()
            .get_queryset()
            .annotate(
                current_quantity=Sum(
                    "inventory__quantity", filter=Q(inventory__status="در انبار")
                )
            )
            .filter(current_quantity__lt=F("minimum_stock_level"))
        )


class ExpiredItemListView(ListView):
    model = Inventory
    template_name = "consumable/reports/expired_list.html"
    context_object_name = "inventory"

    def get_queryset(self):
        return super().get_queryset().filter(status="منقضی شده")


class NewSupplierListView(BaseListView):
    model = Supplier
    template_name = "consumable/reports/new_supplier_list.html"
    context_object_name = "supplier"
    filterset_class = SupplierFilter
    permission_required = "consumable.view_supplier"

    def get_queryset(self):
        one_month_ago = now() - timedelta(days=30)
        return super().get_queryset().filter(created_at__gte=one_month_ago)
