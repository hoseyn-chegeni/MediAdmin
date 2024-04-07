from typing import Any
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Appointment
from datetime import date
from reception.models import Reception
from tasks.models import Task
from financial.models import Financial
from django.db.models import Sum

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        appointment_count = Appointment.objects.filter(date=today).count()
        complete_appointment_count = Appointment.objects.filter(date=today, status="پذیرش شده").count()

        if appointment_count != 0:
            complete_percentage = round((complete_appointment_count / appointment_count) * 100)
        else:
            complete_percentage = 0

        context['appointment_count'] = appointment_count
        context['complete_percentage'] = complete_percentage

        
        context['today_reception'] = Reception.objects.filter(created_at__date = today).count()

        total_task =  Task.objects.count()
        complete_task = Task.objects.filter(status = "انجام شده").count()

        if total_task != 0:
            task_complete_percentage = round((complete_task / total_task) * 100)
        else:
            task_complete_percentage = 0

        context['total_task'] = total_task
        context['task_complete_percentage'] = task_complete_percentage

        total_revenue = Financial.objects.aggregate(total_revenue=Sum('final_amount'))['total_revenue']
        today_revenue = Financial.objects.filter(date_issued=today).aggregate(today_revenue=Sum('final_amount'))['today_revenue']

        if total_revenue != 0:
            revenue_percentage = round((today_revenue / total_revenue) * 100)
        else:
            revenue_percentage = 0

        # Round today_revenue to two decimal places
        today_revenue = round(today_revenue, 3)

        context['today_revenue'] = today_revenue
        context['revenue_percentage'] = revenue_percentage
        return context


