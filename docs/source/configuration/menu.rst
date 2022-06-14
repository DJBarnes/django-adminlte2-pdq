Menu Configuration
******************


ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES
=========================================

By default the main navigation (non-admin) is not part of the sidebar when the
user is viewing an admin page. If you would like users to be able to see all of
the main nav links regardless of what page they are on, set this setting to
``True``.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = {True|False}


ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES
=========================================

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
==================================

By default there will be a implicit separator bar rendered between each menu
group.
These groups include: **MENU_FIRST**, **MENU**, **MENU_LAST**, and the
**Admin Menu**.
More information about these groups can be found on the
:doc:`../menu/admin` page. If you would like to disable this
separator from being automatically rendered set this setting to ``False``.


:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_USE_MENU_GROUP_SEPARATOR = {True|False}


ADMINLTE2_MENU
==============

This setting is the definition for the main navigation menu.
There are a lot of options when creating this menu.
See the :doc:`../menu/admin` section for a detailed explanation on how to
create this menu and all of the available options that can be used.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_MENU = []
