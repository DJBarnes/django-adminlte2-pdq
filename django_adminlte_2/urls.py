"""
Django AdminLTE2 Default URL Configuration
"""
from . import views
from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

app_name = 'django_adminlte_2'
urlpatterns = [
    # Redirects to the home page
    path('', RedirectView.as_view(
        pattern_name=getattr(
            settings,
            'ADMINLTE2_HOME_ROUTE',
            'django_adminlte_2:home'
        ),
        permanent=False
    )),
    # Sample pages
    path(
        'home/',
        views.home,
        name="home"
    ),
    path(
        'accounts/register/',
        views.register,
        name="register"
    ),
    path(
        'sample1/',
        views.sample1,
        name="sample1"
    ),
    path(
        'sample2/',
        views.sample2,
        name="sample2"
    ),
    path(
        'demo-css/',
        views.demo_css,
        name="demo-css"
    ),
]
