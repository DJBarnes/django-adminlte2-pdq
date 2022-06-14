Authorization Configuration
***************************


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

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_WHITELIST = []
