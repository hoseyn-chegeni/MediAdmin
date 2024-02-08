from django.shortcuts import render
from .models import User
from django.views.generic import ListView


# Create your views here.
class UserListView(ListView):
    model = User
    template_name = "accounts/user_list.html"
    permission_required = "accounts.view_user"
    context_object_name = "users"


class UserDetailView:
    pass


class UserCreateView:
    pass


class UserUpdateView:
    pass


class UserDeleteView:
    pass
