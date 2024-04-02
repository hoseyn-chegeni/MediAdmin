from .models import User
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from .filters import UserFilter, UserSentSMSFilter, UserSMSFilter
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseUpdateView,
)
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from logs.models import UserSMSLog, ClientSMSLog
from client.models import Client
from reception.models import Reception
from booking.models import Appointment
from asset.models import Consumable, Supplier
from financial.models import OfficeExpenses
from doctor.models import Doctor
from insurance.models import Insurance
from prescription.models import Prescription
from services.models import Service
from itertools import chain
from operator import attrgetter
from django.http import HttpResponse
import pandas as pd


# Create your views here.
class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active=True)


class SuspendUserListView(BaseListView):
    model = User
    template_name = "accounts/suspend_list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_active=False)


class UserDetailView(BaseDetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"
    permission_required = "accounts.view_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        receive_sms = UserSMSLog.objects.filter(user_id=user.id)
        sent_sms = ClientSMSLog.objects.filter(created_by_id=user.id)
        context["user_permissions"] = user.user_permissions.all()
        context["receive_sms"] = receive_sms.order_by("-created_at")[:5]
        context["receive_sms_count"] = receive_sms.count()
        context["sent_sms"] = sent_sms.order_by("-created_at")[:5]
        context["sent_sms_count"] = sent_sms.count()
        context["clients"] = Client.objects.filter(created_by_id=user.id).count()
        context["receptions"] = Reception.objects.filter(created_by_id=user.id).count()
        context["appointments"] = Appointment.objects.filter(
            created_by_id=user.id
        ).count()
        context["user_count"] = User.objects.filter(created_by_id=user.id).count()
        context["consumable"] = Consumable.objects.filter(created_by_id=user.id).count()
        context["supplier"] = Supplier.objects.filter(created_by_id=user.id).count()
        context["office_expenses"] = OfficeExpenses.objects.filter(
            created_by_id=user.id
        ).count()
        context["doctor"] = Doctor.objects.filter(created_by_id=user.id).count()
        context["insurance"] = Insurance.objects.filter(created_by_id=user.id).count()
        context["prescription"] = Prescription.objects.filter(
            created_by_id=user.id
        ).count()
        context["service"] = Service.objects.filter(created_by_id=user.id).count()
        return context


class UserCreateView(BaseCreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/create.html"
    app_name = "accounts"
    url_name = "user_detail"
    permission_required = "accounts.add_user"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UserUpdateView(BaseUpdateView):
    model = User
    fields = "__all__"
    template_name = "accounts/update.html"
    app_name = "accounts"
    url_name = "user_detail"
    permission_required = "accounts.change_user"


class UserDeleteView(BaseDeleteView):
    model = User
    app_name = "accounts"
    url_name = "user_list"
    permission_required = "accounts.delete_user"


class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse("two_factor:login")


class ProfileView(BaseDetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile"
    permission_required = "accounts.view_user"

    def get_object(self, queryset=None):
        # Assuming UserProfile is associated with User model through a OneToOneField named 'user'
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    success_message = "Password Successfully Changed"
    template_name = (
        "accounts/change_password.html"  # Your template for the change password form
    )
    success_url = reverse_lazy(
        "accounts:profile"
    )  # URL to redirect to after successfully changing password

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message


class SuspendUserView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            user.is_active = False
            messages.success(
                self.request, f"User Suspended '{user.email}' successfully!"
            )
            user.save()
        return HttpResponseRedirect(reverse_lazy("accounts:user_list"))


class ReactiveUserView(View):
    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            user.is_active = True
            messages.success(
                self.request, f"User Reactive '{user.email}' successfully!"
            )
            user.save()
        return HttpResponseRedirect(reverse_lazy("accounts:suspend_user_list"))


class UserActionsView(BaseDetailView):
    model = User
    template_name = "accounts/actions.html"
    context_object_name = "user"
    permission_required = "accounts.view_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        clients = Client.objects.filter(created_by_id=user.id)
        services = Service.objects.filter(created_by_id=user.id)
        reception = Reception.objects.filter(created_by_id=user.id)
        appointment = Appointment.objects.filter(created_by_id=user.id)
        # Combine the querysets of clients and services
        action_list = sorted(
            chain(clients, services, reception, appointment),
            key=attrgetter("created_at"),
            reverse=True,
        )

        # Add model names to each instance in the action_list
        for obj in action_list:
            obj.model_name = obj._meta.verbose_name.title()

        context["actions"] = action_list
        return context


class UserSMSListView(BaseListView):
    model = UserSMSLog
    template_name = "accounts/user_sms_log.html"
    filterset_class = UserSMSFilter
    permission_required = "accounts.view_user"

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return UserSMSLog.objects.filter(user_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.kwargs["pk"])
        return context


class UserSentSMSListView(BaseListView):
    model = ClientSMSLog
    template_name = "accounts/user_sent_sms_log.html"
    filterset_class = UserSentSMSFilter
    permission_required = "accounts.view_user"

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return ClientSMSLog.objects.filter(created_by_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.kwargs["pk"])
        return context
