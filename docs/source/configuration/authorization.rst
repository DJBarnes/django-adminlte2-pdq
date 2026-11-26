Authentication & Authorization Configuration
********************************************


Policy Settings
===============


ADMINLTE2_USE_LOGIN_REQUIRED
----------------------------

Whether all routes will require that users are logged in to access unless
the route is added to a Whitelist.

If this setting is set to False, then all routes will be accessible and
still visible on the sidebar menu.

If this setting is set to True, then all routes will not be accessible nor will
there be links on the sidebar menu unless the user is logged in, the route is
found in the ``ADMINLTE2_LOGIN_EXEMPT_WHITELIST`` or
``ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST`` setting, or its view uses
``allow_anonymous_access``.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_LOGIN_REQUIRED = True


ADMINLTE2_USE_STRICT_POLICY
---------------------------

Whether routes with no defined permission should be hidden unless added to a
Whitelist.

If this setting is set to False, then all routes without a defined permission
are still visible on the sidebar menu.

If this setting is set to True, then all routes without a defined permission
are hidden on the sidebar menu, and redirect logged-in users to the home page,
unless the route is found in the ``ADMINLTE2_STRICT_POLICY_WHITELIST`` or
``ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST`` setting, or its view uses
``allow_without_permissions`` or ``allow_anonymous_access``. Setting it to True
also turns on ``ADMINLTE2_USE_LOGIN_REQUIRED``.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_USE_STRICT_POLICY = True


Whitelist Settings
==================


ADMINLTE2_LOGIN_EXEMPT_WHITELIST
--------------------------------

Assuming ``ADMINLTE2_USE_LOGIN_REQUIRED`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible, despite a user not being logged in.

Setting it when ``ADMINLTE2_USE_LOGIN_REQUIRED`` and
``ADMINLTE2_USE_STRICT_POLICY`` are both False raises ``ImproperlyConfigured``.

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


ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST
--------------------------------------

Assuming ``ADMINLTE2_USE_LOGIN_REQUIRED`` is set to True, a list of path
prefixes that do not require login. Every URL whose path starts with one of
the entries is accessible without logging in, and is shown on the sidebar
menu. Use this for a whole section of a site, such as the Django Debug
Toolbar.

Setting it when ``ADMINLTE2_USE_LOGIN_REQUIRED`` and
``ADMINLTE2_USE_STRICT_POLICY`` are both False raises ``ImproperlyConfigured``.

Entries are paths, so they start with ``/``.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST = ["/__debug__/"]


ADMINLTE2_STRICT_POLICY_WHITELIST
---------------------------------

Assuming ``ADMINLTE2_USE_STRICT_POLICY`` is set to True,
this is the list of routes that will be shown on the sidebar menu and
accessible, despite said routes having no defined permission.

Setting it when ``ADMINLTE2_USE_STRICT_POLICY`` is False raises
``ImproperlyConfigured``.

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


ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST
---------------------------------------

Assuming ``ADMINLTE2_USE_STRICT_POLICY`` is set to True, a list of path
prefixes that do not require permissions. Every URL whose path starts with one
of the entries is accessible, and shown on the sidebar menu, without defined
permissions.

Setting it when ``ADMINLTE2_USE_STRICT_POLICY`` is False raises
``ImproperlyConfigured``.

Entries are paths, so they start with ``/``.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST = ["/__debug__/"]


Login Redirect Settings
=======================


ADMINLTE2_USE_LOGIN_NEXT
------------------------

Whether redirects to the login page pass the requested URL, with its query
string, as ``next``. After logging in, Django's ``LoginView`` sends the user to
``next`` if it is on the same site, and to ``LOGIN_REDIRECT_URL`` otherwise.

When False, no redirect from this package's middleware, decorators, or
mixins adds ``next``, even for a decorator or mixin with a
``redirect_field_name``, so every login goes to ``LOGIN_REDIRECT_URL`` and
requested URLs don't appear in the login page's URL. The permission
decorators' redirects to the home page leave out ``next`` too. The login page
still follows a ``next`` that is already in its URL, such as in a link someone
shares; Django only follows it to pages on the same site. See
:ref:`authorization/security:login redirects`.

Django's own decorators and mixins, such as ``user_passes_test`` and
``UserPassesTestMixin``, don't read this setting and still add ``next``. To
leave it out of their redirects too, pass ``redirect_field_name=None`` to the
decorator, or set ``redirect_field_name = None`` on the view class.

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_USE_LOGIN_NEXT = False


403 and 404 Handling Settings
=============================


ADMINLTE2_REDIRECT_TO_HOME_ON_404
---------------------------------

Whether an unknown URL redirects to the home page with a message, instead of
Django's 404 response. See :ref:`authorization/policies:Handling 404 Errors`.

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_REDIRECT_TO_HOME_ON_404 = False


ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST
-------------------------------------------------

A list of path prefixes that always get Django's 404 response instead of the
redirect to the home page. Static files, media files, websocket paths, and the
favicon already get Django's 404 response.

Entries are paths, so they start with ``/``.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST = [
        "/.well-known/appspecific/com.chrome.devtools.json",
    ]


ADMINLTE2_REDIRECT_TO_HOME_ON_403
---------------------------------

Whether a failed permission check redirects to the home page with a message,
instead of raising ``PermissionDenied``. See
:ref:`authorization/policies:Handling 403 Errors`.

For views with the ``permission_required`` or ``permission_required_one``
decorator, pass ``raise_exception=True`` to the decorator to get the 403;
otherwise it redirects to the home page (its ``login_url`` default).

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_REDIRECT_TO_HOME_ON_403 = False


ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST
-------------------------------------------------

A list of path prefixes where a failed permission check raises
``PermissionDenied`` instead of redirecting to the home page. Use this for
sections that handle permissions themselves, such as an API that returns
JSON errors.

For views with the ``permission_required`` or ``permission_required_one``
decorator, pass ``raise_exception=True`` to the decorator to get the 403;
otherwise it redirects to the home page (its ``login_url`` default).

Entries are paths, so they start with ``/``.

:Type: ``list``
:Default: ``[]``

Example::

    ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST = ["/api/"]


ADMINLTE2_RESPONSE_404_DEBUG_MESSAGE
------------------------------------

The message shown after redirecting from an unknown URL, when ``DEBUG`` is
True. It is also written to the log. Set it to an empty string to show no
message.

:Type: ``string``
:Default: ``"AdminLtePdq Warning: The page you were looking for does not
    exist."``

Example::

    ADMINLTE2_RESPONSE_404_DEBUG_MESSAGE = "Page not found."


ADMINLTE2_RESPONSE_404_PRODUCTION_MESSAGE
-----------------------------------------

The message shown after redirecting from an unknown URL, when ``DEBUG`` is
False. Set it to an empty string to show no message.

Under the login-required and strict policies, anonymous users are sent to the
login page for unknown URLs and don't see the message.

:Type: ``string``
:Default: ``"Unable to locate the requested page. If you believe this was an
    error, please contact the site administrator."``

Example::

    ADMINLTE2_RESPONSE_404_PRODUCTION_MESSAGE = ""


ADMINLTE2_RESPONSE_403_DEBUG_MESSAGE
------------------------------------

The message shown after a failed permission check, when ``DEBUG`` is True. It
can include ``{view_type}`` and ``{view_name}``, which are replaced with the
view's type (function-based or class-based) and name. Set it to an empty string
to show no message.

:Type: ``string``
:Default: a warning that names the view and links to this documentation

Example::

    ADMINLTE2_RESPONSE_403_DEBUG_MESSAGE = "Missing permissions for {view_name}."


ADMINLTE2_RESPONSE_403_PRODUCTION_MESSAGE
-----------------------------------------

The message shown after a failed permission check, when ``DEBUG`` is False.
Set it to an empty string to show no message. The default is the same as the
404 message, so users can't tell a page they lack permission for from a page
that does not exist.

:Type: ``string``
:Default: ``"Unable to locate the requested page. If you believe this was an
    error, please contact the site administrator."``

Example::

    ADMINLTE2_RESPONSE_403_PRODUCTION_MESSAGE = ""
