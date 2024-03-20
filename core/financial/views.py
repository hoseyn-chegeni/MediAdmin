from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Financial, OfficeExpenses
from .filters import FinancialFilter, OfficeExpensesFilter


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financial = self.get_object()
        client = financial.reception.client
        context["client"] = client
        return context


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


# OFFICE EXPENSES VIEWS HERE.
class OfficeExpensesListView(BaseListView):
    model = OfficeExpenses
    template_name = "financial/office_expenses/list.html"
    filterset_class = OfficeExpensesFilter
    context_object_name = "office_expenses"


class OfficeExpensesCreateView(BaseCreateView):
    model = OfficeExpenses
    fields = [
        "user",
        "date",
        "subject",
        "amount",
        "recipient_name",
        "payment_method",
        "description",
        "attachment",
    ]
    template_name = "financial/office_expenses/create.html"
    app_name = "financial"
    url_name = "office_expenses_detail"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OfficeExpensesDetailView(BaseDetailView):
    model = OfficeExpenses
    template_name = "financial/office_expenses/detail.html"


class OfficeExpensesUpdateView(BaseUpdateView):
    model = OfficeExpenses
    template_name = "financial/office_expenses/update.html"
    fields = [
        "user",
        "date",
        "subject",
        "amount",
        "recipient_name",
        "payment_method",
        "description",
        "attachment",
    ]

    app_name = "financial"
    url_name = "office_expenses_detail"


class OfficeExpensesDeleteView(BaseDeleteView):
    model = OfficeExpenses
    app_name = "financial"
    url_name = "office_expenses_list"
