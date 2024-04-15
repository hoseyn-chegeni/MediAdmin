from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import  Equipment
from .filters import (
    EquipmentFilter,
)


# class UpdateInventoryTrackingNumberViews(BaseUpdateView):
#     model = Consumable
#     fields = ["inventory_tracking_number"]
#     template_name = "asset/update_inventory_tracking_number.html"
#     app_name = "asset"
#     url_name = "detail"
#     permission_required = "asset.change_consumable"


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
