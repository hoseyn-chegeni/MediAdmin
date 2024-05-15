from  django.urls import path
from .views import UserImportView

app_name = 'import'

urlpatterns = [
        path("user/", UserImportView.as_view(), name="user"),

]