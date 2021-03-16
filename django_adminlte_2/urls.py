"""Django AdminLTE2 Default URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
