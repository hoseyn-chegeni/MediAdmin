from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import User
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView


# Create your views here.
class UserListView(ListView):
    model = User
    template_name = "accounts/list.html"
    permission_required = "accounts.view_user"
    context_object_name = "users"


class UserDetailView(DetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"


class UserCreateView:
    pass


class UserUpdateView:
    pass


class UserDeleteView:
    pass
