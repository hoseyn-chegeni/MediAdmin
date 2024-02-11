from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView


# Create your views here.
class BaseListView(LoginRequiredMixin, FilterView):
    pass


class BaseCreateView(LoginRequiredMixin, CreateView):
    pass


class BaseDetailView(LoginRequiredMixin, DetailView):
    pass


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    pass


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    pass
