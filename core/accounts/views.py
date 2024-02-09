from .models import User
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .froms import CustomUserCreationForm


# Create your views here.
class UserListView(ListView):
    model = User
    template_name = "accounts/list.html"
    permission_required = "accounts.view_user"
    context_object_name = "users"


class UserDetailView(DetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/create.html"
   

    def get_success_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.object.pk})


class UserUpdateView(UpdateView):
    model = User
    fields = ("first_name", "last_name")
    template_name = "accounts/update.html"

    def get_success_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.object.pk})

class UserDeleteView(DeleteView):
    model = User
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("accounts:user_list")
