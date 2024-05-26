from django.urls import path
from .views import daily_appointments_chart,appointments_chart, sessions_per_doctor_chart, service_reception_counts, user_group_distribution_chart,appointment_service_chart

app_name = 'charts'

urlpatterns = [
    path('appointments-chart/', appointments_chart, name='appointments_chart'),
    path('sessions-per-doctor-chart/', sessions_per_doctor_chart, name='sessions_per_doctor_chart'),
    path('service_reception_counts/', service_reception_counts, name='service_reception_counts'),
    path('user_group_distribution_chart/', user_group_distribution_chart, name='user_group_distribution_chart'),
    path('appointment_service_chart/', appointment_service_chart, name='appointment_service_chart'),
    path('daily_appointments_chart/', daily_appointments_chart, name='daily_appointments_chart'),

]