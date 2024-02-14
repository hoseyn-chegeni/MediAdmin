from django.shortcuts import render
from base.views import BaseListView, BaseCreateView,BaseDeleteView,BaseDetailView,BaseUpdateView
from .models import Insurance
from django.urls import reverse_lazy
from .filters import InsuranceFilter

# Create your views here.
class InsuranceListView(BaseListView):
    model = Insurance
    template_name = "insurance/list.html"
    context_object_name = "insurance"
    filterset_class = InsuranceFilter



class InsuranceCreateView(BaseCreateView):
    model = Insurance
    fields = "__all__"
    template_name = "insurance/create.html"

    def get_success_url(self):
        return reverse_lazy("insurance:detail", kwargs={"pk": self.object.pk})

class InsuranceDetailView(BaseDetailView):
    model = Insurance
    template_name = 'insurance/detail.html'
    context_object_name = 'insurance'

class InsuranceUpdateView(BaseUpdateView):
    model = Insurance
    fields = '__all__'
    template_name = "insurance/update.html"

    def get_success_url(self):
        return reverse_lazy("insurance:detail", kwargs={"pk": self.object.pk})

class InsuranceDeleteView(BaseDeleteView):
    model = Insurance
    template_name = "insurance/delete.html"
    success_url = reverse_lazy("insurance:list")
