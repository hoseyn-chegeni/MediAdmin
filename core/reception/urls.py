from django.urls import path
from .views import (
    ReceptionCreateView,
    ReceptionListView,
    ReceptionDetailView,
    ReceptionCreateViewUsingProfile,
    ReceptionDeleteView,
    ReceptionUpdateView,
    WaitingListView,
    CompleteReceptionView,
)

app_name = "reception"

urlpatterns = [
    path("list/", ReceptionListView.as_view(), name="list"),
    path("detail/<int:pk>/", ReceptionDetailView.as_view(), name="detail"),
    path("create/", ReceptionCreateView.as_view(), name="create"),
    path(
        "create/<int:pk>/",
        ReceptionCreateViewUsingProfile.as_view(),
        name="reception_create_using_profile",
    ),
    path("update/<int:pk>/", ReceptionUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ReceptionDeleteView.as_view(), name="delete"),
    path("waiting_list/", WaitingListView.as_view(), name="waiting_list"),
    path("complete/<int:pk>/", CompleteReceptionView.as_view(), name="complete"),

]
