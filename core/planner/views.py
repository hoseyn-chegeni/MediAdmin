from base.views import BaseListView, BaseCreateView
from .models import Month, Session, Day
from services.models import Service
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

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

        context["service"] = Service.objects.get(id=self.kwargs["service_pk"])
        context["day"] = Day.objects.get(id=self.kwargs["day_pk"])
        return context


class SessionCreateView(BaseCreateView):
    model = Session
    fields = ["client", "first_name", "last_name", "national_id", "phone_number"]
    template_name = "planner/create.html"
    permission_required = "planner.add_session"

    def get_success_url(self):
        return reverse_lazy(
            "planner:calendar", kwargs={"pk": self.kwargs["service_pk"]}
        )

    def form_valid(self, form):
        form.instance.day = Day.objects.get(id=self.kwargs["day_pk"])
        form.instance.service = Service.objects.get(id=self.kwargs["service_pk"])
        return super().form_valid(form)


class ServiceCardView(BaseListView):
    model = Service
    template_name = "planner/service_card.html"
    context_object_name = "services"
    filterset_class = 0
    permission_required = "services.view_service"


class SessionDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Session
    permission_required = "planner.delete_session"  # Update with your permission
    success_message = "نوبت اعلام شده با موفقیت لغو شد."
    template_name = "planner/delete.html"

    def get_success_url(self):
        # Override to redirect to a specific URL after deletion
        return reverse_lazy(
            "planner:list",
            kwargs={"day_pk": self.object.day.pk, "service_pk": self.object.service.pk},
        )
