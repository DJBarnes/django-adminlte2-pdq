Authentication & Authorization Configuration
********************************************


ADMINLTE2_USE_LOGIN_REQUIRED
============================

Whether all routes will require that users are logged in to access unless
the route is added to a Whitelist.

If this setting is set to False, then all routes will be accessible and
still visible on the sidebar menu.

If this setting is set to True, then all routes will not be accessible nor will
there be links on the sidebar menu unless the user is logged in or the route is
found in the
``ADMINLTE2_LOGIN_EXEMPT_WHITELIST`` setting.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_LOGIN_REQUIRED = {True|False}


ADMINLTE2_LOGIN_EXEMPT_WHITELIST
================================

Assuming ``ADMINLTE2_USE_LOGIN_REQUIRED`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible, despite a user not being logged in.

.. note::

    Even though the default value for this list is an empty list,
    the underlying functionality that this setting is used in has some included
    routes. They can be seen in the
    :ref:`authorization/policies:login required`
    Documentation. The routes defined in this setting will be appended to that
    default list.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_LOGIN_EXEMPT_WHITELIST = []


ADMINLTE2_USE_STRICT_POLICY
===========================

Whether routes with no defined permission should be hidden unless added to a
Whitelist.

If this setting is set to False, then all routes without a defined permission
are still visible on the sidebar menu.

If this setting is set to True, then all routes without a defined permission
are hidden on the sidebar menu unless the route is found in the
``ADMINLTE2_STRICT_POLICY_WHITELIST`` setting.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_STRICT_POLICY = {True|False}


ADMINLTE2_STRICT_POLICY_WHITELIST
=================================

Assuming ``ADMINLTE2_USE_STRICT_POLICY`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible, despite said routes having no defined permission.

.. note::

    Even though the default value for this list is an empty list,
    the underlying functionality that this setting is used in has some included
    routes. They can be seen in the
    :ref:`authorization/policies:strict policy`
    Documentation. The routes defined in this setting will be appended to that
    default list.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_WHITELIST = []
