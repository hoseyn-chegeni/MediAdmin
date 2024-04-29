from django.shortcuts import render
from django.views.generic import ListView
from .models import Month

# Create your views here.

class CalendarView(ListView):
    template_name = 'calendar/calendar.html'
    context_object_name = 'months'

    def get_queryset(self):
        return Month.objects.all().prefetch_related('day_set')
