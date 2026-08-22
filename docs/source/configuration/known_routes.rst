Known Routes Configuration
**************************

This page defines commonly define "known routes" that are PDQ package settings.
This includes routes such as the "Home" view, login pages, password reset
pages, etc.

These routes are included as package settings for several reasons, such as to
auto-include some of them in whitelists. Because it makes no sense to have
a login page that is behind a login-required check to access!


ADMINLTE2_HOME_ROUTE
--------------------

Set the "Home" route for your project. This tells the package where to redirect
users when they click a link that is designed to take the user home.


:Type: ``string``
:Default: ``adminlte2_pdq:home``

Example::

    ADMINLTE2_HOME_ROUTE = 'adminlte2_pdq:home'


LOGIN_URL
---------

Set the "login page" route for your project.


:Type: ``string``
:Default: ``reverse_lazy("login")``

Example::

    LOGIN_URL = 'reverse_lazy("login")'


LOGOUT_URL
---------

Set the "logout page" route for your project.


:Type: ``string``
:Default: ``reverse_lazy("logout")``

Example::

    LOGOUT_URL = 'reverse_lazy("logout")'


PWD_RESET_ROUTE
---------------

Set the base "password reset page" route for your project.


:Type: ``string``
:Default: ``password_reset``

Example::

    PWD_RESET_ROUTE = 'password_reset'


PWD_RESET_DONE_ROUTE
--------------------

Set the "password reset done" route for your project.


:Type: ``string``
:Default: ``password_reset_done``

Example::

    PWD_RESET_DONE_ROUTE = 'password_reset_done'


PWD_RESET_CONFIRM_ROUTE
-----------------------

Set the "confirm password reset" route for your project.


:Type: ``string``
:Default: ``password_reset_confirm``

Example::

    PWD_RESET_CONFIRM_ROUTE = 'password_reset_confirm'


PWD_RESET_COMPLETE_ROUTE
------------------------

Set the "password reset complete" route for your project.


:Type: ``string``
:Default: ``password_reset_complete``

Example::

    PWD_RESET_COMPLETE_ROUTE = 'password_reset_complete'

PWD_CHANGE
---------

Set the "change password" route for your project.


:Type: ``string``
:Default: ``password_change``

Example::

    ADMINLTE2_HOME_ROUTE = 'password_change'


PWD_CHANGE_DONE
---------------

Set the "done changing password" route for your project.


:Type: ``string``
:Default: ``password_change_done``

Example::

    ADMINLTE2_HOME_ROUTE = 'password_change_done'


REGISTER_ROUTE
--------------

Set the "user registration" route for your project.


:Type: ``string``
:Default: ``adminlte2_pdq:register``

Example::

    ADMINLTE2_HOME_ROUTE = 'adminlte2_pdq:register'


MEDIA_ROUTE
---------

Set the "media files" route for your project.


:Type: ``string``
:Default: ``/media/``

Example::

    ADMINLTE2_HOME_ROUTE = '/media/'


STATIC_ROUTE
------------

Set the "static files" route for your project.


:Type: ``string``
:Default: ``/static/``

Example::

    ADMINLTE2_HOME_ROUTE = '/static/'


WEBSOCKET_ROUTE
---------------

Set the "websocket" route for your project.


:Type: ``string``
:Default: ``/ws/``

Example::

    ADMINLTE2_HOME_ROUTE = '/ws/'
