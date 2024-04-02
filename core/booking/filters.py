from django_filters import FilterSet
from .models import Appointment, PackageAppointment


class AppointmentFilter(FilterSet):

    class Meta:
        model = Appointment
        fields = {
            "id": ["exact"],
            "service": ["exact"],
            "client": ["exact"],
        }


class PackageAppointmentFilter(FilterSet):

    class Meta:
        model = PackageAppointment
        fields = {
            "id": ["exact"],
            "package": ["exact"],
            "client": ["exact"],
        }
