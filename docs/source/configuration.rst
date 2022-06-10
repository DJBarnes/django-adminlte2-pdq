Configuration
*************

There are various configuration options that can be set via Django Settings to
control the overall look, feel, and functionality of the package.
All settings are listed here for reference even though some of these settings
such as the :doc:`menu` and :doc:`authorization` can become quite complex and
have dedicated documentation pages to better explain the full extent of these
settings.

----

Home Configuration
==================

ADMINLTE2_HOME_ROUTE
--------------------

Set the "Home" route for you project so that the package knows
where to redirect users when they click a link that is designed
to take the user home.

:Type: ``string``
:Default: ``django_adminlte_2:home``

Example::

    ADMINLTE2_HOME_ROUTE = 'django_adminlte_2:home'

----

Menu Configuration
==================

ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES
-----------------------------------------

By default the main navigation (non-admin) is not part of the sidebar when the
user is viewing an admin page. If you would like users to be able to see all of
the main nav links regardless of what page they are on, set this setting to
``True``.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = {True|False}


ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES
-----------------------------------------

By default, admin navigation is not part of the sidebar when the user is
viewing a main navigation (non-admin) page. If you would like users to be able
to see all of the admin nav links regardless of what page they are on, set this
setting to ``True``.

.. note::

    Visibility is still subject to a user having the ``is_staff`` property.
    Without that property, the admin section of the sidebar will still be
    hidden to the user regardless of this setting.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES = {True|False}


ADMINLTE2_USE_MENU_GROUP_SEPARATOR
----------------------------------

By default there will be a implicit separator bar rendered between each menu
group.
These groups include: **MENU_FIRST**, **MENU**, **MENU_LAST**, and the
**Admin Menu**.
More information about these groups can be found on the :doc:`menu` page.
If you would like to disable this separator from being automatically rendered
set this setting to ``False``.


:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_USE_MENU_GROUP_SEPARATOR = {True|False}


ADMINLTE2_MENU
--------------

This setting is the definition for the main navigation menu.
There are a lot of options when creating this menu.
See the :doc:`menu` section for a detailed explanation on how to create this
menu and all of the available options that can be used.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_MENU = []

----

Admin Configuration
===================

.. important::

    All of the settings in this section manipulate the admin section of the
    sidebar.

    However, by default, the admin sidebar section is only shown on
    `Django Admin pages <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
    . If you would like to change this behavior so that the admin sidebar
    section is available on all pages, please see the
    :ref:`configuration:ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES` section for
    more information.


ADMINLTE2_INCLUDE_ADMIN_HOME_LINK
---------------------------------

By default the admin menu sidebar will not have a link to the admin index page.
If you would like to see a link to the admin index page in the sidebar, set this
setting to ``True``.

.. note::

    This link is in essence another Admin link and as such will be treated like
    all other admin links. If you do not see this link in your sidebar after
    enabling, please refer to the
    :ref:`configuration:ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES`
    setting for more information.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = {True|False}


ADMINLTE2_ADMIN_INDEX_USE_APP_LIST
----------------------------------

By default Django-AdminLTE-2 will put the Apps on the Admin Index page
into AdminLTE Info Boxes. Setting this to ``True`` will change that look
to the traditional Django list view but still within the main AdminLTE site
styling.

.. note::

    If you do not see a link for the admin index page in the sidebar, please
    refer to the :ref:`configuration:ADMINLTE2_INCLUDE_ADMIN_HOME_LINK`
    setting for information on how to enable it.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = {True|False}


ADMINLTE2_ADMIN_MENU_IN_TREE
----------------------------

By default the admin sidebar will render a root entry for each app in the
project. Each app entry will be a tree that can be collapsed and expanded to
reveal entries for the models in that app.

Additionally, the entire admin sidebar section can be grouped into a tree. This
will allow the entire admin menu section to be collapsible. To enable this
behavior, change this setting to ``True``.

.. note::

    You can refer to the :ref:`menu:tree` section of the :doc:`menu` page for
    more information about how trees work and are defined.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_ADMIN_MENU_IN_TREE = {True|False}


ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS
------------------------------------

By default, when viewing a Django admin page, there is a tri-cog icon in the
top right corner of the top bar that shows additional information via a
popped out sidebar when clicked. The default content is the "Recent Activity"
section of the admin. In addition to this, up to two additional sections of
information can be added to this popped out sidebar. When more than one section
of information is configured to be shown, tabs are automatically created to be
able to easily switch between those sections on the popped out sidebar.

Since the control sidebar can contain between zero and three tabs, this
single setting controls the visibility of all three of those tabs.
The main setting is called ``ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS``, which is
a dictionary of additional settings. Each of which will either turn on or off
one of the tabs in the sidebar.

The additional settings consist of:

* ``SHOW_RECENT_ACTIVITY_TAB`` - Shows the Recent Activity of the admin.
* ``SHOW_SETTINGS_TAB`` - A good place for any admin related additional settings.
* ``SHOW_EXTRA_TABS`` - An extra tab for whatever else you might need.

The **RECENT_ACTIVITY_TAB** content is automatically generated by the admin.
The content for the other optional tabs must be created by overriding some of
the templates that come with this package. The templates that you would need to
look at and potentially override are:

* ``admin/partials/_control_sidebar.html``
* ``admin/partials/_control_sidebar/_tabs.html``
* ``admin/partials/_control_sidebar/_recent_activity_tab_pane.html``
* ``admin/partials/_control_sidebar/_settings_tab_pane.html``
* ``admin/partials/_control_sidebar/_extra_tab_panes.html``

If all of the tabs are turned off, the entire tri-cog icon and associated
button will be removed and the user dropdown will shift to the right.

:Type: ``dict``
:Default: ``{'SHOW_RECENT_ACTIVITY_TAB': True,}``

Example::

    ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS = {
        'SHOW_RECENT_ACTIVITY_TAB': {True|False},
        'SHOW_SETTINGS_TAB': {True|False},
        'SHOW_EXTRA_TABS': {True|False},
    }

----

Authorization Configuration
===========================

ADMINLTE2_USE_STRICT_POLICY
-------------------------------------------------

Whether routes with no defined permission should be hidden unless added to a
Whitelist

If this setting is set to False, then all routes without a defined permission
are still visible on the sidebar menu

If this setting is set to True, then all routes without a defined permission
are hidden on the sidebar menu unless the route is found in the
``ADMINLTE2_STRICT_POLICY_WHITELIST`` setting.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_STRICT_POLICY = {True|False}


ADMINLTE2_STRICT_POLICY_WHITELIST
----------------------------------------

Assuming ``ADMINLTE2_USE_STRICT_POLICY`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible, despite said routes having no defined permission.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_WHITELIST = []
