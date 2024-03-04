from django.shortcuts import render
from base.views import BaseCreateView
from .models import Appointment
from django.urls import reverse_lazy

# Create your views here.
class AppointmentCreateView(BaseCreateView):
    model = Appointment
    fields = '__all__'
    template_name = "appointments/create.html"
    def get_success_url(self):
        return reverse_lazy('index:index')

    def form_valid(self, form):
        service = form.instance.service
        date = form.instance.date
        client = form.instance.client
        existing_appointments_count = Appointment.objects.filter(service=service, date=date, client = client).count()
        if existing_appointments_count > 0:
            form.add_error(None, "you can only book one visit for a doctor in a day ")
            return self.form_invalid(form)
        return super().form_valid(form)