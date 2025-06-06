"""sample_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path


# Will use the custom 404 provided by the package.
handler404 = "adminlte2_pdq.views.view_404"


urlpatterns = [
    # Standard "Django Admin" views, in Adminlte2 format.
    path("admin/", admin.site.urls),
    # Testing views.
    path("tests/", include("tests.django_adminlte2_pdq.testing.test_urls")),
    path("tests-2/", include("tests.django_adminlte2_pdq.testing.test_urls_2")),
    # Adminlte2 views.
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("adminlte2_pdq.urls")),
]
