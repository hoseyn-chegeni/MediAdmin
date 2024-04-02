from django.shortcuts import render
from django.views.generic import View
from accounts.filters import UserFilter
from accounts.models import User
from django.shortcuts import HttpResponse
import pandas as pd
from asset.filters import ConsumableFilter, SupplierFilter, EquipmentFilter
from asset.models import Consumable,Supplier, Equipment
from base.views import BaseListView
from booking.models import Appointment, PackageAppointment
from booking.filters import AppointmentFilter, PackageAppointmentFilter
from client.models import Client
from client.filters import ClientFilters
from doctor.models import Doctor
from doctor.filters import DoctorFilter
from financial.models import Financial
from financial.filters import FinancialFilter


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

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="user_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response



class ConsumableReportsView(BaseListView):
    model = Consumable
    template_name = "reports/consumable.html"
    context_object_name = "consumable"
    filterset_class = ConsumableFilter
    permission_required = "asset.view_consumable"
    

class ExportConsumableExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        consumable_filter = ConsumableFilter(request.GET, queryset=Consumable.objects.all())
        filtered_consumable = consumable_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_consumable.values()))

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="consumable_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class SupplierReportsView(BaseListView):
    model = Supplier
    template_name = "reports/supplier.html"
    context_object_name = "supplier"
    filterset_class = SupplierFilter
    permission_required = "asset.view_supplier"
    

class ExportSupplierExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        supplier_filter = SupplierFilter(request.GET, queryset=Supplier.objects.all())
        filtered_supplier = supplier_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_supplier.values()))

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="supplier_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response



class EquipmentReportsView(BaseListView):
    model = Supplier
    template_name = "reports/equipment.html"
    filterset_class = EquipmentFilter
    permission_required = "asset.view_equipment"
    

class ExportEquipmentExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        equipment_filter = EquipmentFilter(request.GET, queryset=Equipment.objects.all())
        filtered_equipment = equipment_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_equipment.values()))

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="equipment_report.xlsx"'

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
        appointment_filter = AppointmentFilter(request.GET, queryset=Appointment.objects.all())
        filtered_appointment = appointment_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_appointment.values()))

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="appointment_report.xlsx"'

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
        package_appointment_filter = PackageAppointmentFilter(request.GET, queryset=PackageAppointment.objects.all())
        filtered_package_appointment = package_appointment_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_package_appointment.values()))

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="package_appointment_report.xlsx"'

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

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="client_report.xlsx"'

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

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="doctor_report.xlsx"'

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
        financial_filter = FinancialFilter(request.GET, queryset=Financial.objects.all())
        filtered_financial = financial_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_financial.values()))

        date_columns = users_df.select_dtypes(include=['datetime64[ns, Iran]']).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="invoice_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response