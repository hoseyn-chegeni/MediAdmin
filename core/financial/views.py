from django.shortcuts import render
from base.views import BaseCreateView,BaseDeleteView,BaseDetailView,BaseListView,BaseUpdateView
from .models import Financial
from .filters import FinancialFilter


# Create your views here.
class FinancialListView(BaseListView):
    model = Financial
    template_name = "financial/list.html"
    context_object_name = "financial"
    filterset_class = FinancialFilter

class FinancialCreateView(BaseCreateView):
    model = Financial
    fields = "__all__"
    template_name = "financial/create.html"
    app_name = "financial"
    url_name = "detail"


class FinancialDetailView(BaseDetailView):
    model = Financial
    template_name = "financial/detail.html"
    context_object_name = "financial"

class FinancialUpdateView(BaseUpdateView):
    model = Financial
    fields = "__all__"
    template_name = "financial/update.html"
    app_name = "financial"
    url_name = "detail"

class FinancialDeleteView(BaseDeleteView):
    model = Financial
    template_name = "financial/delete.html"
    app_name = "financial"
    url_name = "list"