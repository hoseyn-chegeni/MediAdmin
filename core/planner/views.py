from base.views import BaseListView, BaseCreateView
from .models import Month, Session, Day, DeletedSession

from services.models import Service
from django.urls import reverse_lazy
from .filters import SessionFilters
# Create your views here.


class CalendarView(BaseListView):
    model = Month
    template_name = "planner/calendar.html"
    context_object_name = "months"
    permission_required = "planner.view_day"
    filterset_class = 0

    def get_queryset(self):
        return Month.objects.all().prefetch_related("day_set")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.kwargs["pk"]
        context["service"] = Service.objects.get(id=service_id)

        # Annotate each day with the count of sessions for the specific service
        for month in context["months"]:
            for day in month.day_set.all():
                day.session_count = Session.objects.filter(
                    day=day, service_id=service_id
                ).count()

        return context


class SessionListView(BaseListView):
    model = Session
    template_name = "planner/list.html"
    context_object_name = "session"
    permission_required = "planner.view_session"
    filterset_class = 0

    def get_queryset(self):
        return Session.objects.filter(
            day_id=self.kwargs["day_pk"], service_id=self.kwargs["service_pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day = Day.objects.get(id=self.kwargs["day_pk"])
        service =  Service.objects.get(id=self.kwargs["service_pk"])
        context["service"] = Service
        context["day"] = day
        context['deleted'] = DeletedSession.objects.filter(day_id = day.id, service_id = service.id)
        return context


class SessionCreateView(BaseCreateView):
    model = Session
    fields = ["client", "first_name", "last_name", "national_id", "phone_number","status"]
    template_name = "planner/create.html"
    permission_required = "planner.add_session"

    def get_success_url(self):
        return reverse_lazy(
            "planner:calendar", kwargs={"pk": self.kwargs["service_pk"]}
        )

    def form_valid(self, form):
        form.instance.day = Day.objects.get(id=self.kwargs["day_pk"])
        form.instance.service = Service.objects.get(id=self.kwargs["service_pk"])
        form.instance.status = "در انتظار"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day = Day.objects.get(id=self.kwargs["day_pk"])
        service =  Service.objects.get(id=self.kwargs["service_pk"])
        context["service"] = service
        context["day"] = day
        return context


class ServiceCardView(BaseListView):
    model = Service
    template_name = "planner/service_card.html"
    context_object_name = "services"
    filterset_class = 0
    permission_required = "services.view_service"


class SessionDeleteView(BaseCreateView):
    model = DeletedSession
    permission_required = "planner.delete_session"  # Update with your permission
    template_name = "planner/delete.html"
    fields = ['reason',]
     # Update with your success URL name
    def form_valid(self, form):
        # Save the form data to create a new Session instance
        session_instance = Session.objects.get(id = self.kwargs['pk'])

        # Create a new instance in DeletedSession model

        form.instance.day_id=session_instance.day.id
        form.instance.service_id=session_instance.service.id
        if session_instance.client:
            form.instance.client_id=session_instance.client.id
        form.instance.first_name=session_instance.first_name
        form.instance.last_name=session_instance.last_name
        form.instance.national_id=session_instance.national_id
        form.instance.phone_number=session_instance.phone_number

        session_instance.delete()

        return super().form_valid(form)
    

    def get_success_message(self, cleaned_data):
        return "با موفقیت حذف شد"

    def get_success_url(self):
        return reverse_lazy(
            "planner:list",
            kwargs={"day_pk": self.object.day.id, "service_pk": self.object.service.id},
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = Session.objects.get(id=self.kwargs["pk"])
        context['session'] = session
        return context
    

class TotalSessionListView(BaseListView):
    model = Session
    template_name = "planner/total_list.html"
    context_object_name = "session"
    filterset_class = SessionFilters
    permission_required = "planner.view_session"


class TotalDeletedSessionListView(BaseListView):
    model = DeletedSession
    template_name = "planner/total_list.html"
    context_object_name = "session"
    filterset_class = SessionFilters
    permission_required = "planner.view_session"
