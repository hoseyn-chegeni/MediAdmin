from django.urls import path
from .views import InsuranceCreateView,InsuranceDetailView,InsuranceListView,InsuranceDeleteView,InsuranceUpdateView

app_name = "insurance"

urlpatterns = [
    path("list/", InsuranceListView.as_view(), name="list"),
    path("detail/<int:pk>/", InsuranceDetailView.as_view(), name="detail"),
    path("create/", InsuranceCreateView.as_view(), name="create"),
    path("update/<int:pk>/", InsuranceUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", InsuranceDeleteView.as_view(), name="delete"),
]
