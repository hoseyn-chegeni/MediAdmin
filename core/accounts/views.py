from .models import User
from django.urls import reverse_lazy, reverse
from .froms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from django_filters.views import FilterView
from .filters import UserFilter
from base.views import BaseCreateView,BaseDeleteView,BaseDetailView,BaseListView,BaseUpdateView


# Create your views here.
class UserListView(FilterView):
    model = User
    template_name = "accounts/list.html"
    permission_required = "accounts.view_user"
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

    def get_success_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.object.pk})


class UserUpdateView(BaseUpdateView):
    model = User
    fields = ("first_name", "last_name")
    template_name = "accounts/update.html"

    def get_success_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.object.pk})


class UserDeleteView(BaseDeleteView):
    model = User
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("accounts:user_list")



class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse("two_factor:login")
