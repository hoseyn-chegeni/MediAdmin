from django.urls import path
from .views import (
    ConsumableCreateView,
    ConsumableDeleteView,
    ConsumableDetailView,
    ConsumableListView,
    ConsumableUpdateView,
)

app_name = "asset"

urlpatterns = [
    path("consumable/list/", ConsumableListView.as_view(), name="list"),
    path("consumable/detail/<int:pk>/", ConsumableDetailView.as_view(), name="detail"),
    path("consumable/create/", ConsumableCreateView.as_view(), name="create"),
    path("consumable/update/<int:pk>/", ConsumableUpdateView.as_view(), name="update"),
    path("consumable/delete/<int:pk>/", ConsumableDeleteView.as_view(), name="delete"),
]
