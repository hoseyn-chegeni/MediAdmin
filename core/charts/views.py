from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from planner.models import Session
from services.models import Service
from django.db.models import Count, Sum, F
from django.http import JsonResponse
from reception.models import Reception
from django.contrib.auth.models import Group
from client.models import Client
from consumable.models import ConsumableCategory
from financial.models import Financial, OfficeExpenses
from tasks.models import Task
from consumable.models import Supplier, Inventory
from doctor.models import Doctor
# Create your views here.


def appointments_chart(request):
    end_date = now().date() + timedelta(days=7)
    start_date = now().date()
    services = Service.objects.all()
    chart_data = []

    for service in services:
        data = {"service": service.name, "appointments": []}
        for day in range(7):
            date = start_date + timedelta(days=day)
            count = Session.objects.filter(
                service=service, day__christ_date=date
            ).count()
            data["appointments"].append(count)
        chart_data.append(data)

    return JsonResponse(
        {
            "chart_data": chart_data,
            "dates": [
                (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
                for day in range(7)
            ],
        }
    )


def sessions_per_doctor_chart(request):
    # Query sessions per doctor with status "در انتظار"
    sessions_per_doctor = (
        Service.objects.filter(session__status="در انتظار")
        .values("doctor__first_name", "doctor__last_name")
        .annotate(session_count=Count("session"))
    )

    # Prepare data for the chart
    labels = [
        entry["doctor__first_name"] + " " + entry["doctor__last_name"]
        for entry in sessions_per_doctor
    ]
    data = [entry["session_count"] for entry in sessions_per_doctor]

    # Create a dictionary to hold the data
    chart_data = {
        "labels": labels,
        "data": data,
    }
    # Return the data as JSON response
    return JsonResponse(chart_data)


def service_reception_counts(request):
    # Get the count of receptions for each service
    reception_counts = Reception.objects.values("service__name").annotate(
        count=Count("id")
    )

    data = {
        "labels": [item["service__name"] for item in reception_counts],
        "data": [item["count"] for item in reception_counts],
    }

    return JsonResponse(data)


def user_group_distribution_chart(request):
    # Query user groups and count the number of users in each group
    groups = Group.objects.annotate(user_count=Count("user"))

    # Prepare data for the pie chart
    labels = [group.name for group in groups]
    data = [group.user_count for group in groups]

    # Create a dictionary to hold the data
    chart_data = {
        "labels": labels,
        "data": data,
    }

    # Return the data as JSON response
    return JsonResponse(chart_data)


def appointment_service_chart(request):
    # Query appointments per service
    appointments_per_service = Service.objects.annotate(
        appointment_count=Count("session")
    ).values("name", "appointment_count")

    # Prepare data for the chart
    labels = [entry["name"] for entry in appointments_per_service]
    data = [entry["appointment_count"] for entry in appointments_per_service]

    # Create a dictionary to hold the data
    chart_data = {
        "labels": labels,
        "data": data,
    }

    # Return the data as JSON response
    return JsonResponse(chart_data)


def daily_appointments_chart(request):
    # Calculate date range for the next 10 days
    start_date = now().date()
    end_date = start_date + timedelta(days=9)  # Next 10 days
    date_range = [start_date + timedelta(days=i) for i in range(10)]

    # Query appointments per day
    appointments_per_day = []
    for date in date_range:
        count = Session.objects.filter(day__christ_date=date).count()
        appointments_per_day.append(count)

    # Prepare data for the chart
    labels = [date.strftime("%Y-%m-%d") for date in date_range]
    data = appointments_per_day

    # Create a dictionary to hold the data
    chart_data = {
        "labels": labels,
        "data": data,
    }

    # Return the data as JSON response
    return JsonResponse(chart_data)


def client_gender_distribution(request):
    male_count = Client.objects.filter(gender="M").count()
    female_count = Client.objects.filter(gender="F").count()

    data = {"male": male_count, "female": female_count}
    return JsonResponse(data)


def client_vip_distribution(request):
    vip_count = Client.objects.filter(is_vip=True).count()
    non_vip_count = Client.objects.filter(is_vip=False).count()

    data = {"VIP": vip_count, "Non-VIP": non_vip_count}
    return JsonResponse(data)


def clients_by_insurance_chart(request):
    insurance_providers = {}
    for client in Client.objects.all():
        if client.insurance:
            insurance_provider = client.insurance.name
            if insurance_provider in insurance_providers:
                insurance_providers[insurance_provider] += 1
            else:
                insurance_providers[insurance_provider] = 1

    return JsonResponse(insurance_providers)


def consumable_categories_distribution(request):
    categories = ConsumableCategory.objects.all()
    data = {"labels": [], "counts": []}

    for category in categories:
        data["labels"].append(category.name)
        data["counts"].append(category.consumable_count)

    return JsonResponse(data)


def invoices_by_service(request):
    services = Service.objects.all()
    data = {"labels": [], "counts": []}

    for service in services:
        data["labels"].append(service.name)
        count = Financial.objects.filter(reception__service=service).count()
        data["counts"].append(count)

    return JsonResponse(data)


def invoices_by_payment_method(request):
    payment_methods = dict(Reception.PAYMENT_TYPE_CHOICES)
    data = {"labels": list(payment_methods.values()), "counts": []}

    for method in payment_methods.keys():
        count = Financial.objects.filter(reception__payment_type=method).count()
        data["counts"].append(count)

    return JsonResponse(data)


def expenses_last_10_days(request):
    end_date = now().date()
    start_date = end_date - timedelta(days=9)

    date_expenses = {}
    for i in range(10):
        date = start_date + timedelta(days=i)
        date_expenses[date] = OfficeExpenses.objects.filter(
            date=date.strftime("%Y-%m-%d")
        ).count()

    labels = [date.strftime("%Y-%m-%d") for date in date_expenses.keys()]
    data = [count for count in date_expenses.values()]

    return JsonResponse({"labels": labels, "data": data})


def invoices_last_10_days(request):
    end_date = now().date()
    start_date = end_date - timedelta(days=9)

    date_invoices = {}
    for i in range(10):
        date = start_date + timedelta(days=i)
        date_invoices[date] = Financial.objects.filter(date_issued=date).count()

    labels = [date.strftime("%Y-%m-%d") for date in date_invoices.keys()]
    data = [count for count in date_invoices.values()]

    return JsonResponse({"labels": labels, "data": data})


def clients_last_10_days(request):
    end_date = now().date()
    start_date = end_date - timedelta(days=9)

    date_clients = {}
    for i in range(10):
        date = start_date + timedelta(days=i)
        date_clients[date] = Client.objects.filter(created_at__date=date).count()

    labels = [date.strftime("%Y-%m-%d") for date in date_clients.keys()]
    data = [count for count in date_clients.values()]

    return JsonResponse({"labels": labels, "data": data})


def receptions_by_service(request):
    services = Service.objects.all()
    data = []
    labels = []

    for service in services:
        count = Reception.objects.filter(service=service).count()
        if count > 0:
            data.append(count)
            labels.append(service.name)

    return JsonResponse({"labels": labels, "data": data})


def receptions_last_10_days_chart(request):
    end_date = now().date()
    start_date = end_date - timedelta(days=9)  # Last 10 days
    dates = [start_date + timedelta(days=i) for i in range(10)]

    receptions_data = []

    for date in dates:
        count = Reception.objects.filter(date=date).count()
        receptions_data.append({"date": date.strftime("%Y-%m-%d"), "count": count})

    return JsonResponse({"receptions_data": receptions_data})


def client_reception_chart(request):
    # Count the number of receptions per client
    client_reception_counts = Reception.objects.values("client").annotate(
        total_receptions=Count("id")
    )

    # Count the number of clients with 1 or less reception and 2 or more receptions
    clients_with_one_or_less_reception = sum(
        1 for item in client_reception_counts if item["total_receptions"] <= 1
    )
    clients_with_two_or_more_receptions = sum(
        1 for item in client_reception_counts if item["total_receptions"] >= 2
    )

    return JsonResponse(
        {
            "labels": ["1 or Less Reception", "2 or More Receptions"],
            "data": [
                clients_with_one_or_less_reception,
                clients_with_two_or_more_receptions,
            ],
        }
    )


def service_reception_chart(request):
    # Count the number of receptions per service
    service_reception_counts = (
        Reception.objects.values("service__name")
        .annotate(total_receptions=Count("id"))
        .order_by("-total_receptions")[:5]
    )

    labels = [item["service__name"] for item in service_reception_counts]
    counts = [item["total_receptions"] for item in service_reception_counts]

    return JsonResponse({"labels": labels, "data": counts})


def task_priority_chart(request):
    # Count the number of tasks for each priority
    priority_counts = Task.objects.values("priority").annotate(count=Count("id"))

    labels = [item["priority"] for item in priority_counts]
    counts = [item["count"] for item in priority_counts]

    return JsonResponse({"labels": labels, "data": counts})


def task_status_chart(request):
    # Count the number of tasks for each status
    status_counts = Task.objects.values("status").annotate(count=Count("id"))

    labels = [item["status"] for item in status_counts]
    counts = [item["count"] for item in status_counts]

    return JsonResponse({"labels": labels, "data": counts})


def suppliers_by_city_chart(request):
    # Query to get the count of suppliers in each city
    city_counts = Supplier.objects.values('city').annotate(count=Count('id'))

    # Extract city names and counts
    cities = [item['city'] for item in city_counts]
    counts = [item['count'] for item in city_counts]

    return JsonResponse({'cities': cities, 'counts': counts})


def inventory_value_by_supplier_chart(request):
    # Aggregate total value of inventory for each supplier
    suppliers = Supplier.objects.annotate(
        total_value=Sum(F('inventory__quantity') * F('inventory__price'))
    ).order_by('-total_value')[:5]

    chart_data = []
    for supplier in suppliers:
        total_value = supplier.total_value or 0
        chart_data.append({
            'supplier': supplier.name,
            'total_value': total_value
        })

    return JsonResponse(chart_data, safe=False)


def doctors_by_specialty_chart(request):
    specialties = Doctor.objects.values('specialization').annotate(count=Count('id'))
    chart_data = []
    for specialty in specialties:
        chart_data.append({
            'specialization': specialty['specialization'],
            'count': specialty['count']
        })
    return JsonResponse({'chart_data': chart_data})
