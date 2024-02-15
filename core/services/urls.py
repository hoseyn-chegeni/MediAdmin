from django.urls import path
from .views import ServiceCreateView,ServiceDetailView,ServiceLDeleteView,ServiceListView,ServiceUpdateView

app_name = "services"

urlpatterns = [
    path("list/", ServiceListView.as_view(), name="list"),
    path("detail/<int:pk>/", ServiceDetailView.as_view(), name="detail"),
    path("create/", ServiceCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ServiceUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ServiceLDeleteView.as_view(), name="delete"),
]
