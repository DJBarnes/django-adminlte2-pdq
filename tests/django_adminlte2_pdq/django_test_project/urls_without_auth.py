"""URL configuration with the package URLs and login/logout, but without Django's other auth URLs."""

# Third-Party Imports.
from django.contrib.auth import views as auth_views
from django.urls import include, path


urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("adminlte2_pdq.urls")),
]
