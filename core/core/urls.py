"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as tf_urls


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include(tf_urls)),
        path("index/", include("index.urls")),
        path("accounts/", include("accounts.urls")),
        path("client/", include("client.urls")),
        path("reception/", include("reception.urls")),
        path("insurance/", include("insurance.urls")),
        path("services/", include("services.urls")),
        path("asset/", include("asset.urls")),
        path("doctor/", include("doctor.urls")),
        path("prescription/", include("prescription.urls")),
        path("financial/", include("financial.urls")),
        path("booking/", include("booking.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
