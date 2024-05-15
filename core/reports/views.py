from django.shortcuts import render
from django.views.generic import View
from accounts.filters import UserFilter
from accounts.models import User
from django.shortcuts import HttpResponse
import pandas as pd
from asset.filters import EquipmentFilter
from asset.models import Equipment
from base.views import BaseListView
from client.models import Client
from client.filters import ClientFilters
from doctor.models import Doctor
from doctor.filters import DoctorFilter
from financial.models import Financial, OfficeExpenses
from financial.filters import FinancialFilter, OfficeExpensesFilter
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
from consumable.models import ConsumableV2, Supplier
from consumable.filters import ConsumableFilter, SupplierFilter
from django.db.models.functions import Concat
from django.db.models import CharField, Value


# Create your views here.
class UserReportsView(BaseListView):
    model = User
    template_name = "reports/user.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"


class ExportUsersCSVView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        user_filter = UserFilter(request.GET, queryset=User.objects.all())
        filtered_users = user_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_users.values()))

        # Remove password column
        users_df.drop(columns=["password", 'image','created_by_id'], inplace=True)

        users_df.rename(
            columns={
                "last_login": "تاریخ آخرین لاگین",
                "is_superuser": "کاربر ادمین",
                "is_staff": "راهبر سیستم",
                "is_active": "وضعیت",
                "date_joined": "تاریخ عضویت",
                "email": "ایمیل",
                "first_name": "نام",
                "last_name": "نام خانوادگی",
                "date_of_birth": "تاریخ تولد",
                "national_id": "کدملی",
                "phone_number": "شماره تماس",
                "address": "آدرس",
                "login_attempts": "تعداد دفعات لاگین",
                "created_at": "تاریخ ایجاد",
                "updated_at": "تاریخ آخرین ویرایش",
            },
            inplace=True,
        )



        # Convert datetime columns to date
        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Add a new column 'created_by_email'
        users_df["ایجاد کننده"] = filtered_users.values_list(
            "created_by__email", flat=True
        )

        # Create a response object
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="user_report.csv"'

        # Write DataFrame to CSV file and return response
        users_df.to_csv(response, index=False)

        return response


class EquipmentReportsView(BaseListView):
    model = Equipment
    template_name = "reports/equipment.html"
    filterset_class = EquipmentFilter
    permission_required = "asset.view_equipment"


class ExportEquipmentExcelView(View):
    def get(self, request):
        # Get filtered equipment based on request parameters
        equipment_filter = EquipmentFilter(
            request.GET, queryset=Equipment.objects.all()
        )
        filtered_equipment = equipment_filter.qs

        # Convert filtered equipment queryset to DataFrame
        equipment_df = pd.DataFrame(list(filtered_equipment.values()))
        equipment_df.drop(columns=['created_by_id'], inplace=True)


        equipment_df.rename(
            columns={
                "name": "نام",
                "manufacturer": "سازنده",
                "model": "مدل",
                "serial_number": "شماره سریال",
                "acquisition_date": "تاریخ بهره برداری",
                "warranty_expiry_date": "تاریخ انقضا گارانتی",
                "location": "لوکیشن",
                "is_available": "در دسترس",
                "description": "توضیحات",
                "last_maintenance_date": "تاریخ آخرین تعمیر",
                "created_at": "تاریخ ایجاد",
                "updated_at": "تاریخ آخرین ویرایش",
            },
            inplace=True,
        )
        equipment_df["ایجاد کننده"] = filtered_equipment.values_list(
            "created_by__email", flat=True
        )
        # Convert datetime columns to date
        date_columns = equipment_df.select_dtypes(
            include=["datetime64[ns, Iran]"]
        ).columns
        for date_column in date_columns:
            equipment_df[date_column] = equipment_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="equipment_report.csv"'

        # Write DataFrame to CSV file and return response
        equipment_df.to_csv(response, index=False)

        return response


class ClientReportsView(BaseListView):
    model = Client
    template_name = "reports/client.html"
    filterset_class = ClientFilters
    permission_required = "client.view_client"


class ExportClientExcelView(View):
    def get(self, request):
        # Get filtered clients based on request parameters
        client_filter = ClientFilters(request.GET, queryset=Client.objects.all())
        filtered_clients = client_filter.qs

        # Convert filtered clients queryset to DataFrame
        clients_df = pd.DataFrame(list(filtered_clients.values()))
        clients_df.drop(
            columns=["image", "insurance_id", "created_by_id", "initial_session_id"],
            inplace=True,
        )

        clients_df.rename(
            columns={
                "case_id": "شماره پرونده",
                "first_name": "نام",
                "last_name": "نام خانوادگی",
                "national_id": "کد ملی",
                "fathers_name": "نام پدر",
                "date_of_birth": "تاریخ تولد",
                "gender": "جنسیت",
                "phone_number": "شماره تماس",
                "address": "آدرس",
                "marital_status": "وضعیت تاهل",
                "emergency_contact_name": "نام همراه ( شرایط اضطراری)",
                "emergency_contact_number": "شماره تماس همراه",
                "surgeries": "سابقه جراحی",
                "allergies": "حساسیت",
                "medical_history": "سوابق درمان",
                "medications": "سوابق دارویی",
                "smoker": "استعمال دخانیات",
                "disease": "بیماری",
                "created_at": "تاریخ ایجاد",
                "updated_at": "تاریخ آخرین ویرایش",
                "is_vip": "وضعیت",
                "number_of_receptions": "تعداد دفعات مراجعه",
                "last_reception_date": "تاریخ آخرین مراجعه",
                "last_reception_reason": "علت آخرین مراجعه",
            },
            inplace=True,
        )

        # Convert datetime columns to date
        date_columns = clients_df.select_dtypes(
            include=["datetime64[ns, Iran]"]
        ).columns
        for date_column in date_columns:
            clients_df[date_column] = clients_df[date_column].dt.date

        # Add created_by_email column
        clients_df["ایجاد کننده"] = filtered_clients.values_list(
            "created_by__email", flat=True
        )
        clients_df["بیمه"] = filtered_clients.values_list("insurance__name", flat=True)

        # Create a response object
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="client_report.csv"'

        # Write DataFrame to CSV file and return response
        clients_df.to_csv(response, index=False)

        return response


class DoctorReportsView(BaseListView):
    model = Doctor
    template_name = "reports/doctor.html"
    filterset_class = DoctorFilter
    permission_required = "doctor.view_doctor"


class ExportDoctorExcelView(View):
    def get(self, request):
        # Get filtered doctors based on request parameters
        doctor_filter = DoctorFilter(request.GET, queryset=Doctor.objects.all())
        filtered_doctors = doctor_filter.qs

        # Convert filtered doctors queryset to DataFrame
        doctors_df = pd.DataFrame(list(filtered_doctors.values()))

        doctors_df.drop(
            columns=["image", "created_by_id",],
            inplace=True,
        )


        doctors_df.rename(
            columns={
                "first_name": "نام",
                "last_name": "نام خانوادگی",
                "email": "ایمیل",
                "phone_number": "شماره تماس",
                "address": "آدرس",
                "specialization": "تخصص",
                "registration_number": "شماره نظام پزشکی",
                "is_active": "وضعیت",
                "created_at": "تاریخ ایجاد",
                "updated_at": "تاریخ آخرین ویرایش",
            },
            inplace=True,
        )


        doctors_df["ایجاد کننده"] = filtered_doctors.values_list(
            "created_by__email", flat=True
        )
        # Convert datetime columns to date
        date_columns = doctors_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            doctors_df[date_column] = doctors_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="doctor_report.csv"'

        # Write DataFrame to CSV file and return response
        doctors_df.to_csv(response, index=False)

        return response



class FinancialReportsView(BaseListView):
    model = Financial
    template_name = "reports/financial.html"
    filterset_class = FinancialFilter
    permission_required = "financial.view_financial"


class ExportFinancialExcelView(View):
    def get(self, request):
        # Get filtered financial records based on request parameters
        financial_filter = FinancialFilter(request.GET, queryset=Financial.objects.all())
        filtered_financial = financial_filter.qs

        # Convert filtered financial records queryset to DataFrame
        financial_df = pd.DataFrame(list(filtered_financial.values()))

        # Drop unnecessary columns
        financial_df.drop(
            columns=["attachment", "created_by_id", "doctor_id", "valid_insurance"],
            inplace=True,
        )

        # Rename columns
        financial_df.rename(
            columns={
                "invoice_number": "شماره صورتحساب",
                "reception_id": "شناسه پذیرش",
                "insurance_range": "درصد پوشش بیمه",
                "discount": "تخفیف",
                "insurance_amount": "مبلغ پوشش بیمه",
                "date_issued": "تاریخ ایجاد",
                "service_price": "مبلغ سرویس",
                "service_tax": "مالیات سرویس",
                "service_price_final": "مبلغ نهایی سرویس",
                "consumable_price": "هزینه مواد مصرفی",
                "consumable_tax": "مالیات مواد مصرفی",
                "consumable_price_final": "مبلغ نهایی مواد مصرفی",
                "total_amount": "مبلغ کل",
                "final_amount": "مبلغ نهایی",
                "payment_status": "وضعیت پرداخت",
                "payment_received_date": "تاریخ پرداخت",
                "doctors_wage": "سهم پزشک",
                "revenue": "درآمد",
                "created_at": "تاریخ ایجاد",
                "updated_at": "تاریخ آخرین ویرایش",
                "coupon_id": "کد تخفیف",
            },
            inplace=True,
        )

        # Add 'ایجاد کننده' column with creator's email
        financial_df["ایجاد کننده"] = filtered_financial.values_list(
            "created_by__email", flat=True
        )

        # Add 'سرویس ارایه شده' column with reception service
        financial_df["سرویس ارایه شده"] = filtered_financial.values_list(
            "reception__service__name", flat=True
        )

        filtered_financial = filtered_financial.annotate(
            full_name=Concat('reception__service__doctor__first_name', Value(' '), 'reception__service__doctor__last_name', output_field=CharField())
        )
        # Add 'پزشک' column with doctor's name
        financial_df["پزشک"] = filtered_financial.values_list(
            "full_name", flat=True
        )

        filtered_financial = filtered_financial.annotate(
            full_name=Concat('reception__client__first_name', Value(' '), 'reception__client__last_name', output_field=CharField())
        )
        # Add 'نام بیمار' column with client's name
        financial_df["نام بیمار"] = filtered_financial.values_list("full_name", flat=True)

        # Create a response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="invoice_report.csv"'

        # Write DataFrame to CSV file and return response
        financial_df.to_csv(response, index=False, encoding='utf-8-sig')  # Ensure correct encoding for Persian characters

        return response



class InsuranceReportsView(BaseListView):
    model = Insurance
    template_name = "reports/insurance.html"
    filterset_class = InsuranceFilter
    permission_required = "insurance.view_insurance"


class ExportInsuranceExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        insurance_filter = UserFilter(request.GET, queryset=Insurance.objects.all())
        filtered_insurance = insurance_filter.qs

        # Convert filtered users queryset to DataFrame
        insurance_df = pd.DataFrame(list(filtered_insurance.values()))

        # Convert filtered insurances queryset to DataFrame
        insurance_df = pd.DataFrame(list(filtered_insurance.values()))
        insurance_df.drop(
            columns=[ "created_by_id",],
            inplace=True,
        )

              # Rename columns
        insurance_df.rename(
            columns={
                "name": "عنوان",
                "policy_number": "شناسه ",
                "insurance_company": "سازمان ارائه دهنده",
                "deductible": "تخفیف",
                "copay": "پرداخت مشترک(copay)",
                "max_annual_coverage": "حداکثر پوشش سالانه",
                "policy_type": "نوع سیاست گذاری",
                "notes": "یادداشت",
                "updated_at": "تاریخ آخرین ویرایش",
                "created_at": "تاریخ ایجاد",
            },
            inplace=True,
        )  


        # Convert datetime columns to date
        date_columns = insurance_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            insurance_df[date_column] = insurance_df[date_column].dt.date


        # Add a new column 'created_by_email'
        insurance_df["ایجاد کننده"] = filtered_insurance.values_list(
            "created_by__email", flat=True
        )
        # Create a response object
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="insurance_report.csv"'

        # Write DataFrame to CSV file and return response
        insurance_df.to_csv(response, index=False)

        return response

class InsuranceServiceReportsView(BaseListView):
    model = InsuranceService
    template_name = "reports/insurance_service.html"
    filterset_class = InsuranceServiceFilter
    permission_required = "insurance.view_insuranceservice"


class ExportInsuranceServiceExcelView(View):
    def get(self, request):
        # Get filtered insurance services based on request parameters
        insurance_service_filter = InsuranceServiceFilter(
            request.GET, queryset=InsuranceService.objects.all()
        )
        filtered_insurance_service = insurance_service_filter.qs

        # Convert filtered insurance services queryset to DataFrame
        insurance_service_df = pd.DataFrame(list(filtered_insurance_service.values()))

        insurance_service_df.drop(
            columns=[ "created_by_id","service_id","insurance_id"],
            inplace=True,
        )

        insurance_service_df.rename(
            columns={
                "percentage": "درصد پوشش",
                "notes": "یادداشت ",
                "updated_at": "تاریخ آخرین ویرایش",
                "created_at": "تاریخ ایجاد",
            },
            inplace=True,
        )  

        # Convert datetime columns to date
        date_columns = insurance_service_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            insurance_service_df[date_column] = insurance_service_df[date_column].dt.date


        insurance_service_df["نام سرویس"] = filtered_insurance_service.values_list(
            "service__name", flat=True
        )
        insurance_service_df["نام بیمه"] = filtered_insurance_service.values_list(
            "insurance__name", flat=True
        )
        # Add a new column 'created_by_email'
        insurance_service_df["ایجاد کننده"] = filtered_insurance_service.values_list(
            "created_by__email", flat=True
        )


        # Create a response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="insurance_service_report.csv"'

        # Write DataFrame to CSV file and return response
        insurance_service_df.to_csv(response, index=False)

        return response



class PrescriptionReportsView(BaseListView):
    model = Prescription
    template_name = "reports/prescription.html"
    filterset_class = PrescriptionFilter
    permission_required = "prescription.view_prescription"


class ExportPrescriptionExcelView(View):
    def get(self, request):
        # Get filtered prescriptions based on request parameters
        prescription_filter = PrescriptionFilter(
            request.GET, queryset=Prescription.objects.all()
        )
        filtered_prescriptions = prescription_filter.qs

        # Convert filtered prescriptions queryset to DataFrame
        prescriptions_df = pd.DataFrame(list(filtered_prescriptions.values()))

        prescriptions_df.drop(
            columns=[ "created_by_id",],
            inplace=True,
        )

        prescriptions_df.rename(
            columns={
                "reception_id": "شناسه پذیرش",
                "date": "تاریخ ",
                "notes": "اطلاعات تکمیلی",
                "updated_at": "تاریخ آخرین ویرایش",
                "created_at": "تاریخ ایجاد",
            },
            inplace=True,
        )  

        # Convert datetime columns to date
        date_columns = prescriptions_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            prescriptions_df[date_column] = prescriptions_df[date_column].dt.date

        # Add a new column 'created_by_email'
        prescriptions_df["ایجاد کننده"] = filtered_prescriptions.values_list(
            "created_by__email", flat=True
        )

        # Create a response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="prescription_report.csv"'

        # Write DataFrame to CSV file and return response
        prescriptions_df.to_csv(response, index=False)

        return response



class ReceptionReportsView(BaseListView):
    model = Reception
    template_name = "reports/reception.html"
    filterset_class = ReceptionFilter
    permission_required = "reception.view_reception"


class ExportReceptionExcelView(View):
    def get(self, request):
        # Get filtered receptions based on request parameters
        reception_filter = ReceptionFilter(
            request.GET, queryset=Reception.objects.all()
        )
        filtered_receptions = reception_filter.qs

        # Convert filtered receptions queryset to DataFrame
        receptions_df = pd.DataFrame(list(filtered_receptions.values()))

        receptions_df.drop(
            columns=[ "created_by_id",'client_id','service_id','invoice_attachment',"reception_in_day"],
            inplace=True,
        )

        receptions_df.rename(
            columns={
                "status": "وضعیت",
                "reason": "علت مراجعه ",
                "payment_type": "نوع پرداخت",
                "payment_status": "وضعیت پرداخت",
                "date": "تاریخ ",
                "created_at": "تاریخ ایجاد",
                "updated_at": " تاریخ آخرین ویرایش",
                "session_id": "شناسه نوبت",
            },
            inplace=True,
        )  
        # Convert datetime columns to date
        date_columns = receptions_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            receptions_df[date_column] = receptions_df[date_column].dt.date

        receptions_df["ایجاد کننده"] = filtered_receptions.values_list(
            "created_by__email", flat=True
        )

                # Add 'سرویس ارایه شده' column with reception service
        receptions_df["سرویس ارایه شده"] = filtered_receptions.values_list(
            "service__name", flat=True
        )

        filtered_receptions = filtered_receptions.annotate(
            full_name=Concat('service__doctor__first_name', Value(' '), 'service__doctor__last_name', output_field=CharField())
        )
        # Add 'پزشک' column with doctor's name
        receptions_df["پزشک"] = filtered_receptions.values_list(
            "full_name", flat=True
        )

        filtered_receptions = filtered_receptions.annotate(
            full_name=Concat('client__first_name', Value(' '), 'client__last_name', output_field=CharField())
        )
        # Add 'نام بیمار' column with client's name
        receptions_df["نام بیمار"] = filtered_receptions.values_list("full_name", flat=True)


        # Create a response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reception_report.csv"'

        # Write DataFrame to CSV file and return response
        receptions_df.to_csv(response, index=False)

        return response


class ServiceReportsView(BaseListView):
    model = Service
    template_name = "reports/service.html"
    filterset_class = ServicesFilter
    permission_required = "services.view_service"


class ExportServiceExcelView(View):
    def get(self, request):
        # Get filtered services based on request parameters
        service_filter = ServicesFilter(request.GET, queryset=Service.objects.all())
        filtered_services = service_filter.qs

        # Convert filtered services queryset to DataFrame
        services_df = pd.DataFrame(list(filtered_services.values()))

        services_df.drop(
            columns=[ "created_by_id",'doctor_id','category_id','check_consumable_inventory',],
            inplace=True,
        )


        services_df.rename(
            columns={
                "name": "عنوان",
                "doctors_wage_percentage": " درصد سهم پزشک",
                "description": "توضیحات",
                "duration": "مدت زمان تقریبی",
                "price": "مبلغ سرویس ",
                "preparation_instructions": "دستورالعمل های آماده سازی",
                "is_active": "وضعیت فعال بودن",
                "therapeutic_measures": "اقدامات درمانی",
                "appointment_per_day": "ظرفیت نوبت دهی در روز",
                "created_at": "تاریخ ایجاد",
                "updated_at": " تاریخ آخرین ویرایش",
                "documentation_requirements": "ملزومات مستندسازی",
                "recommendations": "توصیه ها",
            },
            inplace=True,
        )  

        date_columns = services_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
                services_df[date_column] = services_df[date_column].dt.date



        services_df["ایجاد کننده"] = filtered_services.values_list(
            "created_by__email", flat=True
        )

        filtered_services = filtered_services.annotate(
            full_name=Concat('doctor__first_name', Value(' '), 'doctor__last_name', output_field=CharField())
        )
        # Add 'پزشک' column with doctor's name
        services_df["پزشک"] = filtered_services.values_list(
            "full_name", flat=True
        )
        services_df["دسته بندی"] = filtered_services.values_list(
            "category__name", flat=True
        )

        # Create a response object
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="service_report.csv"'

        # Write DataFrame to CSV file and return response
        services_df.to_csv(response, index=False)

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

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="supplier_report.xlsx"'

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response


class OfficeExpensesReportsView(BaseListView):
    model = Financial
    template_name = "reports/office_expenses.html"
    filterset_class = OfficeExpensesFilter
    permission_required = "financial.view_office_expenses"


class ExportOfficeExpensesExcelView(View):
    def get(self, request):
        # Get filtered users based on request parameters
        office_expenses_filter = OfficeExpensesFilter(
            request.GET, queryset=OfficeExpenses.objects.all()
        )
        filtered_office_expenses = office_expenses_filter.qs

        # Convert filtered users queryset to DataFrame
        users_df = pd.DataFrame(list(filtered_office_expenses.values()))

        date_columns = users_df.select_dtypes(include=["datetime64[ns, Iran]"]).columns
        for date_column in date_columns:
            users_df[date_column] = users_df[date_column].dt.date

        # Create a response object
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment; filename="office_expenses_report.xlsx"'
        )

        # Write DataFrame to Excel file and return response
        users_df.to_excel(response, index=False)

        return response
