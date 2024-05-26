from django.urls import path
from .views import appointments_chart, sessions_per_doctor_chart, service_reception_counts, user_group_distribution_chart

app_name = 'charts'

urlpatterns = [
    path('appointments-chart/', appointments_chart, name='appointments_chart'),
    path('sessions-per-doctor-chart/', sessions_per_doctor_chart, name='sessions_per_doctor_chart'),
    path('service_reception_counts/', service_reception_counts, name='service_reception_counts'),
    path('user_group_distribution_chart/', user_group_distribution_chart, name='user_group_distribution_chart'),
]