"""URL configuration with only the Django admin, without the package's URLs."""

# Third-Party Imports.
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
]
