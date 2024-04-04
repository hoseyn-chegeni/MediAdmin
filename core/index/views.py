from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
class IndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "index.html"
    permission_required = "index.view_index"


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