from django.urls import path
from .views import ExportUsersExcelView, ConsumableReportsView,ExportConsumableExcelView, UserReportsView

app_name = 'reports'

urlpatterns = [
        path('user_reports/', UserReportsView.as_view(), name='user_reports'),
        path('export-users-excel/', ExportUsersExcelView.as_view(), name='export_users_excel'),

        path('consumable_reports/', ConsumableReportsView.as_view(), name='consumable_reports'),
        path('export-consumable-excel/', ExportConsumableExcelView.as_view(), name='export_consumable_excel'),
]