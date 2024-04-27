from typing import Any
from django.views.generic.base import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Appointment
from datetime import date
from reception.models import Reception
from tasks.models import Task
from financial.models import Financial
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import redirect
from client.models import Client


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        appointment_count = Appointment.objects.filter(date=today).count()
        complete_appointment_count = Appointment.objects.filter(
            date=today, status="پذیرش شده"
        ).count()

        if appointment_count != 0:
            complete_percentage = round(
                (complete_appointment_count / appointment_count) * 100
            )
        else:
            complete_percentage = 0

        context["appointment_count"] = appointment_count
        context["complete_percentage"] = complete_percentage

        today_reception = Reception.objects.filter(created_at__date=today).count()
        total_reception = Reception.objects.count()

        if total_reception != 0:
            reception_percentage = round((today_reception / total_reception) * 100)
        else:
            reception_percentage = 0

        context["today_reception"] = today_reception
        context["reception_percentage"] = reception_percentage

        total_task = Task.objects.count()
        complete_task = Task.objects.filter(status="انجام شده").count()

        if total_task != 0:
            task_complete_percentage = round((complete_task / total_task) * 100)
        else:
            task_complete_percentage = 0

        context["total_task"] = total_task
        context["task_complete_percentage"] = task_complete_percentage

        total_revenue = Financial.objects.aggregate(total_revenue=Sum("final_amount"))[
            "total_revenue"
        ]
        today_revenue = Financial.objects.filter(date_issued=today).aggregate(
            today_revenue=Sum("final_amount")
        )["today_revenue"]

        if total_revenue != 0 and today_revenue != None:
            revenue_percentage = round((today_revenue / total_revenue) * 100)
        else:
            revenue_percentage = 0

        # Round today_revenue to two decimal places
        if today_revenue != None:
            today_revenue = round(today_revenue, 3)

        context["today_revenue"] = today_revenue
        context["revenue_percentage"] = revenue_percentage
        return context


class ClientNationalIdSearchView(View):
    def get(self, request):
        query = request.GET.get("query")
        if query:
            # Search for the client
            client = Client.objects.filter(national_id=query).first()
            if client:
                # Redirect to the client detail page
                return redirect("client:detail", pk=client.pk)
            else:
                # Client does not exist, redirect to index page with a message
                messages.error(request, "بیمار با کدملی وارد شده در سیستم موجود نیست")
                return redirect(
                    "index:index"
                )  # Update 'index:index' with your actual URL name
        else:
            # If no query provided, redirect to the index page
            return redirect("index:index")


class ClientCaseIdSearchView(View):
    def get(self, request):
        query = request.GET.get("query")
        if query:
            # Search for the client
            client = Client.objects.filter(id=query).first()
            if client:
                # Redirect to the client detail page
                return redirect("client:detail", pk=client.pk)
            else:
                # Client does not exist, redirect to index page with a message
                messages.error(
                    request, "بیمار با شماره پرونده وارد شده در سیستم موجود نیست"
                )
                return redirect(
                    "index:index"
                )  # Update 'index:index' with your actual URL name
        else:
            # If no query provided, redirect to the index page
            return redirect("index:index")
