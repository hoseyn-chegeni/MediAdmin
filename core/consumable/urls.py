from django.urls import path
from .views import ConsumableCreateView,ConsumableListView,ConsumableDeleteView,ConsumableDetailView,ConsumableUpdateView

app_name = 'consumable'


urlpatterns = [
    path("list/", ConsumableListView.as_view(), name="list"),
    path("detail/<int:pk>/", ConsumableDetailView.as_view(), name="detail"),
    path("create/", ConsumableCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ConsumableUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ConsumableDeleteView.as_view(), name="delete"),
]