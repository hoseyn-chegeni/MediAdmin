from django.urls import path
from .views import UserListView,UserDetailView

app_name = "accounts"

urlpatterns = [
    path("user/list/", UserListView.as_view(), name="user_list"),
    path("user/detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
