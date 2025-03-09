Longstart
**********

1.  Install the Django package via pip.

    .. code-block:: bash

        python -m pip install django-adminlte2-pdq


2.  Add "adminlte2_pdq" to your INSTALLED_APPS setting in ``<PROJECT_FOLDER>/settings.py`` like this:

    .. code-block:: python

        INSTALLED_APPS = [
            'adminlte2_pdq',
            ...
        ]

    .. important::

        The **adminlte2_pdq** app should be listed before any Django apps so
        that template overriding works correctly. Additionally, if you plan to
        override any Django-AdminLTE2-PDQ templates, the apps containing those
        templates should be listed above the **adminlte2_pdq** app.


3.  Django-AdminLTE2-PDQ provides a middleware that is required for some of the
    available authentication and authorization policies from this package to
    function.

    Add this middleware to your middleware list in ``<PROJECT_FOLDER>/settings.py``.

    Once this middleware is installed various authentication and authorization
    policies become available. They are all controlled by changing various
    settings in your ``settings.py`` file.
    For more information about the various policies and associated settings
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


4.  Django-AdminLTE2-PDQ provides routes and templates for a default home page,
    some sample pages, and Django's account pages. You can add these default
    routes to your root URLconf in ``<PROJECT_FOLDER>/urls.py`` if you would
    like to use them.

    .. note::

        Using the included routes and templates requires that your
        ``urlpatterns`` has both the routes from the package added as well
        as the ``accounts`` routes provided by Django. See sample code below.

    .. warning::

        Opting not to use these default routes requires that you configure the
        :doc:`ADMINLTE2_HOME_ROUTE </configuration/home>`
        setting, as some parts of the default templates expect
        that your site has at minimum, a home page, defined in that setting.

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
    page included in step 4. At least until a proper profile route can be
    set up.

    .. code-block:: python

        LOGIN_REDIRECT_URL = 'adminlte2_pdq:home'

    .. warning::

        If you are not using the default urls from step 4, we assume that you
        already know where you would like to have users redirected to on
        successful login and thus have already done this step with a different
        value.

6.  Update ``settings.py`` to customize the look and feel of
    **Django-AdminLTE2-PDQ**.

    See the :doc:`Configuration <configuration/home>` pages for more information.


7.  Override templates to further customize the look and feel of
    **Django-AdminLTE2-PDQ**.

    See the :doc:`Templates <templates/templates>` pages for more information.

8.  The package should now have the required bare minimum setup complete.
    You should be able to run the server and see the default pages located at:
    ``http://localhost:8000``
