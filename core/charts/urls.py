from django.urls import path
from .views import appointments_chart, sessions_per_doctor_chart, service_reception_counts

app_name = 'charts'

urlpatterns = [
    path('appointments-chart/', appointments_chart, name='appointments_chart'),
    path('sessions-per-doctor-chart/', sessions_per_doctor_chart, name='sessions_per_doctor_chart'),
    path('service_reception_counts/', service_reception_counts, name='service_reception_counts'),

]