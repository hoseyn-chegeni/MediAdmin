from django.urls import path
from .views import IndexView, ClientCaseIdSearchView, ClientNationalIdSearchView

app_name = "index"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "national_id/search/",
        ClientNationalIdSearchView.as_view(),
        name="national_id_search",
    ),
    path("case_id/search/", ClientCaseIdSearchView.as_view(), name="case_id_search"),
]
