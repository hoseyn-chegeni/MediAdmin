from typing import Any
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Appointment
from datetime import date


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        appointment_count = Appointment.objects.filter(date=today).count()
        complete_appointment_count = Appointment.objects.filter(date=today, status="پذیرش شده").count()

        if appointment_count != 0:
            complete_percentage = round((complete_appointment_count / appointment_count) * 100)
        else:
            complete_percentage = 0

        context['appointment_count'] = appointment_count
        context['complete_percentage'] = complete_percentage
        return context


