Known Routes Configuration
**************************

The package needs to know the routes of some pages: the pages that must work
without logging in (login, logout, password reset, registration), the pages
that must work without permissions (home, password change), and the URL
prefixes of files that are not views (static, media, websockets). These pages
are added to the login exempt and strict policy whitelists automatically (see
:doc:`authorization`).

The defaults match Django's ``django.contrib.auth.urls`` and this package's
URLs. Change them only if your project uses different routes.

Most of these settings take a URL name, such as ``"password_reset"`` or
``"myapp:register"``. The settings that take a URL path say so.

.. note::

    ``LOGIN_URL``, ``MEDIA_URL``, and ``STATIC_URL`` are Django's own settings.
    The other settings on this page belong to this package and use the
    ``ADMINLTE2_`` prefix. Their old names without the prefix still work, with
    a deprecation warning, and will be removed in a future release:

    =============================  ==========================================
    Old name                       New name
    =============================  ==========================================
    ``LOGOUT_URL``                 ``ADMINLTE2_LOGOUT_URL``
    ``PWD_RESET_ROUTE``            ``ADMINLTE2_PASSWORD_RESET_ROUTE``
    ``PWD_RESET_DONE_ROUTE``       ``ADMINLTE2_PASSWORD_RESET_DONE_ROUTE``
    ``PWD_RESET_CONFIRM_ROUTE``    ``ADMINLTE2_PASSWORD_RESET_CONFIRM_ROUTE``
    ``PWD_RESET_COMPLETE_ROUTE``   ``ADMINLTE2_PASSWORD_RESET_COMPLETE_ROUTE``
    ``REGISTER_ROUTE``             ``ADMINLTE2_REGISTER_ROUTE``
    ``PWD_CHANGE``                 ``ADMINLTE2_PASSWORD_CHANGE_ROUTE``
    ``PWD_CHANGE_DONE``            ``ADMINLTE2_PASSWORD_CHANGE_DONE_ROUTE``
    ``WEBSOCKET_URL``              ``ADMINLTE2_WEBSOCKET_URL``
    =============================  ==========================================

The home route is set by :ref:`configuration/home:ADMINLTE2_HOME_ROUTE`.


Routes That Don't Require Login
===============================

LOGIN_URL
---------

Django's own setting. The package redirects users who need to log in to this
URL, and does not require login for it.

:Type: ``string`` (a URL path or a URL name)
:Default: Django's default, ``"/accounts/login/"``

Example::

    LOGIN_URL = "login"


ADMINLTE2_LOGOUT_URL
--------------------

The logout page. It does not require login. Django has no logout URL
setting, so this one belongs to the package.

:Type: ``string`` (a URL path or a URL name)
:Default: the URL of the ``logout`` route

Example::

    ADMINLTE2_LOGOUT_URL = "/accounts/logout/"


ADMINLTE2_PASSWORD_RESET_ROUTE
------------------------------

The page where users request a password reset.

:Type: ``string`` (URL name)
:Default: ``"password_reset"``

Example::

    ADMINLTE2_PASSWORD_RESET_ROUTE = "accounts:password_reset"


ADMINLTE2_PASSWORD_RESET_DONE_ROUTE
-----------------------------------

The page shown after a password reset is requested.

:Type: ``string`` (URL name)
:Default: ``"password_reset_done"``

Example::

    ADMINLTE2_PASSWORD_RESET_DONE_ROUTE = "accounts:password_reset_done"


ADMINLTE2_PASSWORD_RESET_CONFIRM_ROUTE
--------------------------------------

The page where users set a new password from the reset link.

:Type: ``string`` (URL name)
:Default: ``"password_reset_confirm"``

Example::

    ADMINLTE2_PASSWORD_RESET_CONFIRM_ROUTE = "accounts:password_reset_confirm"


ADMINLTE2_PASSWORD_RESET_COMPLETE_ROUTE
---------------------------------------

The page shown after the new password is set.

:Type: ``string`` (URL name)
:Default: ``"password_reset_complete"``

Example::

    ADMINLTE2_PASSWORD_RESET_COMPLETE_ROUTE = "accounts:password_reset_complete"


ADMINLTE2_REGISTER_ROUTE
------------------------

The user registration page.

:Type: ``string`` (URL name)
:Default: ``"adminlte2_pdq:register"``

Example::

    ADMINLTE2_REGISTER_ROUTE = "accounts:register"


Routes That Don't Require Permissions
=====================================

These pages require login, but no permissions, under the strict policy.

ADMINLTE2_PASSWORD_CHANGE_ROUTE
-------------------------------

The page where logged-in users change their password.

:Type: ``string`` (URL name)
:Default: ``"password_change"``

Example::

    ADMINLTE2_PASSWORD_CHANGE_ROUTE = "accounts:password_change"


ADMINLTE2_PASSWORD_CHANGE_DONE_ROUTE
------------------------------------

The page shown after the password is changed.

:Type: ``string`` (URL name)
:Default: ``"password_change_done"``

Example::

    ADMINLTE2_PASSWORD_CHANGE_DONE_ROUTE = "accounts:password_change_done"


File and Websocket Routes
=========================

The middleware does not check login or permissions for paths that start with
these prefixes, and a missing file returns Django's 404 response instead of
redirecting to the home page.

MEDIA_URL and STATIC_URL
------------------------

Django's own settings. The package reads them as they are.


ADMINLTE2_WEBSOCKET_URL
-----------------------

The path prefix of the project's websocket routes.

:Type: ``string`` (URL path)
:Default: ``"/ws/"``

Example::

    ADMINLTE2_WEBSOCKET_URL = "/websockets/"
