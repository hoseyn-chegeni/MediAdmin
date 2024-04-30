from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Month, Session, Day
from services.models import Service
from django.urls import reverse_lazy

# Create your views here.


class CalendarView(ListView):
    template_name = 'planner/calendar.html'
    context_object_name = 'months'

    def get_queryset(self):
        return Month.objects.all().prefetch_related('day_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.kwargs["pk"]
        context["service"] = Service.objects.get(id=service_id)

        # Annotate each day with the count of sessions for the specific service
        for month in context["months"]:
            for day in month.day_set.all():
                day.session_count = Session.objects.filter(day=day, service_id=service_id).count()

        return context
    

class SessionListView(ListView):
    template_name = 'planner/list.html'
    context_object_name = 'session'

    def get_queryset(self):
        return Session.objects.filter(day_id = self.kwargs['day_pk'], service_id = self.kwargs['service_pk'])


class SessionCreateView(CreateView):
    model = Session
    fields = ['client',]
    template_name = "planner/create.html"

    def get_success_url(self):
            return reverse_lazy(
                'planner:calendar', kwargs={"pk": self.kwargs["service_pk"]}
            )
    def form_valid(self, form):
        form.instance.day = Day.objects.get(id = self.kwargs['day_pk'])
        form.instance.service = Service.objects.get(id = self.kwargs['service_pk'])
        return super().form_valid(form)