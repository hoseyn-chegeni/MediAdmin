from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientDeleteView,
    ClientDetailView,
    ClientUpdateView,
)

app_name = "client"

urlpatterns = [
    path("list/", ClientListView.as_view(), name="list"),
    path("detail/<int:pk>/", ClientDetailView.as_view(), name="detail"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ClientUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete"),
]
