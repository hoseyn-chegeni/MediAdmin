from .models import User
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, UserUpdateForm
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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from logs.models import UserSMSLog, ClientSMSLog
from client.models import Client
from reception.models import Reception
from planner.models import Session
from financial.models import OfficeExpenses
from doctor.models import Doctor
from insurance.models import Insurance
from prescription.models import Prescription
from services.models import Service
from tasks.models import Task
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import View, DetailView
from consumable.models import ConsumableV2, Supplier
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.timezone import now
from datetime import timedelta


# Create your views here.
class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"

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
        context["appointments"] = Session.objects.filter(created_by_id=user.id).count()
        context["user_count"] = User.objects.filter(created_by_id=user.id).count()
        # context["consumable"] = Consumable.objects.filter(created_by_id=user.id).count()
        context["office_expenses"] = OfficeExpenses.objects.filter(
            created_by_id=user.id
        ).count()
        context["doctor"] = Doctor.objects.filter(created_by_id=user.id).count()
        context["insurance"] = Insurance.objects.filter(created_by_id=user.id).count()
        context["prescription"] = Prescription.objects.filter(
            created_by_id=user.id
        ).count()
        context["service"] = Service.objects.filter(created_by_id=user.id).count()
        context["created_task"] = Task.objects.filter(created_by_id=user.id).count()
        context["assign_task"] = Task.objects.filter(assign_to_id=user.id).count()
        context["consumable"] = ConsumableV2.objects.filter(
            created_by_id=user.id
        ).count()
        context["supplier"] = Supplier.objects.filter(created_by_id=user.id).count()

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
    form_class = UserUpdateForm
    template_name = "accounts/update.html"
    app_name = "accounts"
    url_name = "user_detail"
    permission_required = "accounts.change_user"


class UserDeleteView(BaseDeleteView):
    model = User
    app_name = "accounts"
    url_name = "user_list"
    permission_required = "accounts.delete_user"
    message = "کاربر با موفقیت حذف شد"


def logout_view(request):
    logout(request)
    # Redirect to a desired URL after logout
    return redirect(
        "two_factor:login"
    )  # Replace 'login' with the name of your login URL pattern


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    success_message = "رمز عبور با موفقیت تغییر داده شد"
    template_name = (
        "accounts/change_password.html"  # Your template for the change password form
    )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.request.user.id})


class SuspendUserView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            user.is_active = False
            messages.success(self.request, f"کاربر با موفقیت غیرفعال شد.")
            user.save()
        return HttpResponseRedirect(
            reverse_lazy("accounts:user_detail", kwargs={"pk": user.id})
        )


class ReactiveUserView(View):
    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            user.is_active = True
            messages.success(self.request, f"کاربر با موفقیت فعال شد.")
            user.save()
        return HttpResponseRedirect(
            reverse_lazy("accounts:user_detail", kwargs={"pk": user.id})
        )


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


class LoginAsUserView(PermissionRequiredMixin, View):
    permission_required = "accounts.super_user"

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if (
                request.user.is_superuser
            ):  # Check if the current user is a superuser (admin)
                login(request, user)
        except User.DoesNotExist:
            pass  # Handle the case where the user does not exist
        return redirect("index:index")


class DeleteSelectedUsersView(View):
    def post(self, request):
        if request.method == "POST":
            user_ids = request.POST.getlist(
                "user_ids"
            )  # Get the list of selected user IDs from the form
            deleted_users_count = User.objects.filter(
                id__in=user_ids
            ).delete()  # Delete selected users
            messages.success(
                request, f"تعداد {deleted_users_count[0]} کاربر با موفقیت حذف شدند."
            )  # Add success message
        return redirect("accounts:user_list")


#############################
#############################
#############################
######## REPORT LIST ########
#############################
#############################
#############################


class ActiveUserListView(BaseListView):
    model = User
    template_name = "accounts/reports/active_list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SuspendUserListView(BaseListView):
    model = User
    template_name = "accounts/reports/suspend_list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class InActiveForMonthUserListVIew(BaseListView):
    model = User
    template_name = "accounts/reports/in_active_list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self):
        one_month_ago = now() - timedelta(days=30)
        return super().get_queryset().filter(last_login__lt=one_month_ago)


class NewUserListView(BaseListView):
    model = User
    template_name = "accounts/reports/new_list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

    def get_queryset(self):
        one_month_ago = now() - timedelta(days=30)
        return super().get_queryset().filter(created_at__gte=one_month_ago)
