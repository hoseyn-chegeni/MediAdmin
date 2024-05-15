from django.urls import path
from .views import (
    ExportUsersCSVView,
    UserReportsView,
    EquipmentReportsView,
    ExportEquipmentExcelView,
    ClientReportsView,
    ExportClientExcelView,
    DoctorReportsView,
    ExportDoctorExcelView,
    FinancialReportsView,
    ExportFinancialExcelView,
    InsuranceReportsView,
    ExportInsuranceExcelView,
    InsuranceServiceReportsView,
    ExportInsuranceServiceExcelView,
    PrescriptionReportsView,
    ExportPrescriptionExcelView,
    ReceptionReportsView,
    ExportReceptionExcelView,
    ServiceReportsView,
    ExportServiceExcelView,
    PackageReportsView,
    ExportPackageExcelView,
    ClientSMSLogReportsView,
    ExportClientSMSLogExcelView,
    TaskReportsView,
    ExportTaskExcelView,
    ConsumableReportsView,
    ExportConsumableExcelView,
    SupplierReportsView,
    ExportSupplierExcelView,
    OfficeExpensesReportsView,
    ExportOfficeExpensesExcelView,
)

app_name = "reports"

urlpatterns = [
    path("user_reports/", UserReportsView.as_view(), name="user_reports"),
    path(
        "export-users-excel/", ExportUsersCSVView.as_view(), name="export_users_excel"
    ),
    path(
        "equipment_reports/", EquipmentReportsView.as_view(), name="equipment_reports"
    ),
    path(
        "export-equipment-excel/",
        ExportEquipmentExcelView.as_view(),
        name="export_equipment_excel",
    ),
    path("client_reports/", ClientReportsView.as_view(), name="client_reports"),
    path(
        "export-client-excel/",
        ExportClientExcelView.as_view(),
        name="export_client_excel",
    ),
    path("doctor_reports/", DoctorReportsView.as_view(), name="doctor_reports"),
    path(
        "export-doctor-excel/",
        ExportDoctorExcelView.as_view(),
        name="export_doctor_excel",
    ),
    path(
        "financial_reports/", FinancialReportsView.as_view(), name="financial_reports"
    ),
    path(
        "export-financial-excel/",
        ExportFinancialExcelView.as_view(),
        name="export_financial_excel",
    ),
    path(
        "insurance_reports/", InsuranceReportsView.as_view(), name="insurance_reports"
    ),
    path(
        "export-insurance-excel/",
        ExportInsuranceExcelView.as_view(),
        name="export_insurance_excel",
    ),
    path(
        "insurance_service_reports/",
        InsuranceServiceReportsView.as_view(),
        name="insurance_service_reports",
    ),
    path(
        "export-insurance-service-excel/",
        ExportInsuranceServiceExcelView.as_view(),
        name="export_insurance_service_excel",
    ),
    path(
        "prescription_reports/",
        PrescriptionReportsView.as_view(),
        name="prescription_reports",
    ),
    path(
        "export-prescription-excel/",
        ExportPrescriptionExcelView.as_view(),
        name="export_prescription_excel",
    ),
    path(
        "reception_reports/", ReceptionReportsView.as_view(), name="reception_reports"
    ),
    path(
        "export-reception-excel/",
        ExportReceptionExcelView.as_view(),
        name="export_reception_excel",
    ),
    path("service_reports/", ServiceReportsView.as_view(), name="service_reports"),
    path(
        "export-service-excel/",
        ExportServiceExcelView.as_view(),
        name="export_service_excel",
    ),
    path("package_reports/", PackageReportsView.as_view(), name="package_reports"),
    path(
        "export-package-excel/",
        ExportPackageExcelView.as_view(),
        name="export_package_excel",
    ),
    path(
        "client_sms_log_reports/",
        ClientSMSLogReportsView.as_view(),
        name="client_sms_log_reports",
    ),
    path(
        "export-client_sms_log-excel/",
        ExportClientSMSLogExcelView.as_view(),
        name="export_client_sms_log_excel",
    ),
    path("tasks_reports/", TaskReportsView.as_view(), name="tasks_reports"),
    path(
        "export-tasks-excel/", ExportTaskExcelView.as_view(), name="export_tasks_excel"
    ),
    path(
        "consumable_reports/",
        ConsumableReportsView.as_view(),
        name="consumable_reports",
    ),
    path(
        "export-consumable-excel/",
        ExportConsumableExcelView.as_view(),
        name="export_consumable_excel",
    ),
    path("supplier_reports/", SupplierReportsView.as_view(), name="supplier_reports"),
    path(
        "export-supplier-excel/",
        ExportSupplierExcelView.as_view(),
        name="export_supplier_excel",
    ),
    path(
        "office_expenses_reports/",
        OfficeExpensesReportsView.as_view(),
        name="office_expenses_reports",
    ),
    path(
        "export-office_expenses_excel/",
        ExportOfficeExpensesExcelView.as_view(),
        name="export_office_expenses_excel",
    ),
]
