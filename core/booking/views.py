from django.shortcuts import render
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from .models import Appointment, PackageAppointment
from django.urls import reverse_lazy
from datetime import datetime
from .filters import AppointmentFilter, PackageAppointmentFilter
from datetime import date

# Create your views here.
class AppointmentListView(BaseListView):
    model = Appointment
    template_name = "booking/list.html"
    context_object_name = "appointments"
    filterset_class = AppointmentFilter
    permission_required = "booking.view_appointment"

class TodaysAppointmentListView(BaseListView):
    model = Appointment
    template_name = "booking/today_list.html"
    context_object_name = "appointments"
    filterset_class = AppointmentFilter
    permission_required = "booking.view_appointment"

    def get_queryset(self):
        today_date = date.today()
        queryset = super().get_queryset().filter(date=today_date)
        return queryset


class AppointmentDetailView(BaseDetailView):
    model = Appointment
    template_name = "booking/detail.html"
    context_object_name = "appointment"
    permission_required = "booking.view_appointment"


class AppointmentUpdateView(BaseUpdateView):
    model = Appointment
    fields = "__all__"
    template_name = "booking/update.html"
    app_name = "booking"
    url_name = "detail"
    permission_required = "booking.change_appointment"


class AppointmentDeleteView(BaseDeleteView):
    model = Appointment
    app_name = "booking"
    url_name = "list"
    permission_required = "booking.delete_appointment"


class AppointmentCreateView(BaseCreateView):
    model = Appointment
    fields = "__all__"
    template_name = "booking/create.html"
    app_name = "booking"
    url_name = "detail"
    permission_required = "booking.add_appointment"

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

        service = form.instance.service
        appointment_date = form.cleaned_data["date"]

        # Check if appointment date falls on any selected off day
        off_days = service.off_days.all()
        for off_day in off_days:
            if appointment_date.weekday() == off_day.day_of_week:
                form.add_error(
                    "date", "Appointments cannot be scheduled on this day, (OFF)."
                )
                return self.form_invalid(form)

        if appointment_date < datetime.now().date():
            form.add_error("date", "Appointments cannot be scheduled for past dates.")
            return self.form_invalid(form)
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# PACKAGE APPOINTMENT VIEWS HERE.
class PackageAppointmentListView(BaseListView):
    model = PackageAppointment
    template_name = "booking/package/list.html"
    context_object_name = "appointments"
    filterset_class = PackageAppointmentFilter
    permission_required = "booking.view_packageappointment"


class PackageAppointmentCreateView(BaseCreateView):
    model = PackageAppointment
    fields = "__all__"
    template_name = "booking/package/create.html"
    app_name = "booking"
    url_name = "package_detail"
    permission_required = "booking.add_packageappointment"

    def form_valid(self, form):
        if form.instance.package.total_price < form.instance.prepayment:
            form.add_error(
                "prepayment",
                f"مبلغ پیش پرداخت از مبلغ کل سرویس ({form.instance.package.total_price} ) بیشتر است .",
            )
            return self.form_invalid(form)
        return super().form_valid(form)


class PackageAppointmentDetailViews(BaseDetailView):
    model = PackageAppointment
    template_name = "booking/package/detail.html"
    permission_required = "booking.view_packageappointment"


class PackageAppointmentUpdateView(BaseUpdateView):
    model = PackageAppointment
    fields = "__all__"
    template_name = "booking/package/update.html"
    app_name = "booking"
    url_name = "package_detail"
    permission_required = "booking.change_packageappointment"


class PackageAppointmentDeleteView(BaseDeleteView):
    model = PackageAppointment
    app_name = "booking"
    url_name = "package_list"
    permission_required = "booking.delete_packageappointment"
