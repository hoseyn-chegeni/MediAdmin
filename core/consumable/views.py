from django.shortcuts import render
from base.views import BaseCreateView,BaseDeleteView,BaseDetailView,BaseUpdateView,BaseListView
from .models import ConsumableV2
from django.views.generic import ListView
# Create your views here.
#Consumable Views.
class ConsumableListView(ListView):
    model = ConsumableV2
    template_name = "consumable/list.html"
    context_object_name = "consumable"


class ConsumableDetailView(BaseDetailView):
    model = ConsumableV2
    template_name = "consumable/detail.html"
    context_object_name = "consumable"
    permission_required = "consumable.view_consumablev2"


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
    url_name = 'list'
    permission_required = "consumable.delete_consumablev2"