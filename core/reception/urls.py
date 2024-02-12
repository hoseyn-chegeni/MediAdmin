from django.urls import path 
from .views import ReceptionCreateView, ReceptionListView, ReceptionDetailView

app_name = 'reception'

urlpatterns =[
    path("list/", ReceptionListView.as_view(), name="list"),
    path("detail/<int:pk>/", ReceptionDetailView.as_view(), name="detail"),
    path("create/", ReceptionCreateView.as_view(), name="create"),
]