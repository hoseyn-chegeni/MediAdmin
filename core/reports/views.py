from django.shortcuts import render
from django.views.generic import View
from accounts.filters import UserFilter
from accounts.models import User
from django.shortcuts import HttpResponse
import pandas as pd

from asset.filters import ConsumableFilter
from asset.models import Consumable
from base.views import BaseListView

# Create your views here.
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
    template_name = "reports/consumable_reports.html"
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
