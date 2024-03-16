from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy


# Create your views here.
class BaseListView(LoginRequiredMixin, FilterView):
    def get_paginate_by(self, queryset):
        # Get the value for paginate_by dynamically (e.g., from a form input or session)
        # Example: Set paginate_by to a user-selected value stored in session
        user_selected_value = self.request.session.get(
            "items_per_page", 10
        )  # Default to 10
        return user_selected_value


class BaseCreateView(LoginRequiredMixin, CreateView):
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.pk}
        )


class BaseDetailView(LoginRequiredMixin, DetailView):
    pass


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.pk}
        )


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(f"{self.app_name}:{self.url_name}")
