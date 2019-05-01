"""
*pylabber* URL Configuration
----------------------------

The `urlpatterns <https://docs.djangoproject.com/en/2.0/topics/http/urls/>`_ list routes URLs to views.

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
from django.views.generic.base import TemplateView
from accounts.choices import Position
from accounts.models import Profile, TITLE_ORDERING_SQL

BADGE_CLASS = {
    Position.PI.name: "dark",
    Position.POST.name: "primary",
    Position.AFF.name: "secondary",
    Position.PHD.name: "success",
    Position.MSC.name: "info",
    Position.MAN.name: "danger",
    Position.RA.name: "warning",
}

urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="home.html",
            extra_context={
                "members": Profile.objects.extra(
                    select={"position_order": TITLE_ORDERING_SQL},
                    order_by=["position_order"],
                ),
                "badge_class": BADGE_CLASS,
            },
        ),
        name="home",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("dicom/", include("django_dicom.urls", namespace="dicom")),
    # path("smb/", include("django_smb.urls", namespace="smb")),
    path("research/", include("research.urls", namespace="research")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
