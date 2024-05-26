from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from planner.models import Session
from services.models import Service
from django.db.models import Count
from django.http import JsonResponse
from reception.models import Reception
from django.contrib.auth.models import Group
# Create your views here.


def appointments_chart(request):
    end_date = now().date() + timedelta(days=7)
    start_date = now().date()
    services = Service.objects.all()
    chart_data = []

    for service in services:
        data = {
            'service': service.name,
            'appointments': []
        }
        for day in range(7):
            date = start_date + timedelta(days=day)
            count = Session.objects.filter(service=service, day__christ_date=date).count()
            data['appointments'].append(count)
        chart_data.append(data)
    
    return JsonResponse({'chart_data': chart_data, 'dates': [(start_date + timedelta(days=day)).strftime('%Y-%m-%d') for day in range(7)]})

def sessions_per_doctor_chart(request):
    # Query sessions per doctor with status "در انتظار"
    sessions_per_doctor = (
        Service.objects.filter(session__status="در انتظار")
        .values('doctor__first_name', 'doctor__last_name')
        .annotate(session_count=Count('session'))
    )
    
    # Prepare data for the chart
    labels = [entry['doctor__first_name'] + ' ' + entry['doctor__last_name'] for entry in sessions_per_doctor]
    data = [entry['session_count'] for entry in sessions_per_doctor]

    # Create a dictionary to hold the data
    chart_data = {
        'labels': labels,
        'data': data,
    }
    # Return the data as JSON response
    return JsonResponse(chart_data)


def service_reception_counts(request):
    # Get the count of receptions for each service
    reception_counts = Reception.objects.values('service__name').annotate(count=Count('id'))
    
    data = {
        'labels': [item['service__name'] for item in reception_counts],
        'data': [item['count'] for item in reception_counts]
    }

    return JsonResponse(data)



def user_group_distribution_chart(request):
    # Query user groups and count the number of users in each group
    groups = Group.objects.annotate(user_count=Count('user'))

    # Prepare data for the pie chart
    labels = [group.name for group in groups]
    data = [group.user_count for group in groups]

    # Create a dictionary to hold the data
    chart_data = {
        'labels': labels,
        'data': data,
    }

    # Return the data as JSON response
    return JsonResponse(chart_data)


def appointment_service_chart(request):
    # Query appointments per service
    appointments_per_service = (
        Service.objects.annotate(appointment_count=Count('session'))
        .values('name', 'appointment_count')
    )

    # Prepare data for the chart
    labels = [entry['name'] for entry in appointments_per_service]
    data = [entry['appointment_count'] for entry in appointments_per_service]

    # Create a dictionary to hold the data
    chart_data = {
        'labels': labels,
        'data': data,
    }

    # Return the data as JSON response
    return JsonResponse(chart_data)