from django.shortcuts import render
from django.views.generic import ListView, DeleteView,DetailView,CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class BaseListView(LoginRequiredMixin, ListView):
    pass

class BaseCreateView(LoginRequiredMixin, CreateView):
    pass

class BaseDetailView(LoginRequiredMixin, DetailView):
    pass

class BaseUpdateView(LoginRequiredMixin, UpdateView):
    pass

class BaseDeleteView(LoginRequiredMixin, DeleteView):
    pass


