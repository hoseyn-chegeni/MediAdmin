from django.urls import path
from .views import (
    FinancialCreateView,
    FinancialDeleteView,
    FinancialDetailView,
    FinancialListView,
    FinancialUpdateView,
    OfficeExpensesCreateView,
    OfficeExpensesDeleteView,
    OfficeExpensesDetailView,
    OfficeExpensesListView,
    OfficeExpensesUpdateView,
)

app_name = "financial"

urlpatterns = [
    path("list/", FinancialListView.as_view(), name="list"),
    path("detail/<int:pk>/", FinancialDetailView.as_view(), name="detail"),
    path("create/", FinancialCreateView.as_view(), name="create"),
    path("update/<int:pk>/", FinancialUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", FinancialDeleteView.as_view(), name="delete"),
    # OFFICE EXPENSES
    path(
        "office_expenses_list/",
        OfficeExpensesListView.as_view(),
        name="office_expenses_list",
    ),
    path(
        "office_expenses_detail/<int:pk>/",
        OfficeExpensesDetailView.as_view(),
        name="office_expenses_detail",
    ),
    path(
        "office_expenses_create/",
        OfficeExpensesCreateView.as_view(),
        name="office_expenses_create",
    ),
    path(
        "office_expenses_update/<int:pk>/",
        OfficeExpensesUpdateView.as_view(),
        name="office_expenses_update",
    ),
    path(
        "office_expenses_delete/<int:pk>/",
        OfficeExpensesDeleteView.as_view(),
        name="office_expenses_delete",
    ),
]
