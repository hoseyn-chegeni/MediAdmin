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
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"


    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active=True)


class SuspendUserListView(BaseListView):
    model = User
    template_name = "accounts/suspend_list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active=False)


class UserDetailView(BaseDetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"
    permission_required = "accounts.view_user"


class UserCreateView(BaseCreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/create.html"
    app_name = "accounts"
    url_name = "user_detail"
    permission_required = "accounts.add_user"


class UserUpdateView(BaseUpdateView):
    model = User
    fields = "__all__"
    template_name = "accounts/update.html"
    app_name = "accounts"
    url_name = "user_detail"
    permission_required = "accounts.change_user"


class UserDeleteView(BaseDeleteView):
    model = User
    app_name = "accounts"
    url_name = "user_list"
    permission_required = "accounts.delete_user"


class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse("two_factor:login")


class ProfileView(BaseDetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile"
    permission_required = "accounts.view_user"


    def get_object(self, queryset=None):
        # Assuming UserProfile is associated with User model through a OneToOneField named 'user'
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    success_message = "Password Successfully Changed"
    template_name = (
        "accounts/change_password.html"  # Your template for the change password form
    )
    success_url = reverse_lazy(
        "accounts:profile"
    )  # URL to redirect to after successfully changing password

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message


class SuspendUserView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            user.is_active = False
            messages.success(
                self.request, f"User Suspended '{user.email}' successfully!"
            )
            user.save()
        return HttpResponseRedirect(reverse_lazy("accounts:user_list"))


class ReactiveUserView(View):
    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            user.is_active = True
            messages.success(
                self.request, f"User Reactive '{user.email}' successfully!"
            )
            user.save()
        return HttpResponseRedirect(reverse_lazy("accounts:suspend_user_list"))
