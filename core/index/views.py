from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

