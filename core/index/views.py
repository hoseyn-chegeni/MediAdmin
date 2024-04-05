from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
class IndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "index.html"
    permission_required = "index.view_index"
