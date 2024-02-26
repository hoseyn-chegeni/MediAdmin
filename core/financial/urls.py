from django.urls import path
from .views import FinancialCreateView,FinancialDeleteView,FinancialDetailView,FinancialListView,FinancialUpdateView

app_name = 'financial'

urlpatterns = [
    path("list/", FinancialListView.as_view(), name="list"),
    path("detail/<int:pk>/", FinancialDetailView.as_view(), name="detail"),
    path("create/", FinancialCreateView.as_view(), name="create"),
    path("update/<int:pk>/", FinancialUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", FinancialDeleteView.as_view(), name="delete"),
]