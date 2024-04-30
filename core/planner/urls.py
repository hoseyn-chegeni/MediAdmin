from django.urls import path
from .views import CalendarView, SessionListView,SessionCreateView, ServiceCardView, SessionDeleteView

app_name = 'planner'

urlpatterns = [
    path('<int:pk>/', CalendarView.as_view(), name='calendar'),
    path('list/<int:service_pk>/<int:day_pk>/', SessionListView.as_view(), name='list'),
    path('create/<int:service_pk>/<int:day_pk>/', SessionCreateView.as_view(), name='create'),
    path('service/card/',ServiceCardView.as_view(), name='service_card'),
    path("session/delete/<int:pk>/",SessionDeleteView.as_view(),name="session_delete",),
]