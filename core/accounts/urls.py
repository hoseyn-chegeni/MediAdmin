from django.urls import path
from .views import UserListView,UserDetailView,UserCreateView

app_name = "accounts"

urlpatterns = [
    path("user/list/", UserListView.as_view(), name="user_list"),
    path("user/detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/create/", UserCreateView.as_view(), name="user_create"),

]
