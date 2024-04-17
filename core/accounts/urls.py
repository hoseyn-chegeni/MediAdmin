from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    ChangePasswordView,
    SuspendUserView,
    ReactiveUserView,
    UserSMSListView,
    UserSentSMSListView,
    LoginAsUserView,
    DeleteSelectedUsersView,
    logout_view,
)

app_name = "accounts"

urlpatterns = [
    path("user/list/", UserListView.as_view(), name="user_list"),
    path("user/detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/create/", UserCreateView.as_view(), name="user_create"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("logout/", logout_view, name="logout"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("suspend/<int:pk>/", SuspendUserView.as_view(), name="suspend"),
    path("reactive/<int:pk>/", ReactiveUserView.as_view(), name="reactive"),
    path(
        "user/<int:pk>/sms_log/",
        UserSMSListView.as_view(),
        name="user-sms_log",
    ),
    path(
        "user/<int:pk>/sent_sms_log/",
        UserSentSMSListView.as_view(),
        name="user_sent_sms_log",
    ),
    path("login-as-user/<int:pk>/", LoginAsUserView.as_view(), name="login_as_user"),
    path(
        "users/delete/", DeleteSelectedUsersView.as_view(), name="delete_selected_users"
    ),
]
