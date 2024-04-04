from django.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import User
from client.models import Client
from doctor.models import Doctor
from services.models import Service, Package
from booking.models import Appointment, PackageAppointment
from reception.models import Reception
from financial.models import Financial, OfficeExpenses
from logs.models import ClientSMSLog
from prescription.models import Prescription
from asset.models import Consumable, Supplier, Equipment
from insurance.models import Insurance
from datetime import date

# Create your views here.
class BaseListView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    def get_paginate_by(self, queryset):
        # Get the value for paginate_by dynamically (e.g., from a form input or session)
        # Example: Set paginate_by to a user-selected value stored in session
        user_selected_value = self.request.session.get(
            "items_per_page", 10
        )  # Default to 10
        return user_selected_value
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_date = date.today()
        context["user_count"] = User.objects.count()
        context["client_count"] = Client.objects.count()
        context["client_sms_count"] = ClientSMSLog.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["package_appointment_count"] = PackageAppointment.objects.count()
        context["todays_appointment_count"] = Appointment.objects.filter(date=today_date).count()
        context["reception_count"] = Reception.objects.count()
        context["financial_count"] = Financial.objects.count()
        context["office_expenses_count"] = OfficeExpenses.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["service_count"] = Service.objects.count()
        context["package_count"] = Package.objects.count()
        context["prescription_count"] = Prescription.objects.count()
        context["consumable_count"] = Consumable.objects.count()
        context["supplier_count"] = Supplier.objects.count()
        context["equipment_count"] = Equipment.objects.count()
        context["insurance_count"] = Insurance.objects.count()
        return context

class BaseCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    success_message = ""
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.pk}
        )

    def get_success_message(self, cleaned_data):
        return "با موفقیت افزوده شد"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_date = date.today()
        context["user_count"] = User.objects.count()
        context["client_count"] = Client.objects.count()
        context["client_sms_count"] = ClientSMSLog.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["package_appointment_count"] = PackageAppointment.objects.count()
        context["todays_appointment_count"] = Appointment.objects.filter(date=today_date).count()
        context["reception_count"] = Reception.objects.count()
        context["financial_count"] = Financial.objects.count()
        context["office_expenses_count"] = OfficeExpenses.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["service_count"] = Service.objects.count()
        context["package_count"] = Package.objects.count()
        context["prescription_count"] = Prescription.objects.count()
        context["consumable_count"] = Consumable.objects.count()
        context["supplier_count"] = Supplier.objects.count()
        context["equipment_count"] = Equipment.objects.count()
        context["insurance_count"] = Insurance.objects.count()
        return context


class BaseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_date = date.today()
        context["user_count"] = User.objects.count()
        context["client_count"] = Client.objects.count()
        context["client_sms_count"] = ClientSMSLog.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["package_appointment_count"] = PackageAppointment.objects.count()
        context["todays_appointment_count"] = Appointment.objects.filter(date=today_date).count()
        context["reception_count"] = Reception.objects.count()
        context["financial_count"] = Financial.objects.count()
        context["office_expenses_count"] = OfficeExpenses.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["service_count"] = Service.objects.count()
        context["package_count"] = Package.objects.count()
        context["prescription_count"] = Prescription.objects.count()
        context["consumable_count"] = Consumable.objects.count()
        context["supplier_count"] = Supplier.objects.count()
        context["equipment_count"] = Equipment.objects.count()
        context["insurance_count"] = Insurance.objects.count()
        return context


class BaseUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.pk}
        )

    def get_success_message(self, cleaned_data):
        return "با موفقیت ویرایش شد"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_date = date.today()
        context["user_count"] = User.objects.count()
        context["client_count"] = Client.objects.count()
        context["client_sms_count"] = ClientSMSLog.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["package_appointment_count"] = PackageAppointment.objects.count()
        context["todays_appointment_count"] = Appointment.objects.filter(date=today_date).count()
        context["reception_count"] = Reception.objects.count()
        context["financial_count"] = Financial.objects.count()
        context["office_expenses_count"] = OfficeExpenses.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["service_count"] = Service.objects.count()
        context["package_count"] = Package.objects.count()
        context["prescription_count"] = Prescription.objects.count()
        context["consumable_count"] = Consumable.objects.count()
        context["supplier_count"] = Supplier.objects.count()
        context["equipment_count"] = Equipment.objects.count()
        context["insurance_count"] = Insurance.objects.count()
        return context


class BaseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = "delete.html"
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(f"{self.app_name}:{self.url_name}")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_date = date.today()
        context["user_count"] = User.objects.count()
        context["client_count"] = Client.objects.count()
        context["client_sms_count"] = ClientSMSLog.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["package_appointment_count"] = PackageAppointment.objects.count()
        context["todays_appointment_count"] = Appointment.objects.filter(date=today_date).count()
        context["reception_count"] = Reception.objects.count()
        context["financial_count"] = Financial.objects.count()
        context["office_expenses_count"] = OfficeExpenses.objects.count()
        context["doctor_count"] = Doctor.objects.count()
        context["service_count"] = Service.objects.count()
        context["package_count"] = Package.objects.count()
        context["prescription_count"] = Prescription.objects.count()
        context["consumable_count"] = Consumable.objects.count()
        context["supplier_count"] = Supplier.objects.count()
        context["equipment_count"] = Equipment.objects.count()
        context["insurance_count"] = Insurance.objects.count()
        return context
