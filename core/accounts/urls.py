from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserLogoutView,
    ProfileView,
    ChangePasswordView,
    SuspendUserListView,
    SuspendUserView,
    ReactiveUserView,
)

app_name = "accounts"

urlpatterns = [
    path("user/list/", UserListView.as_view(), name="user_list"),
    path("suspend_user/list/", SuspendUserListView.as_view(), name="suspend_user_list"),
    path("user/detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("suspend/<int:pk>/", SuspendUserView.as_view(), name="suspend"),
    path("reactive/<int:pk>/", ReactiveUserView.as_view(), name="reactive"),
]
