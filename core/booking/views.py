from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from .models import  PackageAppointment
from .filters import  PackageAppointmentFilter


# Create your views here.
# PACKAGE APPOINTMENT VIEWS HERE.
class PackageAppointmentListView(BaseListView):
    model = PackageAppointment
    template_name = "booking/package/list.html"
    context_object_name = "appointments"
    filterset_class = PackageAppointmentFilter
    permission_required = "booking.view_packageappointment"


class PackageAppointmentCreateView(BaseCreateView):
    model = PackageAppointment
    fields = "__all__"
    template_name = "booking/package/create.html"
    app_name = "booking"
    url_name = "package_detail"
    permission_required = "booking.add_packageappointment"

    def form_valid(self, form):
        if form.instance.package.total_price < form.instance.prepayment:
            form.add_error(
                "prepayment",
                f"مبلغ پیش پرداخت از مبلغ کل سرویس ({form.instance.package.total_price} ) بیشتر است .",
            )
            return self.form_invalid(form)
        return super().form_valid(form)


class PackageAppointmentDetailViews(BaseDetailView):
    model = PackageAppointment
    template_name = "booking/package/detail.html"
    permission_required = "booking.view_packageappointment"


class PackageAppointmentUpdateView(BaseUpdateView):
    model = PackageAppointment
    fields = "__all__"
    template_name = "booking/package/update.html"
    app_name = "booking"
    url_name = "package_detail"
    permission_required = "booking.change_packageappointment"


class PackageAppointmentDeleteView(BaseDeleteView):
    model = PackageAppointment
    app_name = "booking"
    url_name = "package_list"
    permission_required = "booking.delete_packageappointment"
