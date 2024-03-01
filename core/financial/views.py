from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
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
    fields = ["service_price", "consumable_price"]
    template_name = "financial/update.html"
    app_name = "financial"
    url_name = "detail"

    def form_valid(self, form):
        financial = form.save(commit=False)
        # Calculate total amount including tax
        total_amount_before_tax = financial.service_price + financial.consumable_price
        total_amount_after_tax = total_amount_before_tax * (1 + financial.tax_rate)
        financial.total_amount = total_amount_after_tax
        financial.save()
        return super().form_valid(form)


class FinancialDeleteView(BaseDeleteView):
    model = Financial
    app_name = "financial"
    url_name = "list"
