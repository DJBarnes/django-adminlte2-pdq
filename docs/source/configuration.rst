Configuration
=============

There are various configuration options that can be set via Django Settings to
control the overall look, feel, and functionality of the package.

Home
----

ADMINLTE2_HOME_ROUTE
^^^^^^^^^^^^^^^^^^^^

Set the "Home" route for you project so that the package knows
where to redirect users when they click a link that is designed
to take the user home.

:Type: ``string``
:Default: ``django_adminlte_2:home``

Example::

    ADMINLTE2_HOME_ROUTE = 'django_adminlte_2:home'


Admin
-----

ADMINLTE2_ADMIN_INDEX_USE_APP_LIST
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default Django-AdminLTE-2 will put the Apps on the Admin Index page
into AdminLTE Info Boxes. Setting this to True will change that look
to the traditional Django list view.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_ADMIN_INDEX_USE_APP_LIST = {True|False}


ADMINLTE2_INCLUDE_ADMIN_HOME_LINK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether the sidebar menu should have a link to the admin index.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_ADMIN_HOME_LINK = {True|False}


ADMINLTE2_ADMIN_MENU_IN_TREE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether the admin links in the sidebar should be in a tree

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_ADMIN_MENU_IN_TREE = {True|False}


Menu
----

ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether the sidebar main nav should be shown when on an admin page in addition
to the admin nav

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = {True|False}


ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether the sidebar admin nav should be shown when on a main page in addition
to the main nav

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES = {True|False}


ADMINLTE2_USE_MENU_GROUP_SEPARATOR
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether to put in sidebar separators between each menu group

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_MENU_GROUP_SEPARATOR = {True|False}


ADMINLTE2_MENU_FIRST
^^^^^^^^^^^^^^^^^^^^

This menu setting is useful for defining a menu that should come before the
main menu. Sometimes you may be in a subsection of your website that has
additional navigation that should precede the normal main navigation but only
be shown when in this subsection. This setting allows that without having to
change the main navigation menu. See the :doc:`menu` section for more
information.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_MENU_FIRST = []


ADMINLTE2_MENU
^^^^^^^^^^^^^^

This menu setting is the main menu that should be available no matter what
section
of the website you are in. It is the main navigation.
See the :doc:`menu` section for more information.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_MENU = []


ADMINLTE2_MENU_LAST
^^^^^^^^^^^^^^^^^^^

This menu setting is useful for defining a menu that should come after the
admin menu links. A menu footer so to speak.
See the :doc:`menu` section for more information.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_MENU_LAST = []


Authorization
-------------

ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether routes with no defined permission should be hidden unless added to a
Whitelist

If this setting is set to False, then all routes without a defined permission
are still visible on the sidebar menu

If this setting is set to True, then all routes without a defined permission
are hidden on the sidebar menu unless the route is found in the
``ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST`` setting.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS = {True|False}


ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming ``ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible
despite a defined permission.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST = []
