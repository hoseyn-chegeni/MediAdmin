from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from .models import Financial, OfficeExpenses
from .filters import FinancialFilter, OfficeExpensesFilter
from .models import ConsumablePrice
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.
class FinancialListView(BaseListView):
    model = Financial
    template_name = "financial/list.html"
    context_object_name = "financial"
    filterset_class = FinancialFilter
    permission_required = "financial.view_financial"


class FinancialDetailView(BaseDetailView):
    model = Financial
    template_name = "financial/detail.html"
    permission_required = "financial.view_financial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financial = self.get_object()
        client = financial.reception.client
        consumable = ConsumablePrice.objects.filter(reception_id=financial.reception.id)
        context["consumable"] = consumable

        context["client"] = client
        return context


class FinancialCreateView(BaseCreateView):
    model = Financial
    fields = "__all__"
    template_name = "financial/create.html"
    app_name = "financial"
    url_name = "detail"
    permission_required = "financial.add_financial"


class FinancialUpdateView(BaseUpdateView):
    model = Financial
    fields = ["service_price", "consumable_price"]
    template_name = "financial/update.html"
    app_name = "financial"
    url_name = "detail"
    permission_required = "financial.change_financial"

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
    permission_required = "financial.delete_financial"


class InvoiceView(BaseDetailView):
    model = Financial
    template_name = "financial/invoice.html"
    permission_required = "financial.view_financial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financial = self.get_object()
        client = financial.reception.client
        consumable = ConsumablePrice.objects.filter(reception_id=financial.reception.id)
        context["consumable"] = consumable

        context["client"] = client
        return context


class UpdatePaymentStatusView(LoginRequiredMixin, View):
    def get(self, request, pk):
        invoice = Financial.objects.filter(pk=pk).first()
        if invoice :
            invoice.payment_status = "پرداخت شده"
            messages.success(
                self.request,
                f"وضعیت فاکتور با موفقیت به حالت پرداخت شده درآمد"
            )
            invoice.save()

        return HttpResponseRedirect(
            reverse_lazy("financial:detail", kwargs={"pk": invoice.pk})
        )



# OFFICE EXPENSES VIEWS HERE.
class OfficeExpensesListView(BaseListView):
    model = OfficeExpenses
    template_name = "financial/office_expenses/list.html"
    filterset_class = OfficeExpensesFilter
    context_object_name = "office_expenses"
    permission_required = "financial.view_officeexpenses"


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
    permission_required = "financial.add_officeexpenses"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OfficeExpensesDetailView(BaseDetailView):
    model = OfficeExpenses
    template_name = "financial/office_expenses/detail.html"
    permission_required = "financial.view_officeexpenses"


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
    permission_required = "financial.change_officeexpenses"


class OfficeExpensesDeleteView(BaseDeleteView):
    model = OfficeExpenses
    app_name = "financial"
    url_name = "office_expenses_list"
    permission_required = "financial.delete_officeexpenses"


class DeleteSelectedFinancialView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "financial_ids"
            )  # Get the list of selected user IDs from the form
            Financial.objects.filter(id__in=user_ids).delete()  # Delete selected users
        return redirect("financial:list")


class DeleteSelectedOfficeExpensesView(View):
    def post(self, request):
        if request.method == "POST":
            ids = request.POST.getlist(
                "ids"
            )  # Get the list of selected user IDs from the form
            OfficeExpenses.objects.filter(id__in=ids).delete()  # Delete selected users
        return redirect("financial:office_expenses_list")
