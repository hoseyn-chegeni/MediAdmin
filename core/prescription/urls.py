from django.urls import path 
from .views import PrescriptionHeaderCreateView, PrescriptionHeaderUpdateView

app_name = 'prescription'

urlpatterns = [
    path("create/<int:pk>/",PrescriptionHeaderCreateView.as_view(),name="create",),
    path("update/<int:pk>/", PrescriptionHeaderUpdateView.as_view(), name="update"),
]