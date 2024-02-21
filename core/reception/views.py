from base.views import (
    BaseCreateView,
    BaseListView,
    BaseDetailView,
    BaseDeleteView,
    BaseUpdateView,
)
from .models import Reception
from .filters import ReceptionFilter
from django.views.generic import ListView


# Create your views here.
class ReceptionListView(BaseListView):
    model = Reception
    template_name = "reception/list.html"
    context_object_name = "reception"
    filterset_class = ReceptionFilter


class ReceptionCreateView(BaseCreateView):
    model = Reception
    fields = ["reason", "payment_type", "payment_status", "client", "service"]
    template_name = "reception/create.html"
    app_name = "reception"
    url_name = "detail"

    def form_valid(self, form):
        # Set the client for the reception
        form.instance.status = "WAITE"
        return super().form_valid(form)


class ReceptionDetailView(BaseDetailView):
    model = Reception
    template_name = "reception/detail.html"
    context_object_name = "reception"


class ReceptionCreateViewUsingProfile(BaseCreateView):
    model = Reception
    fields = ["reason", "payment_type", "payment_status", "service"]
    template_name = "reception/create_profile.html"
    app_name = "reception"
    url_name = "detail"

    def get_initial(self):
        initial = super().get_initial()
        # Set the initial client value to the client whose profile page the user is on
        initial["client"] = self.kwargs[
            "pk"
        ]  # Assuming client's pk is passed in the URL
        return initial

    def form_valid(self, form):
        # Set the client for the reception
        form.instance.status = "WAITE"
        form.instance.client_id = self.kwargs[
            "pk"
        ]  # Assuming client's pk is passed in the URL
        return super().form_valid(form)


class ReceptionUpdateView(BaseUpdateView):
    model = Reception
    fields = "__all__"
    template_name = "reception/update.html"
    app_name = "reception"
    url_name = "detail"


class ReceptionDeleteView(BaseDeleteView):
    model = Reception
    template_name = "reception/delete.html"
    app_name = "reception"
    url_name = "list"


class WaitingListView(ListView):
    model = Reception
    template_name = "reception/waiting_list.html"
    context_object_name = "reception"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(status="WAITE")
