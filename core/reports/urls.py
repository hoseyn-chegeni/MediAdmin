from django.urls import path
from .views import (
        ExportUsersExcelView,
        ConsumableReportsView,
        ExportConsumableExcelView,
        UserReportsView,
        SupplierReportsView,
        ExportSupplierExcelView,
        EquipmentReportsView, 
        ExportEquipmentExcelView
)

app_name = 'reports'

urlpatterns = [
        path('user_reports/', UserReportsView.as_view(), name='user_reports'),
        path('export-users-excel/', ExportUsersExcelView.as_view(), name='export_users_excel'),

        path('consumable_reports/', ConsumableReportsView.as_view(), name='consumable_reports'),
        path('export-consumable-excel/', ExportConsumableExcelView.as_view(), name='export_consumable_excel'),

        path('supplier_reports/', SupplierReportsView.as_view(), name='supplier_reports'),
        path('export-supplier-excel/', ExportSupplierExcelView.as_view(), name='export_supplier_excel'),

        path('equipment_reports/', EquipmentReportsView.as_view(), name='equipment_reports'),
        path('export-equipment-excel/', ExportEquipmentExcelView.as_view(), name='export_equipment_excel'),
]