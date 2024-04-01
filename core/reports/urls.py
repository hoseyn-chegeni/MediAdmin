from django.urls import path
from .views import ExportUsersExcelView, ConsumableReportsView,ExportConsumableExcelView

app_name = 'reports'

urlpatterns = [
        path('export-users-excel/', ExportUsersExcelView.as_view(), name='export_users_excel'),

        path('consumable_reports/', ConsumableReportsView.as_view(), name='consumable_reports'),
        path('export-consumable-excel/', ExportConsumableExcelView.as_view(), name='export_consumable_excel'),
]