from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from .models import Appointment
from django.urls import reverse_lazy
from datetime import datetime


# Create your views here.
class AppointmentListView(BaseListView):
    model = Appointment
    template_name = "booking/list.html"
    context_object_name = "appointments"
    filterset_class = 0


class AppointmentDetailView(BaseDetailView):
    model = Appointment
    template_name = "booking/detail.html"
    context_object_name = "appointment"


class AppointmentUpdateView(BaseUpdateView):
    model = Appointment
    fields = "__all__"
    template_name = "booking/update.html"
    app_name = "booking"
    url_name = "detail"


class AppointmentDeleteView(BaseDeleteView):
    model = Appointment
    app_name = "booking"
    url_name = "list"


class AppointmentCreateView(BaseCreateView):
    model = Appointment
    fields = "__all__"
    template_name = "booking/create.html"
    app_name = "booking"
    url_name = "detail"

    def form_valid(self, form):
        appointment_date = form.cleaned_data["date"]
        current_month = datetime.now().month
        appointment_month = appointment_date.month
        if current_month != appointment_month:
            form.add_error(
                "date", "Appointments can only be made for the current month."
            )
            return self.form_invalid(form)

        service = form.instance.service
        date = form.instance.date
        client = form.instance.client
        existing_appointments_count = Appointment.objects.filter(
            service=service, date=date, client=client
        ).count()
        if existing_appointments_count > 0:
            form.add_error(None, "you can only book one visit for a doctor in a day ")
            return self.form_invalid(form)

        service = form.cleaned_data["service"]
        date = form.cleaned_data["date"]
        appointment_per_day = form.instance.service.appointment_per_day
        appointments_count = Appointment.objects.filter(
            service=service, date=date
        ).count()
        if appointments_count >= appointment_per_day:
            form.add_error(
                "service",
                "This service already has maximum appointments for this date.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)
