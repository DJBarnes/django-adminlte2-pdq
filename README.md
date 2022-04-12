# Django-AdminLTE-2

Django-AdminLTE-2 is a Django app to easily style all pages and the admin with AdminLTE2.
Additionally there are tools, utilities and additional CSS options to aid in the rapid development of a site.

## Quick start

1. Install the Django App via GitHub for now. Working on getting on Pypi soon.
    ```shell
    python -m pip install git+https://github.com/DJBarnes/django-adminlte-2.git@master
    ```

2. Add "django_adminlte_2" to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        'django_adminlte_2',
        ...
    ]
    ```

3. Django-AdminLTE-2 provides templates for django's account routes and some sample routes. Add the routes to your URLconf if you want to use them.
    ```python
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

4. Django-AdminLTE-2 does not include a route or templates for /accounts/profile which is the default Login redirect. Add the following to settings to have successful logins redirect to the sample home page included in Django-AdminLTE-2
    ```python
    LOGIN_REDIRECT_URL = 'django_adminlte_2:home'
    ```

5. Update settings.py to customize the look and feel of Django-AdminLTE-2

    Alter to whatever your home route is
    ```python
    ADMINLTE2_HOME_ROUTE = 'django_adminlte_2:home'
    ```

    If you want the admin index page to put the various apps in a list format rather than AdminLTE2 Info Boxes.
    ```python
    ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = (True/False)
    ```

    Whether the sidebar menu should have a link to the admin index
    ```python
    ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = (True/False)
    ```

    Whether the admin links in the sidebar should be in a tree
    ```python
    ADMINLTE2_ADMIN_MENU_IN_TREE - (True/False)
    ```

    Whether the sidebar main nav should be shown when on an admin page in addition to the admin nav
    ```python
    ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = (True/False)
    ```

    Whether the sidebar admin nav should be shown when on a main page in addition to the main nav
    ```python
    ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES = (True/False)
    ```

    Whether to put in sidebar separators between each menu group
    ```python
    ADMINLTE2_USE_MENU_GROUP_SEPARATOR = (True/False)
    ```

    Whether routes with no defined permission should be hidden unless added to a Whitelist
    If this setting is set to False, then all routes without a defined permission are still visible on the sidebar menu
    If this setting is set to True, then all routes without a defined permission are hidden on the sidebar menu unless the route is found in the ```ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST``` setting.
    ```python
    ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS = (True/False)
    ```

    Assuming ```ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS``` is set to True, this is the list of routes that will be shown on the sidebar menu and accessible despite a defined permission.
    ```python
    ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST = []
    ```

    This menu setting is useful for defining a menu that should come before the main menu. Sometimes you may be in a subsection of your website that has additional navigation that should precede the normal main navigation but only be shown when in this subsection. This setting allows that without having to change the main navigation menu.
    See the Menu section (coming soon) for more information.
    ```python
    ADMINLTE2_MENU_FIRST = []
    ```

    This menu setting is the main menu that should be available no matter what section of the website you are in. It is the main navigation.
    See the Menu section (coming soon) for more information.
    ```python
    ADMINLTE2_MENU = []
    ```

    This menu setting is useful for defining a menu that should come after the admin menu links. A menu footer so to speak.
    See the Menu section (coming soon) for more information.
    ```python
    ADMINLTE2_MENU_LAST = []
    ```

6. Override and update blocks in base.html to customize the layout further
    1. Create ```adminlte2/base.html``` in one of your django projects template folders
    2. Extend the packages default base.html by adding the following line to the file created above.
        ```htmldjango
        {% extends "adminlte2/base.html" %}
        ```
    3. Override the skin class to set the color theme of the site by adding the following line to the file created above.
        Valid values can be found here: https://adminlte.io/docs/2.4/layout
        ```htmldjango
        {% block skin_class %}skin-blue{% endblock skin_class %}
        ```
    4. Optionally override any other template blocks that you would like to either remove or change the implementation of
