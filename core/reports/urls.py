from django.urls import path
from .views import ExportUsersExcelView

app_name = 'reports'

urlpatterns = [
        path('export-users-excel/', ExportUsersExcelView.as_view(), name='export_users_excel'),
]