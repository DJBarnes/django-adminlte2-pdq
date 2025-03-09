Quickstart
**********

1.  Install the Django package via pip.

    .. code-block:: bash

        python -m pip install django-adminlte2-pdq


2.  Add "adminlte2_pdq" to your ``INSTALLED_APPS`` setting in ``<PROJECT_FOLDER>/settings.py`` like this:

    .. code-block:: python

        INSTALLED_APPS = [
            'adminlte2_pdq',
            ...
        ]

    .. important::

        The **adminlte2_pdq** app should be listed before any Django apps so
        that template overriding works correctly.


3.  Django-AdminLTE2-PDQ provides a middleware that is required for some of the
    available authentication and authorization policies from this package to
    function.

    Add this middleware to your middleware list in ``<PROJECT_FOLDER>/settings.py``.

    .. code-block:: python

       MIDDLEWARE = [
           ...
           'adminlte2_pdq.middleware.AuthMiddleware',
       ]


4.  Django-AdminLTE2-PDQ provides routes and templates for a default home page,
    some sample pages, and Django's account pages. You should add these default
    routes to your root URLconf in ``<PROJECT_FOLDER>/urls.py``.

    .. code-block:: python

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

5.  Ensure that successful logins redirect to a valid endpoint.

    Django-AdminLTE2-PDQ does not include a route or templates for
    ``/accounts/profile`` which is the default
    `Django Login redirect. <https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url>`_
    Adding the above entry to your ``settings.py`` file
    will allow successful logins to redirect to the default provided home
    page included in step 4.

    .. code-block:: python

        LOGIN_REDIRECT_URL = 'adminlte2_pdq:home'


6.  The package should now have the required bare minimum setup complete.
    You should be able to run the server and see the default pages located at:
    ``http://localhost:8000``

    For a more detailed setup, consider following the
    :doc:`Longstart <longstart>`.
