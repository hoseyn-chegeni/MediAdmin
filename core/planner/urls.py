from django.urls import path
from .views import (
    CalendarView,
    SessionListView,
    SessionCreateView,
    ServiceCardView,
    SessionDeleteView,
    TotalSessionListView,
    TotalDeletedSessionListView,
    TodaySessionListView,
    appointments_chart,sessions_per_doctor_chart
)

app_name = "planner"

urlpatterns = [
    path("<int:pk>/", CalendarView.as_view(), name="calendar"),
    path("list/<int:service_pk>/<int:day_pk>/", SessionListView.as_view(), name="list"),
    path(
        "create/<int:service_pk>/<int:day_pk>/",
        SessionCreateView.as_view(),
        name="create",
    ),
    path("service/card/", ServiceCardView.as_view(), name="service_card"),
    path(
        "session/delete/<int:pk>/",
        SessionDeleteView.as_view(),
        name="session_delete",
    ),
    path("total/list/", TotalSessionListView.as_view(), name="total_list"),
    path(
        "total/deleted/",
        TotalDeletedSessionListView.as_view(),
        name="total_deleted_list",
    ),
    path("list/today/", TodaySessionListView.as_view(), name="today_list"),
    path('appointments-chart/', appointments_chart, name='appointments_chart'),
    path('sessions-per-doctor-chart/', sessions_per_doctor_chart, name='sessions_per_doctor_chart'),

]
