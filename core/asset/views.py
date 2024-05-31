from django.shortcuts import render, redirect
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Equipment
from .filters import (
    EquipmentFilter,
)
from django.contrib import messages
from django.views.generic import View
from django.utils.timezone import now
from datetime import timedelta
from .forms import EquipmentForm

# Medical Equipment Views Here.
class EquipmentListView(BaseListView):
    model = Equipment
    template_name = "asset/equipment/list.html"
    context_object_name = "equipment"
    filterset_class = EquipmentFilter
    permission_required = "asset.view_equipment"


class EquipmentDetailView(BaseDetailView):
    model = Equipment
    template_name = "asset/equipment/detail.html"
    permission_required = "asset.view_equipment"


class EquipmentCreateView(BaseCreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "asset/equipment/create.html"
    app_name = "asset"
    url_name = "equipment_detail"
    permission_required = "asset.add_equipment"


class EquipmentUpdateView(BaseUpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "asset/equipment/update.html"
    app_name = "asset"
    url_name = "equipment_detail"
    permission_required = "asset.change_equipment"


class EquipmentDeleteView(BaseDeleteView):
    model = Equipment
    app_name = "asset"
    url_name = "equipment_list"
    permission_required = "asset.delete_equipment"


class DeleteSelectedEquipmentView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "equipment_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = Equipment.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request,
                f"تعداد {deleted_users_count[0]} تجهیزات پزشکی با موفقیت حذف شدند.",
            )  # Add success message
        return redirect("asset:equipment_list")


#############################
#############################
#############################
######## REPORT LIST ########
#############################
#############################
#############################


class InUseEquipmentsView(BaseListView):
    model = Equipment
    template_name = "asset/equipment/reports/in_use_list.html"
    context_object_name = "equipment"
    filterset_class = EquipmentFilter
    permission_required = "asset.view_equipment"

    def get_queryset(self):
        return super().get_queryset().filter(in_use=True)


class NewEquipmentsView(BaseListView):
    template_name = "asset/equipment/reports/new_list.html"
    context_object_name = "equipment"
    filterset_class = EquipmentFilter
    permission_required = "asset.view_equipment"

    def get_queryset(self):
        one_month_ago = now() - timedelta(days=30)
        return super().get_queryset().filter(created_at__gte=one_month_ago)
