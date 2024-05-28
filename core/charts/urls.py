from django.urls import path
from .views import (
    daily_appointments_chart,
    appointments_chart,
    sessions_per_doctor_chart,
    service_reception_counts,
    user_group_distribution_chart,
    appointment_service_chart,
    client_gender_distribution,
    client_vip_distribution,
    clients_by_insurance_chart,
    consumable_categories_distribution,
    invoices_by_service,
    invoices_by_payment_method,
    expenses_last_10_days,
    invoices_last_10_days,
    clients_last_10_days,
    receptions_by_service,
    receptions_last_10_days_chart,
    client_reception_chart,
    service_reception_chart,
    task_priority_chart,
    task_status_chart,
    suppliers_by_city_chart,
    inventory_value_by_supplier_chart,
    doctors_by_specialty_chart,
)

app_name = "charts"

urlpatterns = [
    path("appointments-chart/", appointments_chart, name="appointments_chart"),
    path(
        "sessions-per-doctor-chart/",
        sessions_per_doctor_chart,
        name="sessions_per_doctor_chart",
    ),
    path(
        "service_reception_counts/",
        service_reception_counts,
        name="service_reception_counts",
    ),
    path(
        "user_group_distribution_chart/",
        user_group_distribution_chart,
        name="user_group_distribution_chart",
    ),
    path(
        "appointment_service_chart/",
        appointment_service_chart,
        name="appointment_service_chart",
    ),
    path(
        "daily_appointments_chart/",
        daily_appointments_chart,
        name="daily_appointments_chart",
    ),
    path(
        "client_gender_distribution/",
        client_gender_distribution,
        name="client_gender_distribution",
    ),
    path(
        "client_vip_distribution/",
        client_vip_distribution,
        name="client_vip_distribution",
    ),
    path(
        "clients_by_insurance_chart/",
        clients_by_insurance_chart,
        name="clients_by_insurance_chart",
    ),
    path(
        "consumable_categories_distribution/",
        consumable_categories_distribution,
        name="consumable_categories_distribution",
    ),
    path("invoices_by_service/", invoices_by_service, name="invoices_by_service"),
    path(
        "invoices_by_payment_method/",
        invoices_by_payment_method,
        name="invoices_by_payment_method",
    ),
    path("expenses_last_10_days/", expenses_last_10_days, name="expenses_last_10_days"),
    path("invoices_last_10_days/", invoices_last_10_days, name="invoices_last_10_days"),
    path("clients_last_10_days/", clients_last_10_days, name="clients_last_10_days"),
    path("receptions_by_service/", receptions_by_service, name="receptions_by_service"),
    path(
        "receptions_last_10_days_chart/",
        receptions_last_10_days_chart,
        name="receptions_last_10_days_chart",
    ),
    path(
        "client_reception_chart/", client_reception_chart, name="client_reception_chart"
    ),
    path(
        "service_reception_chart/",
        service_reception_chart,
        name="service_reception_chart",
    ),
    path("task_priority_chart/", task_priority_chart, name="task_priority_chart"),
    path("task_status_chart/", task_status_chart, name="task_status_chart"),
    path("suppliers_by_city_chart/", suppliers_by_city_chart, name="suppliers_by_city_chart"),
    path("inventory_value_by_supplier_chart/", inventory_value_by_supplier_chart, name="inventory_value_by_supplier_chart"),
    path("doctors_by_specialty_chart/", doctors_by_specialty_chart, name="doctors_by_specialty_chart"),
]
