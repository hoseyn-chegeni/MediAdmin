from .models import User
from django.urls import reverse_lazy, reverse
from .froms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from .filters import UserFilter
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)


# Create your views here.
class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter


class UserDetailView(BaseDetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"


class UserCreateView(BaseCreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/create.html"
    app_name = "accounts"
    url_name = "detail"


class UserUpdateView(BaseUpdateView):
    model = User
    fields = ("first_name", "last_name")
    template_name = "accounts/update.html"
    app_name = "accounts"
    url_name = "detail"


class UserDeleteView(BaseDeleteView):
    model = User
    template_name = "accounts/delete.html"
    app_name = "accounts"
    url_name = "list"


class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse("two_factor:login")
