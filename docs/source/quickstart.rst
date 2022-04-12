Quickstart
==========

1. Install the Django App via GitHub for now. Working on getting on Pypi soon.
    .. code-block:: bash

        python -m pip install git+https://github.com/DJBarnes/django-adminlte-2.git@master


2. Add "django_adminlte_2" to your INSTALLED_APPS setting like this:
    .. code-block:: python

        INSTALLED_APPS = [
            'django_adminlte_2',
            ...
        ]


3. Django-AdminLTE-2 provides templates for django's account routes and some sample routes. Add the routes to your URLconf if you want to use them.
    .. code-block:: python

        from django.urls import include

        urlpatterns = [
            # Adminlte2 default routes for demo purposes
            path('', include('django_adminlte_2.urls')),
            # Django Account Routes - Styled in AdminLTE2
            path('accounts/', include('django.contrib.auth.urls')),
            # Admin - Styled in Django but hosted in AdminLTE2 layout
            path('admin/', admin.site.urls),
        ]

4. Django-AdminLTE-2 does not include a route or templates for /accounts/profile which is the default Login redirect. Add the following to settings to have successful logins redirect to the sample home page included in Django-AdminLTE-2
    .. code-block:: python

        LOGIN_REDIRECT_URL = 'django_adminlte_2:home'


5. Update settings.py to customize the look and feel of Django-AdminLTE-2

   See the :doc:`configuration` section for more information.


6. Override templates to further customize the look and feel of
   Django-AdminLTE-2

   See the :doc:`templates` section for more information.
