# Django-AdminLTE-2

**Django-AdminLTE-2** is a [Django](https://www.djangoproject.com/) app
that takes all of the work out of making a beautiful and functional web
application using the
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
* Automatic form error and messages styling.
* [Font Awesome 4](https://fontawesome.com/v4/icons/)
  & [Font Awesome 5](https://fontawesome.com/v5/search) integration.
* Highly configurable functionality, via project
  [Django settings variables](https://docs.djangoproject.com/en/dev/topics/settings/).

The full documentation can be found on [Read The Docs](#) (coming soon).

![django-adminlte-2-static-menu](https://user-images.githubusercontent.com/4390026/174349983-70984453-1aa5-4976-8749-fadd9028a94c.png)

## Quickstart

1.  Install the Django App via GitHub for now. Working on getting on Pypi soon.
    ```shell
    python -m pip install git+https://github.com/DJBarnes/django-adminlte-2.git@master
    ```

2.  Add "django_adminlte_2" to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        'django_adminlte_2',
        ...
    ]
    ```

    ---
    :information_source: **NOTE**
    The **django_adminlte_2** app should be listed before any django apps so
    that template overriding works correctly. Additionally, if you plan to
    override any Django-AdminLTE-2 templates, they should be listed above
    the **django_adminlte_2 app**.

    ---

3.  Django-AdminLTE-2 provides a middleware that is required for some of the
    available authentication and authorization scenarios from this package to
    function.

    Add this middleware to your middleware list in ``settings.py``.

    Once installed the available scenarios are controlled by changing settings
    in your ``settings.py`` file.
    For more information about the various scenarios and associated settings
    refer to the full documentation on [Read The Docs](#) (coming soon).

    ```python

       MIDDLEWARE = [
           ...
           'django_adminlte_2.middleware.AuthMiddleware',
       ]
    ```

    ---
    :information_source: **NOTE**
    Django-AdminLTE-2 has been configured out of the box to get you setup
    and running as fast as possible. As a result, the settings surrounding
    authentication and authorization are not as strict as they could be.
    We **strongly** encourage you to read the Authentication and Authorization
    section on [Read The Docs](#) (coming soon) once you get the basics of this
    package working.

    ---

4.  Django-AdminLTE-2 provides templates for django's account routes and some
    sample routes. Add the routes to your URLconf if you want to use them.
    ```python
    from django.contrib import admin
    from django.urls import include

    urlpatterns = [
        # Adminlte2 default routes for demo purposes
        path('', include('django_adminlte_2.urls')),
        # Django Account Routes - Styled in AdminLTE2
        path('accounts/', include('django.contrib.auth.urls')),
        # Admin - Styled in Django but hosted in AdminLTE2 layout
        path('admin/', admin.site.urls),
    ]
    ```

5.  Ensure that the login redirect will work.
    ```python
    LOGIN_REDIRECT_URL = 'django_adminlte_2:home'
    ```
    ---
    :information_source: **NOTE**
    Django-AdminLTE-2 does not include a route or templates for
    `/accounts/profile` which is the default
    [Django Login redirect.](https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url)
    Adding the above entry to your `settings.py` file
    will allow successful logins to redirect to the sample home page
    included in Django-AdminLTE-2 until a proper profile route is set up.

    ---

6.  Update ``settings.py`` to customize the look and feel of
    **Django-AdminLTE-2**. Common configuration options are listed below in the
    [configuration section](#configuration).

    For the full list of configuration options refer to the documentation on
    [Read The Docs](#).

7. Override templates to further customize the look and feel of
   **Django-AdminLTE-2**.

   See the Templates section on [Read The Docs](#) for more information.

## Configuration

### Home

Set the "Home" route for your project. This tells the package where to redirect
users when they click a link that is designed to take the user home.
```python
ADMINLTE2_HOME_ROUTE = 'django_adminlte_2:home'
```

Set the Logo text for your site. This will be shown in the top left of the top
bar, when the side bar is expanded.
```python
ADMINLTE2_LOGO_TEXT = 'My Awesome Site'
```

Set the small Logo text for your site. This will be shown in the top left of the
top bar, when the side bar is collapsed.
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

By default the main navigation (non-admin) menu is not part of the sidebar when
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

By default there will be a implicit separator bar rendered between each menu
group.
These groups include: **MENU_FIRST**, **MENU**, **MENU_LAST**, and the
**Admin Menu**.
More information about these groups can be found on the
[Read The Docs Admin page](#). If you would like to disable this
separator from being automatically rendered, set this value to ``False``.
```python
ADMINLTE2_USE_MENU_GROUP_SEPARATOR = (True/False)
```

This setting is the definition for the main navigation menu.
There are a lot of options when creating this menu.
See the [Read The Docs Menu page](#) for a detailed explanation on how to
create this menu and all of the available options that can be used.
```python
ADMINLTE2_MENU = []
```

### Admin

By default the admin menu sidebar will not have a link to the admin index page.
If you would like to append a link to the admin index page in the sidebar,
set this value to ``True``.
```python
ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = (True/False)
```

By default Django-AdminLTE-2 will put the Apps on the Admin Index page
into AdminLTE Info Boxes. Setting this to ``True`` will change that look
to the traditional Django list view, but still within the main AdminLTE site
styling.
```python
ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = (True/False)
```

### Authorization

Whether routes with no defined permission should be hidden unless added to a
Whitelist.

If this setting is set to False, then all routes without a defined permission
are still visible on the sidebar menu.

If this setting is set to True, then all routes without a defined permission
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
