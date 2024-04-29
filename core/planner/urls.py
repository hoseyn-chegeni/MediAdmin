from django.urls import path
from .views import CalendarView

app_name = 'planner'

urlpatterns = [
    path('/<int:pk>/', CalendarView.as_view(), name='calendar'),
]