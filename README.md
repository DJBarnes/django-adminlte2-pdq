# Django-AdminLTE-2

Django-AdminLTE-2 is a Django app to easily style all pages and the admin with AdminLTE2.
Additionally there are tools, utilities and additional CSS options to aid in the rapid development of a site.

## Quick start

1. Install the Django App via GitHub for now. Working on getting on Pypi soon.
    ```
    python -m pip install git+https://github.com/DJBarnes/django-adminlte-2.git@master
    ```

2. Add "django_adminlte2" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        'django_adminlte2.apps.DjangoAdminLTE2Config',
        ...
    ]
    ```

3. Django-AdminLTE-2 provides templates for django's account routes and some sample routes. Add the routes to your URLconf if you want to use them.
    ```
    from django.urls import include

    urlpatterns = [
        # Adminlte2 default routes for demo purposes
        path('', include('django_adminlte2.urls')),
        # Django Account Routes - Styled in AdminLTE2
        path('accounts/', include('django.contrib.auth.urls')),
        # Admin - Styled in Django but hosted in AdminLTE2 layout
        path('admin/', admin.site.urls),
    ]
    ```

4. Django-AdminLTE-2 does not include a route or templates for /accounts/profile which is the default Login redirect. Add the following to settings to have successful logins redirect to the sample home page included in Django-AdminLTE-2
    ```
    LOGIN_REDIRECT_URL = 'django_adminlte2:home'
    ```

5. Update settings.py to customize the look and feel of Django-AdminLTE-2

    Alter to whatever your home route is
    ```
    ADMINLTE2_HOME_ROUTE = 'django-adminlte2:home'
    ```

    If you want the admin index page to list the various apps of the django project
    ```
    ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = (True/False)
    ```

    Whether the sidebar menu should have a link to the admin index
    ```
    ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = (True/False)
    ```

    Whether the admin links in the sidebar should be in a tree
    ```
    ADMINLTE2_ADMIN_MENU_IN_TREE - (True/False)
    ```

    Whether the sidebar main nav should be shown when on an admin page in addition to the admin nav
    ```
    ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = (True/False)
    ```

    Whether the sidebar admin nav should be shown when on a main page in addition to the main nav
    ```
    ADMINLTE2_INCLUDE_ADMIN_NAVE_ON_MAIN_PAGES = (True/False)
    ```

    Whether to put in sidebar separators between each menu group
    ```
    ADMINLTE2_USER_MENU_GROUP_SEPARATOR = (True/False)
    ```

    Whether routes with no defined permission should be hidden unless added to a Whitelist
    ```
    ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS = (True/False)
    ```
