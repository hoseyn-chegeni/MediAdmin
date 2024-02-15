from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy


# Create your views here.
class BaseListView(LoginRequiredMixin, FilterView):
    pass


class BaseCreateView(LoginRequiredMixin, CreateView):
    app_name = ""

    def get_success_url(self):
        return reverse_lazy(f"{self.app_name}:detail", kwargs={"pk": self.object.pk})


class BaseDetailView(LoginRequiredMixin, DetailView):
    pass


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    app_name = ""

    def get_success_url(self):
        return reverse_lazy(f"{self.app_name}:detail", kwargs={"pk": self.object.pk})


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    app_name = ""

    def get_success_url(self):
        return reverse_lazy(f"{self.app_name}:list")
