from django.shortcuts import render
from base.views import BaseCreateView
from .models import Appointment
from django.urls import reverse_lazy
from datetime import datetime

# Create your views here.
class AppointmentCreateView(BaseCreateView):
    model = Appointment
    fields = '__all__'
    template_name = "appointments/create.html"
    def get_success_url(self):
        return reverse_lazy('index:index')

    def form_valid(self, form):
        appointment_date = form.cleaned_data['date']
        current_month = datetime.now().month
        appointment_month = appointment_date.month
        if current_month != appointment_month:
            form.add_error('date', "Appointments can only be made for the current month.")
            return self.form_invalid(form)

        service = form.instance.service
        date = form.instance.date
        client = form.instance.client
        existing_appointments_count = Appointment.objects.filter(service=service, date=date, client = client).count()
        if existing_appointments_count > 0:
            form.add_error(None, "you can only book one visit for a doctor in a day ")
            return self.form_invalid(form)
        

        service = form.cleaned_data['service']
        date = form.cleaned_data['date']
        appointments_count = Appointment.objects.filter(service=service, date=date).count()
        if appointments_count >= 3:
            form.add_error('service', "This service already has maximum appointments for this date.")
            return self.form_invalid(form)

        return super().form_valid(form)