from django.urls import path
from .views import UserListView

app_name = "accounts"

urlpatterns = [
    path("user_list/", UserListView.as_view(), name="user_list"),
]
