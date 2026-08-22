Authentication & Authorization Configuration
********************************************


AUTH POLICY SETTINGS
====================

These settings control the default policy state across all views.

Reminder that this is just the initial state for a view, and can be
modified/adjusted for each individual view as needed.

These adjustments can be handled through either whitelists or decorators/mixins,
depending on personal preference.


ADMINLTE2_USE_LOGIN_REQUIRED
----------------------------

Configures default view behavior, such that all routes will require users
to be logged in, in order to have access.

If set to False, then by default all routes will be accessible to all users,
regardless of authentication status.

If set to True, then all routes require login by default.

Exceptions can be made on a per-view basis, using either the project
``ADMINLTE2_LOGIN_EXEMPT_WHITELIST`` whitelist setting,
or through view :doc:`decorators<../authorization/function_views>`
/ :doc:`mixins<../authorization/class_views>`.

.. note::

    Due to how the sidebar menu is handled, this has a side-effect of automatically
    hiding sidebar menu links which the user does not have permission to access.

    If a user seems to be missing links in the sidebar menu, double check
    authentication first.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_LOGIN_REQUIRED = {True|False}


ADMINLTE2_USE_STRICT_POLICY
---------------------------

Configures default view behavior, such that all routes will require specific
user permissions, in order to have access.

By extension, this also means that routes with no defined permission will be
hidden/inaccessible unless added to a Whitelist.

If set to False, then logic will fall back to either ``Loose`` or
``Login-Required`` auth policies (whichever is selected), and all routes
without a defined permission will still be visible on the sidebar menu.

If this setting is set to True, then all routes will require permissions
to access.

Exceptions can be made on a per-view basis, using either the project
``ADMINLTE2_STRICT_POLICY_WHITELIST`` whitelist setting,
or through view :doc:`decorators<../authorization/function_views>`
/ :doc:`mixins<../authorization/class_views>`.

.. note::

    Due to how the sidebar menu is handled, this has a side-effect of automatically
    hiding sidebar menu links which the user does not have permission to access.

    If a user seems to be missing links in the sidebar menu, double check
    authentication first.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_STRICT_POLICY = {True|False}

----


WHITELIST SETTINGS
==================

Project whitelists are one of two ways to change default policy behavior of
specific routes.

The other method is through view :doc:`decorators<../authorization/function_views>`
/ :doc:`mixins<../authorization/class_views>`.


ADMINLTE2_LOGIN_EXEMPT_WHITELIST
--------------------------------

Only applicable if ``ADMINLTE2_USE_LOGIN_REQUIRED`` or
``ADMINLTE2_USE_STRICT_POLICY`` is set to True.

This is the list of routes that will always be accessible to users, even
when not logged in.

By extension, these routes will also always be shown on the sidebar menu and
accessible.

.. note::

    Even though the default value for this list is an empty list,
    the underlying functionality that this setting is used in has some included
    routes.
    They can be seen in the :ref:`authorization/policies:login required`
    Documentation.
    The routes defined in this setting will be appended to that default list.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_LOGIN_EXEMPT_WHITELIST = []


ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST
--------------------------------------

Similar to above ``ADMINLTE2_LOGIN_EXEMPT_WHITELIST``.

The difference is that the above list only takes exact route values.

Meanwhile, this list acts as a "fuzzy" list, which can be given a partial
url base, and then use that to whitelist all values that stem from that base.

For example, if you have a base url of ``/public/`` and then multiple routes
that stem from that (such as ``/public/a/``, ``/public/b/``, etc),
then you can add your base url of ``/public/`` here, which will whitelist all
other routes for ``/public/a/``, ``/public/b/``, etc.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST = []


ADMINLTE2_STRICT_POLICY_WHITELIST
---------------------------------

Only applicable if ``ADMINLTE2_USE_STRICT_POLICY`` is set to True.

This is the list of routes that will be excluded from the permission requirement,
of ``Strict`` mode.

By extension, these routes do not need associated permissions defined,
and will be available to any user that is logged in.

When also listed in with the ``ADMINLTE2_LOGIN_EXEMPT_WHITELIST``, routes will
be available regardless of users being logged in.

.. note::

    Even though the default value for this list is an empty list,
    the underlying functionality that this setting is used in has some included
    routes.
    They can be seen in the :ref:`authorization/policies:strict policy`
    documentation.
    The routes defined in this setting will be appended to that default list.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_WHITELIST = []


ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST
--------------------------------------

Similar to above ``ADMINLTE2_STRICT_POLICY_WHITELIST``.

The difference is that the above list only takes exact route values.

Meanwhile, this list acts as a "fuzzy" list, which can be given a partial
url base, and then use that to whitelist all values that stem from that base.

For example, if you have a base url of ``/public/`` and then multiple routes
that stem from that (such as ``/public/a/``, ``/public/b/``, etc),
then you can add your base url of ``/public/`` here, which will whitelist all
routes for ``/public/a/``, ``/public/b/``, etc.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST = []


----


403 & 404 HANDLING SETTINGS
===========================

ADMINLTE2_REDIRECT_TO_HOME_ON_403
---------------------------------

Controls whether the package should:

 * Use provided functionality of redirecting users to the ``Home`` page on a
   403 error (behavior when set to ``True``).

 * Raise a standard Django 403 error that has to be handled manually by
   whatever means is set up in the Django project (behavior when set to ``False``).

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_REDIRECT_TO_HOME_ON_403 = {True|False}


ADMINLTE2_REDIRECT_TO_HOME_ON_404
---------------------------------

Controls whether the package should:

 * Use provided functionality of redirecting users to the ``Home`` page on a
   404 error (behavior when set to ``True``).

 * Raise a standard Django 404 error that has to be handled manually by
   whatever means is set up in the Django project (behavior when set to ``False``).

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_REDIRECT_TO_HOME_ON_404 = {True|False}


ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST
-------------------------------------------------

This takes either an exact url or url base of urls that should serve a 403
and not redirect to the home page when strict mode is enabled.
Useful for specific url patterns that will handle authentication and
authorization manually.

EX: You may create an app for apis in your project and all of them are located
at an endpoint such as ``api/``. In this case, when there is a 403, you do not want
to do the default behavior of sending a redirect to the Home page of the site.

You instead probably want to create some sort of JSON response that conveys the
problem to the user.
So, by adding ``api/`` to this list, all urls that start with ``api/``
will be handled by raising a PermissionDenied exception when a 403 occurs,
rather than redirecting to home.
Which can be manually handled by code that you write.


:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST = []


ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST
-------------------------------------------------

This takes either an exact url or url base of urls that should serve a 404
and not redirect to the home page when strict mode is enabled.
Useful for uncontrollable requests that come from a browser or an extension.

EX: When using Chrome and the
`Django Debug Toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_
is open, there will be an automatic request to your Django app for
``.well-known/appspecific/com.chrome.devtools.json``
which may not exist.

Redirecting to Home for that request seems wasteful.
So, that url base can be added to this whitelist to make sure that they serve
back a 404 instead of redirecting to Home.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST = []


ALLOW_403_404_MESSAGES_IN_PRODUCTION
------------------------------------

Sets if 403 and 404 messages are allowed to show up in production.
Enabling can be useful for debugging.

Defaults to on, to match default expected Django behavior.

However, note that technically this is a minor security risk.
By showing these messages in production, malicious third-parties
can use this to gather info on which URLs are valid.

See :ref:`authorization/security_notes:Preventing Url Sniffing` for details
on why you may want to change this behavior.


:Type: ``bool``
:Default: ``True``

Example::

    ALLOW_403_404_MESSAGES_IN_PRODUCTION = {True|False}


ALLOW_403_404_MESSAGES_IN_PRODUCTION_ONLY_WHEN_AUTHD
----------------------------------------------------

Similar to above ``ALLOW_403_404_MESSAGES_IN_PRODUCTION``, but instead
allows disabling 403/404 messages only when a user is not authenticated.

True means messages will only show if a user is authenticated.
False means messages will show for all users.

Default of False to match standard Django behavior.


:Type: ``bool``
:Default: ``False``

Example::

    ALLOW_403_404_MESSAGES_IN_PRODUCTION_ONLY_WHEN_AUTHD = {True|False}


RESPONSE_403_DEBUG_MESSAGE
--------------------------

403 message to show when experiencing a standard 403 "missing permissions"
redirect in ``development`` mode, aka project settings ``DEBUG = True``.

To skip showing this specific message type, set to a blank string.

If not in ``development`` mode, then the ``RESPONSE_403_PRODUCTION_MESSAGE``
will show instead.


:Type: ``string``
:Default: ``AdminLtePdq Warning: Attempted to access {view_type} view
            '{view_name}' which requires permissions, and user
            permission requirements were not met.
            Redirected to project home instead.``


            ``For further information, please see the docs:
            https://django-adminlte2-pdq.readthedocs.io/``

Example::

    RESPONSE_403_DEBUG_MESSAGE = ""


RESPONSE_403_PRODUCTION_MESSAGE
-------------------------------

403 message to show when experiencing a standard 403 "missing permissions"
redirect in ``production`` mode, aka project settings ``DEBUG = False``.

To skip showing this specific message type, set to a blank string.

If not in ``production`` mode, then the ``RESPONSE_403_DEBUG_MESSAGE``
will show instead.


:Type: ``string``
:Default: ``Unable to locate the requested page.
            If you believe this was an error, please contact the
            site administrator.``

Example::

    RESPONSE_403_PRODUCTION_MESSAGE = ""


RESPONSE_404_DEBUG_MESSAGE
--------------------------

404 message to show when experiencing a standard 404 "page not found"
redirect in ``development`` mode, aka project settings ``DEBUG = True``.

To skip showing this specific message type, set to a blank string.

If not in ``development`` mode, then the ``RESPONSE_404_PRODUCTION_MESSAGE``
will show instead.


:Type: ``string``
:Default: ``AdminLtePdq Warning: The page you were looking for does not exist.``

Example::

    RESPONSE_404_DEBUG_MESSAGE = ""


RESPONSE_404_PRODUCTION_MESSAGE
-------------------------------

404 message to show when experiencing a standard 404 "page not found"
redirect in ``production`` mode, aka project settings ``DEBUG = False``.

To skip showing this specific message type, set to a blank string.

If not in ``production`` mode, then the ``RESPONSE_404_DEBUG_MESSAGE``
will show instead.


:Type: ``string``
:Default: ``Unable to locate the requested page.
            If you believe this was an error, please contact the
            site administrator.``

Example::

    RESPONSE_404_PRODUCTION_MESSAGE = ""


----


NEXT URL SETTINGS
=================

The following settings affect how the "next" url redirect property is handled,
when a user accesses the login page.

For example, if a user attempts to go to a valid page of `<domain>/sales/`
and their authentication credentials need renewed, then by default, they will
be redirect to a page of `<domain>/accounts/login/?next=/sales/`.

The below values modify the behavior of the "next" portion of the URL.

See :ref:`authorization/security_notes:Preventing Url Sniffing` for details
on why you may want to change this behavior.


ADMINLTE2_USE_LOGIN_NEXT
------------------------

Enables or disables redirecting to a "next" redirect in the URL, when logging in.

Can have minor security risks when True, similar to the
`ALLOW_403_404_MESSAGES_IN_PRODUCTION` setting, as it can potentially show
malicious third-party users what pages exist in a site.

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_USE_LOGIN_NEXT = {True|False}


ADMINLTE2_LOGIN_NEXT_UNIVERSAL_URL
------------------------

Optional "Universal" URL to redirect to for the "next" property,
when a user is logging in.

If this value is left blank (default state), then the project will try to
redirect "next" to whatever page the user attempted to access, prior to login page.

If this value is populated, then that string will unconditionally be used as
the login "next" property.

:Type: ``string``
:Default: ``""``

Example::

    ADMINLTE2_LOGIN_NEXT_UNIVERSAL_URL = {True|False}
