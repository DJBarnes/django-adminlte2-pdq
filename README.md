# Django-AdminLTE2-PDQ

[![PyPI](https://img.shields.io/pypi/v/django-adminlte2-pdq?color=blue)](https://img.shields.io/pypi/v/django-adminlte2-pdq?color=blue)
[![Python Versions](https://img.shields.io/badge/python-%3E%3D3.7-brightgreen)](https://img.shields.io/badge/python-%3E%3D3.7-brightgreen)
[![Django Versions](https://img.shields.io/badge/django-%3E%3D3.2-brightgreen)](https://img.shields.io/badge/django-%3E%3D3.2-brightgreen)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Run Tests](https://github.com/DJBarnes/django-adminlte2-pdq/actions/workflows/test.yaml/badge.svg)](https://github.com/DJBarnes/django-adminlte2-pdq/actions/workflows/test.yaml)
[![Coverage Status](https://coveralls.io/repos/github/DJBarnes/django-adminlte2-pdq/badge.svg?branch=main)](https://coveralls.io/github/DJBarnes/django-adminlte2-pdq?branch=main)
[![Documentation Status](https://readthedocs.org/projects/django-adminlte2-pdq/badge/?version=latest)](https://django-adminlte2-pdq.readthedocs.io/en/latest/?badge=latest)
[![GitHub](https://img.shields.io/github/license/DJBarnes/django-adminlte2-pdq)](https://img.shields.io/github/license/DJBarnes/django-adminlte2-pdq)
[![PyPI Downloads per Month](https://img.shields.io/pypi/dm/django-adminlte2-pdq.svg)](https://pypi.python.org/pypi/django-adminlte2-pdq)


**Django-AdminLTE2-PDQ** is a [Django](https://www.djangoproject.com/) app
that takes all of the work out of making a beautiful and functional web
application pretty darn quickly (PDQ) using the
[AdminLTE2](https://adminlte.io/themes/AdminLTE/index2.html)
theme.

Additionally, the app provides decorators, mixins, template filters, and
template tags to aid in the rapid development of a site.

Features include:

* Styled with [AdminLTE2](https://adminlte.io/themes/AdminLTE/index2.html).
* Easy sidebar menu creation.
* Automatic
  [Django Admin](https://docs.djangoproject.com/en/dev/ref/contrib/admin/)
  styling that matches AdminLTE2.
* Automatic inclusion of Admin links in the sidebar.
* Automatic menu link hiding based on user permissions to views.
* Template filters to aid in manual styling.
* Template tags for form rendering that matches AdminLTE2.
* Automatic form error and message styling.
* [Font Awesome 4](https://fontawesome.com/v4/icons/)
  & [Font Awesome 5](https://fontawesome.com/v5/search) integration.
* Highly configurable functionality, via project
  [Django settings variables](https://docs.djangoproject.com/en/dev/topics/settings/).

The full documentation can be found on [Read The Docs](https://django-adminlte2-pdq.readthedocs.io/en/latest/).

![django-adminlte2-pdq-static-menu](https://user-images.githubusercontent.com/4390026/174349983-70984453-1aa5-4976-8749-fadd9028a94c.png)

## Quickstart

1.  Install the Django App via GitHub for now. Working on getting on Pypi soon.
    ```shell
    python -m pip install django-adminlte2-pdq
    ```

2.  Add "adminlte2_pdq" to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        'adminlte2_pdq',
        ...
    ]
    ```

    ---
    :information_source: **NOTE**
    The **adminlte2_pdq** app should be listed before any Django apps so
    that template overriding works correctly.

    ---

3.  Django-AdminLTE2-PDQ provides a middleware that is required for some of the
    available authentication and authorization scenarios from this package to
    function.

    Add this middleware to your middleware list in ``<PROJECT_FOLDER>/settings.py``.

    ```python

       MIDDLEWARE = [
           ...
           'adminlte2_pdq.middleware.AuthMiddleware',
       ]
    ```

4.  Django-AdminLTE2-PDQ provides routes and templates for a default home page,
    some sample pages, and Django's account pages. You should add these default
    routes to your root URLconf in ``<PROJECT_FOLDER>/urls.py``

    ```python
    from django.contrib import admin
    from django.urls import include

    urlpatterns = [
        # Adminlte2 default routes for demo purposes
        path('', include('adminlte2_pdq.urls')),
        # Django Account Routes - Styled in AdminLTE2
        path('accounts/', include('django.contrib.auth.urls')),
        # Admin - Styled in Django but hosted in AdminLTE2 layout
        path('admin/', admin.site.urls),
    ]
    ```

5.  Ensure that successful logins redirect to a valid endpoint.

    Django-AdminLTE2-PDQ does not include a route or templates for
    `/accounts/profile` which is the default
    [Django Login redirect.](https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url)
    Adding the above entry to your `settings.py` file
    will allow successful logins to redirect to the default provided home page
    included in step 4.

    ```python
    LOGIN_REDIRECT_URL = 'adminlte2_pdq:home'
    ```

6.  The package should now have the required bare minimum setup complete.
    You should be able to run the server and see the default pages located at:
    ``http://localhost:8000``

    For a more detailed setup, consider reading the
    [Longstart](https://django-adminlte2-pdq.readthedocs.io/en/latest/longstart.html)
    and the rest of the full documentation on
    [Read The Docs](https://django-adminlte2-pdq.readthedocs.io/en/latest/).
