from django.shortcuts import render
from django.views.generic import View
from accounts.filters import UserFilter
from accounts.models import User
from django.shortcuts import HttpResponse
import pandas as pd
from asset.filters import  EquipmentFilter
from asset.models import  Equipment
from base.views import BaseListView
from booking.models import Appointment, PackageAppointment
from booking.filters import AppointmentFilter, PackageAppointmentFilter
from client.models import Client
from client.filters import ClientFilters
from doctor.models import Doctor
from doctor.filters import DoctorFilter
from financial.models import Financial
from financial.filters import FinancialFilter
from insurance.models import Insurance, InsuranceService
from insurance.filters import InsuranceFilter, InsuranceServiceFilter
from prescription.models import Prescription
from prescription.filters import PrescriptionFilter
from reception.models import Reception
from reception.filters import ReceptionFilter
from services.models import Service, Package
from services.filters import ServicesFilter, PackageFilter
from logs.models import ClientSMSLog
from notification.filters import ClientSMSLogFilter
from tasks.models import Task
from tasks.filters import TaskFilter
from consumable.models import ConsumableV2
from consumable.filters import ConsumableFilter

# Create your views here.
class UserReportsView(BaseListView):
    model = User
    template_name = "reports/user.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"


class ExportUsersExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        user_filter = UserFilter(request.GET, queryset=User.objects.all())
        filtered_users = user_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_users.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="user_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response





class EquipmentReportsView(BaseListView):
    model = Equipment
    template_name = "reports/equipment.html"
    filterset_class = EquipmentFilter
    permission_required = "asset.view_equipment"


class ExportEquipmentExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        equipment_filter = EquipmentFilter(
            request.GET, queryset=Equipment.objects.all()
        )
        filtered_equipment = equipment_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_equipment.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="equipment_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class AppointmentReportsView(BaseListView):
    model = Appointment
    template_name = "reports/appointment.html"
    filterset_class = AppointmentFilter
    permission_required = "booking.view_appointment"


class ExportAppointmentExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        appointment_filter = AppointmentFilter(
            request.GET, queryset=Appointment.objects.all()
        )
        filtered_appointment = appointment_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_appointment.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment; filename="appointment_report.xlsx"'
        )

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class PackageAppointmentReportsView(BaseListView):
    model = PackageAppointment
    template_name = "reports/package_appointment.html"
    filterset_class = PackageAppointmentFilter
    permission_required = "booking.view_packageappointment"


class ExportPackageAppointmentExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        package_appointment_filter = PackageAppointmentFilter(
            request.GET, queryset=PackageAppointment.objects.all()
        )
        filtered_package_appointment = package_appointment_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_package_appointment.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment; filename="package_appointment_report.xlsx"'
        )

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class ClientReportsView(BaseListView):
    model = Client
    template_name = "reports/client.html"
    filterset_class = ClientFilters
    permission_required = "client.view_client"


class ExportClientExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        client_filter = ClientFilters(request.GET, queryset=Client.objects.all())
        filtered_client = client_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_client.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="client_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class DoctorReportsView(BaseListView):
    model = Doctor
    template_name = "reports/doctor.html"
    filterset_class = DoctorFilter
    permission_required = "doctor.view_doctor"


class ExportDoctorExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        doctor_filter = DoctorFilter(request.GET, queryset=Doctor.objects.all())
        filtered_doctor = doctor_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_doctor.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="doctor_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class FinancialReportsView(BaseListView):
    model = Financial
    template_name = "reports/financial.html"
    filterset_class = FinancialFilter
    permission_required = "financial.view_financial"


class ExportFinancialExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        financial_filter = FinancialFilter(
            request.GET, queryset=Financial.objects.all()
        )
        filtered_financial = financial_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_financial.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="invoice_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class InsuranceReportsView(BaseListView):
    model = Insurance
    template_name = "reports/insurance.html"
    filterset_class = InsuranceFilter
    permission_required = "insurance.view_insurance"


class ExportInsuranceExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        insurance_filter = InsuranceFilter(
            request.GET, queryset=Insurance.objects.all()
        )
        filtered_insurance = insurance_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_insurance.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="insurance_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class InsuranceServiceReportsView(BaseListView):
    model = InsuranceService
    template_name = "reports/insurance_service.html"
    filterset_class = InsuranceServiceFilter
    permission_required = "insurance.view_insuranceservice"


class ExportInsuranceServiceExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        insurance_service_filter = InsuranceServiceFilter(
            request.GET, queryset=InsuranceService.objects.all()
        )
        filtered_insurance_service = insurance_service_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_insurance_service.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment; filename="insurance_service_report.xlsx"'
        )

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class PrescriptionReportsView(BaseListView):
    model = Prescription
    template_name = "reports/prescription.html"
    filterset_class = PrescriptionFilter
    permission_required = "prescription.view_prescription"


class ExportPrescriptionExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        prescription_filter = PrescriptionFilter(
            request.GET, queryset=Prescription.objects.all()
        )
        filtered_prescription = prescription_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_prescription.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment; filename="prescription_report.xlsx"'
        )

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class ReceptionReportsView(BaseListView):
    model = Reception
    template_name = "reports/reception.html"
    filterset_class = ReceptionFilter
    permission_required = "reception.view_reception"


class ExportReceptionExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        reception_filter = ReceptionFilter(
            request.GET, queryset=Reception.objects.all()
        )
        filtered_reception = reception_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_reception.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="reception_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class ServiceReportsView(BaseListView):
    model = Service
    template_name = "reports/service.html"
    filterset_class = ServicesFilter
    permission_required = "services.view_service"


class ExportServiceExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        service_filter = ServicesFilter(request.GET, queryset=Service.objects.all())
        filtered_service = service_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_service.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="service_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class PackageReportsView(BaseListView):
    model = Package
    template_name = "reports/package.html"
    filterset_class = PackageFilter
    permission_required = "services.view_package"


class ExportPackageExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        package_filter = PackageFilter(request.GET, queryset=Package.objects.all())
        filtered_package = package_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_package.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="package_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class ClientSMSLogReportsView(BaseListView):
    model = ClientSMSLog
    template_name = "reports/client_sms_log.html"
    filterset_class = ClientSMSLogFilter
    permission_required = "logs.view_clientsmslog"


class ExportClientSMSLogExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        client_sms_filter = ClientSMSLogFilter(
            request.GET, queryset=ClientSMSLog.objects.all()
        )
        filtered_client_sms = client_sms_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_client_sms.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="sms_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class TaskReportsView(BaseListView):
    model = Task
    template_name = "reports/tasks.html"
    filterset_class = TaskFilter
    permission_required = "tasks.view_task"


class ExportTaskExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        task_filter = TaskFilter(request.GET, queryset=Task.objects.all())
        filtered_task = task_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_task.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="tasks_reports.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response



class ConsumableReportsView(BaseListView):
    model = ConsumableV2
    template_name = "reports/consumable.html"
    context_object_name = "consumable"
    filterset_class = ConsumableFilter
    permission_required = "consumable.view_consumableV2"


class ExportConsumableExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        consumable_filter = ConsumableFilter(
            request.GET, queryset=ConsumableV2.objects.all()
        )
        filtered_consumable = consumable_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_consumable.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment; filename="consumable_report.xlsx"'
        )

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response