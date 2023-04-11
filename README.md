# Django-AdminLTE2-PDQ

[![Documentation Status](https://readthedocs.org/projects/django-adminlte2-pdq/badge/?version=latest)](https://django-adminlte2-pdq.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/django-adminlte2-pdq?color=blue)](https://img.shields.io/pypi/v/django-adminlte2-pdq?color=blue)
[![Python Versions](https://img.shields.io/badge/python-%3E%3D3.7-brightgreen)](https://img.shields.io/badge/python-%3E%3D3.7-brightgreen)
[![Django Versions](https://img.shields.io/badge/django-%3E%3D3-brightgreen)](https://img.shields.io/badge/django-%3E%3D3-brightgreen)
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
    that template overriding works correctly. Additionally, if you plan to
    override any Django-AdminLTE2-PDQ templates, they should be listed above
    the **adminlte2_pdq app**.

    ---

3.  Django-AdminLTE2-PDQ provides a middleware that is required for some of the
    available authentication and authorization scenarios from this package to
    function.

    Add this middleware to your middleware list in ``settings.py``.

    Once installed the available scenarios are controlled by changing settings
    in your ``settings.py`` file.
    For more information about the various scenarios and associated settings
    refer to the full documentation on
    [Read The Docs](https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html).

    ```python

       MIDDLEWARE = [
           ...
           'adminlte2_pdq.middleware.AuthMiddleware',
       ]
    ```

    ---
    :information_source: **NOTE**
    Django-AdminLTE2-PDQ has been configured out of the box to get you set up
    and running as fast as possible. As a result, the settings surrounding
    authentication and authorization are not as strict as they could be.
    We **strongly** encourage you to read the Authentication and Authorization
    section on
    [Read The Docs](https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html)
    once you get the basics of this package working.

    ---

4.  Django-AdminLTE2-PDQ provides templates for django's account routes and some
    sample routes. Add the routes to your URLconf if you want to use them.
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

5.  Ensure that the login redirect will work.
    ```python
    LOGIN_REDIRECT_URL = 'adminlte2_pdq:home'
    ```
    ---
    :information_source: **NOTE**
    Django-AdminLTE2-PDQ does not include a route or templates for
    `/accounts/profile` which is the default
    [Django Login redirect.](https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url)
    Adding the above entry to your `settings.py` file
    will allow successful logins to redirect to the sample home page
    included in Django-AdminLTE2-PDQ until a proper profile route is set up.

    ---

6.  Update ``settings.py`` to customize the look and feel of
    **Django-AdminLTE2-PDQ**. Common configuration options are listed below in the
    [configuration section](#configuration).

    For the full list of configuration options refer to the documentation on
    [Read The Docs](https://django-adminlte2-pdq.readthedocs.io/en/latest/configuration/home.html).

7. Override templates to further customize the look and feel of
   **Django-AdminLTE2-PDQ**.

   See the Templates section on
   [Read The Docs](https://django-adminlte2-pdq.readthedocs.io/en/latest/templates/templates.html)
   for more information.

## Configuration

### Home

Set the "Home" route for your project. This tells the package where to redirect
users when they click a link that is designed to take the user home.
```python
ADMINLTE2_HOME_ROUTE = 'adminlte2_pdq:home'
```

Set the Logo text for your site. This will be shown in the top left of the top
bar when the sidebar is expanded.
```python
ADMINLTE2_LOGO_TEXT = 'My Awesome Site'
```

Set the small Logo text for your site. This will be shown in the top left of the
top bar when the sidebar is collapsed.
```python
ADMINLTE2_LOGO_TEXT = 'MAS'
```

Set the skin class to use for the site. Valid skin classes can be found on the
[AdminLTE documentation](https://adminlte.io/themes/AdminLTE/documentation/)
page.
```python
ADMINLTE2_SKIN_CLASS = 'skin-green-light'
```

### Menu

By default, the main navigation (non-admin) menu is not part of the sidebar when
the user is viewing a
[Django Admin page](https://docs.djangoproject.com/en/dev/ref/contrib/admin/)
If you would like users to be able to see all of the main nav links regardless
of what page they are on, set this value to ``True``.
```python
ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = (True/False)
```

By default, the admin navigation menu is not part of the sidebar when the user
is viewing a main navigation
(non-[Django-Admin](https://docs.djangoproject.com/en/dev/ref/contrib/admin/))
page. If you would like users to be able to see all of the admin nav links
regardless of what page they are on, set this value to ``True``.
```python
ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES = (True/False)
```

By default, there will be an implicit separator bar rendered between each menu
group.
These groups include: **MENU_FIRST**, **MENU**, **MENU_LAST**, and the
**Admin Menu**.
More information about these groups can be found on the
[Read The Docs Admin page](https://django-adminlte2-pdq.readthedocs.io/en/latest/menu/general_information.html).
If you would like to disable this
separator from being automatically rendered, set this value to ``False``.
```python
ADMINLTE2_USE_MENU_GROUP_SEPARATOR = (True/False)
```

This setting is the definition for the main navigation menu.
There are a lot of options when creating this menu.
See the
[Read The Docs Menu page](https://django-adminlte2-pdq.readthedocs.io/en/latest/menu/general_information.html)
for a detailed explanation of how to
create this menu and all of the available options that can be used.
```python
ADMINLTE2_MENU = []
```

### Admin

By default, the admin menu sidebar will not have a link to the admin index page.
If you would like to append a link to the admin index page in the sidebar,
set this value to ``True``.
```python
ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = (True/False)
```

By default, Django-AdminLTE2-PDQ will put the Apps on the Admin Index page
into AdminLTE Info Boxes. Setting this to ``True`` will change that look
to the traditional Django list view, but still within the main AdminLTE site
styling.
```python
ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = (True/False)
```

### Authorization

Whether routes with no defined permission should be hidden unless added to a
Whitelist.

If this setting is set to False, then all routes without defined permissions
are still visible on the sidebar menu.

If this setting is set to True, then all routes without defined permissions
are hidden on the sidebar menu unless the route is found in the
``ADMINLTE2_STRICT_POLICY_WHITELIST`` setting.
```python
ADMINLTE2_USE_STRICT_POLICY = (True/False)
```

Assuming ``ADMINLTE2_USE_STRICT_POLICY`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible, despite said routes having no defined permission.
```python
ADMINLTE2_STRICT_POLICY_WHITELIST = []
```
