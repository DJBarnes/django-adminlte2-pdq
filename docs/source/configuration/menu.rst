Menu Configuration
******************


ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES
=========================================

By default, the main navigation (non-admin) menu is not part of the sidebar when
the user is viewing a
`Django Admin page <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_.
If you would like users to be able to see all of the main nav links regardless
of what page they are on, set this value to ``True``.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES = {True|False}


ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES
=========================================

By default, the admin navigation menu is not part of the sidebar when the user
is viewing a main navigation
(non-`Django-Admin <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_)
page. If you would like users to be able to see all of the admin nav links
regardless of what page they are on, set this value to ``True``.

.. note::

    Only staff users and superusers see the admin section. Staff users see
    only the models they have a permission for.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES = {True|False}


ADMINLTE2_USE_MENU_GROUP_SEPARATOR
==================================

By default, there will be an implicit separator bar rendered between each menu
group.
These groups are, in order: **MENU_FIRST**, **MENU**, the **Admin Menu**, and
**MENU_LAST**.
More information about these groups can be found on the
:doc:`../menu/advanced` page. If you would like to disable this
separator from being automatically rendered, set this value to ``False``.


:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_USE_MENU_GROUP_SEPARATOR = {True|False}


ADMINLTE2_MENU
==============

This setting is the definition for the main navigation menu.
There are a lot of options when creating this menu.
See the :doc:`../menu/general_information` and :doc:`../menu/building_blocks`
sections for a detailed explanation of how to create this menu and all of the
available options that can be used.

:Type: ``list``
:Default: the package's demo menu (``adminlte2_pdq.menu.MENU``) when its routes
    are registered, which they are when the project includes
    ``adminlte2_pdq.urls``. Otherwise ``[]``.

Example::

    ADMINLTE2_MENU = []
