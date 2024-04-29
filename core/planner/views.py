from django.shortcuts import render
from django.views.generic import ListView
from .models import Month
from services.models import Service

# Create your views here.

class CalendarView(ListView):
    template_name = 'planner/calendar.html'
    context_object_name = 'months'

    def get_queryset(self):
        return Month.objects.all().prefetch_related('day_set')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = Service.objects.get(id=self.kwargs["pk"])
        return context