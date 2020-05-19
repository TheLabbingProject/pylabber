"""
*pylabber* URL Configuration
----------------------------

The `urlpatterns <https://docs.djangoproject.com/en/2.0/topics/http/urls/>`_ list routes
URLs to views.

Examples:
* Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
* Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
* Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("django.contrib.auth.urls")),
    path("api/", include(router.urls)),
    path("api/", include("accounts.urls", namespace="accounts")),
    path("api/", include("django_dicom.urls", namespace="dicom")),
    path("api/", include("research.urls", namespace="research")),
    path("api/", include("django_mri.urls", namespace="mri")),
    path("api/", include("django_analyses.urls", namespace="analyses")),
    path("api/auth/", include("rest_auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
