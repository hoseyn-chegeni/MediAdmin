from django.urls import path
from .views import CalendarView, SessionListView

app_name = 'planner'

urlpatterns = [
    path('<int:pk>/', CalendarView.as_view(), name='calendar'),
    path('session/<int:service_pk>/<int:day_pk>/', SessionListView.as_view(), name='session_list'),

]