from django.shortcuts import render
from base.views import BaseCreateView,BaseListView,BaseDetailView
from .models import Reception
from django.urls import reverse_lazy
from .filters import ReceptionFilter

# Create your views here.
class ReceptionListView(BaseListView):
    model = Reception
    template_name = "reception/list.html"
    context_object_name = "reception"
    filterset_class = ReceptionFilter


class ReceptionCreateView(BaseCreateView):
    model = Reception
    fields =[
        "reason","payment_type","payment_status","client"
    ]
    template_name = "reception/create.html"

    def get_success_url(self):
        return reverse_lazy("reception:detail", kwargs={"pk": self.object.pk})
    
    # def form_valid(self, form):
    #     form.instance.client = self.object.pk
    #     return super().form_valid(form)



class ReceptionDetailView(BaseDetailView):
    model = Reception
    template_name = 'reception/detail.html'
    context_object_name = 'reception'