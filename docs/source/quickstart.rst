Quickstart
**********

1.  Install the Django App via GitHub for now. Working on getting on Pypi soon.

    .. code-block:: bash

        python -m pip install django-adminlte2-pdq


2.  Add "adminlte2_pdq" to your INSTALLED_APPS setting like this:

    .. code-block:: python

        INSTALLED_APPS = [
            'adminlte2_pdq',
            ...
        ]

    .. important::

        The **adminlte2_pdq** app should be listed before any Django apps so
        that template overriding works correctly. Additionally, if you plan to
        override any Django-AdminLTE2-PDQ templates, they should be listed above
        the **adminlte2_pdq** app.


3.  Django-AdminLTE2-PDQ provides a middleware that is required for some of the
    available authentication and authorization scenarios from this package to
    function.

    Add this middleware to your middleware list in ``settings.py``.

    Once installed the available scenarios are controlled by changing settings
    in your ``settings.py`` file.
    For more information about the various scenarios and associated settings
    refer to the
    :doc:`Authentication and Authorization <authorization/policies>` section.

    .. code-block:: python

       MIDDLEWARE = [
           ...
           'adminlte2_pdq.middleware.AuthMiddleware',
       ]

    .. note::

        Django-AdminLTE2-PDQ has been configured out of the box to get you set up
        and running as fast as possible. As a result, the settings surrounding
        authentication and authorization are not as strict as they could be.
        We **strongly** encourage you to read the section on
        :doc:`Authentication and Authorization <authorization/policies>`
        once you get the basics of this package working.


4.  Django-AdminLTE2-PDQ provides templates for Django's account routes and some
    sample routes. Add the routes to your URLconf if you want to use them.

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

5.  Ensure that the login redirect will work.

    .. code-block:: python

        LOGIN_REDIRECT_URL = 'adminlte2_pdq:home'

    .. note::
        Django-AdminLTE2-PDQ does not include a route or templates for
        ``/accounts/profile`` which is the default
        `Django Login redirect. <https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url>`_
        Adding the above entry to your ``settings.py`` file
        will allow successful logins to redirect to the sample home page
        included in Django-AdminLTE2-PDQ until a proper profile route is set up.

6.  Update ``settings.py`` to customize the look and feel of
    **Django-AdminLTE2-PDQ**.

    See the :doc:`Configuration <configuration/home>` pages for more information.


7.  Override templates to further customize the look and feel of
    **Django-AdminLTE2-PDQ**.

    See the :doc:`Templates <templates/templates>` pages for more information.
