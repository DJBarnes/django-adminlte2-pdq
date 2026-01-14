Authentication and Authorization Policy
***************************************

The **Django-AdminLTE2-PDQ** package comes with built-in functionality to make it
easy to customize and manage various user
:ref:`authorization/policies:authentication` and
:ref:`authorization/policies:authorization`
policies and scenarios.

.. note::

    This functionality is heavily based on the
    `standard Django practices <https://docs.djangoproject.com/en/dev/topics/auth/default/>`_
    to manage view access and user permissions.
    We recommend reviewing that information before reading this section.

.. important::

    Django-AdminLTE2-PDQ provides a middleware that is required for some of the
    available authentication and authorization functionality this package
    provides.

    If you haven't already done so, reference the :ref:`quickstart:quickstart`
    to add this middleware to your middleware list in ``settings.py`` so that
    you can use the full potential of this package.


Authentication
==============

Authentication is the handling of user login, and view access when logged in
or anonymous.

Setting up authentication for the package requires choosing if your site will:

* Require users to be logged in to gain access to the majority of site views.
* Allow anonymous users to see site views by default (this is the default Django
  handling).

If you would like to require that users are logged in to
visit the majority of your site, see the
:ref:`authorization/policies:login required`
section for more information on how to enable that.

Login Required
--------------

If you would like to prevent anonymous users from accessing the majority of
the views in your site, you can require login by
setting the ``ADMINLTE2_USE_LOGIN_REQUIRED`` setting in your ``settings.py``
file to ``True``.

**settings.py**

.. code:: python

    ADMINLTE2_USE_LOGIN_REQUIRED = True

When enabled, the included middleware will redirect all requests made by an
anonymous user to the login page unless the URL that they are trying to access
is explicitly listed in a whitelist.
The default whitelist contains the following standard anonymous routes:

* login - As defined via the ``LOGIN_URL`` setting in ``settings.py``
* logout
* password_reset
* password_reset_done
* password_reset_confirm
* password_reset_complete
* media url - As defined via the ``MEDIA_URL`` setting in ``settings.py``
  so long as it is not the default value of ``''``. See note below.

If you would like to add additional routes to this list, you can do so by
adding either the route name or URL for the endpoint to the
``ADMINLTE2_LOGIN_EXEMPT_WHITELIST`` setting in your ``settings.py`` file.

**settings.py**

.. code:: python

    ADMINLTE2_LOGIN_EXEMPT_WHITELIST = [
        'two_factor_confirm',  # url_name of route to two factor confirmation
    ]

.. tip::

    If the majority of your routes do not require being logged in and you only
    have a handful of routes that do, it is better to leave the
    ``ADMINLTE2_USE_LOGIN_REQUIRED`` undefined or set to ``False`` and instead
    use the
    :ref:`authorization/function_views:login required decorator` or
    :ref:`authorization/class_views:login required mixin` on the specific
    views that do require being logged in.

.. note::

    The ``MEDIA_URL`` is exempt from the login required processing so long as
    it has a value other than the default.

    By default, the ``MEDIA_URL`` setting is set to ``''``, the blank string.
    This automatically gets converted to the root URL ``'/'`` to ensure that
    it is a valid URL and that there will be no issues when running your app.

    If you leave the ``MEDIA_URL`` setting as the default and then try to
    serve media files from that location with the login required turned on,
    those files will not be able to be served to anonymous users.


Authorization
=============

Authorization is the handling of user view access, based on the permissions
and groups of a given logged in user.

Setting up authorization for the package requires
:ref:`authorization/policies:choosing a policy` and then properly using
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins`
provided by this package to set permissions on various views.

Setting the permissions on the view with the
:ref:`authorization/function_views:Decorators` and
:ref:`authorization/class_views:Mixins`
provided by this package will prevent a user from accessing a view that
they do not have permission to. Just like the ones provided by
`Django <https://docs.djangoproject.com/en/dev/topics/auth/default/#limiting-access-to-logged-in-users>`_.
But they will additionally dynamically show/hide any menu sidebar links for the
protected view, in the, provided AdminLTE menus.

.. note::

    Within this documentation and in the context of
    :ref:`authorization/policies:choosing a policy` the
    :ref:`authorization/function_views:login required decorator` and
    :ref:`authorization/class_views:login required mixin` are included.
    Although these are not typically considered part of authorization they have
    been included in these sections because they will also handle showing and
    hiding a sidebar link depending on whether or not the user meets the
    criteria of being logged in.

Choosing a Policy
-----------------

The first step in using and configuring authorization for views and sidebar
menu links are to determine what general policy you want to adhere to.
Regardless of whether you have the global
:ref:`authorization/policies:login required`
turned on or off, knowing what type of policy you want to achieve is critical.

Your choices are:

1.  :ref:`authorization/policies:Loose Policy` - Has the following
    characteristics:

    * Majority of sidebar links and associated views are visible to all users.
    * Sidebar links and associated views will still be visible and accessible
      if you set required permissions or the login required criteria on that
      route's view and that user meets the required criteria to access that
      view.
    * Sidebar links and associated views will be hidden / blocked if you set a
      required permission or the login required criteria on that route's view
      and the user does not meet the required criteria to access that view.

    .. warning::

        If you have the global :ref:`authorization/policies:login required`
        setting turned off and you opt for the
        :ref:`authorization/policies:Loose Policy`
        you  will be allowing all users, both logged in and anonymous, access
        to every view on your site that does not have a required permission
        or the login required criteria defined on the view.


2.  :ref:`authorization/policies:Strict Policy` - Has the following
    characteristics:

    * Majority of sidebar links and associated views are hidden to all users.
    * Sidebar links and associated views will become visible and accessible if
      you set required permissions or the login required criteria on a route's
      view and the user meets the required criteria.
    * Sidebar links and associated views will become visible and accessible if
      you put the route in an explicit whitelist defined in the settings.

    .. note::

        With the :ref:`authorization/policies:Strict Policy`, if you forget to
        add permissions to a view, the view will be inaccessible to everyone
        except for superusers.
        This is a good way to ensure that you don't accidentally create
        features that everyone automatically has access to.
        You have to explicitly think about what permissions are required for
        each feature, set them on the view, and then assign the permissions to
        the users that need them before anyone can gain access to it.

Once you have determined what general policy you want to follow, use
the corresponding section to properly set up and configure authorization.


Loose Policy
------------

This policy assumes users should be able to see and access all links and views,
by default.

When enabled, all views that do not use one of the included
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins` will be accessible to everyone.
Additionally, if the sidebar menu contains an entry for the view, the link to
that view will be visible to everyone.

Views will only be hidden if one of the
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins`
are used and the user does not meet the required criteria.
This will both prevent the user from being able to go directly to the view as
well as hide any sidebar link that links to that view.

Refer to the :doc:`../configuration/authorization` section for information about
the specific settings in ``settings.py`` mentioned below.

1.  Ensure that the ``ADMINLTE2_USE_STRICT_POLICY``
    is either not defined in ``settings.py``, or is set to ``False`` if it is
    defined.

    **settings.py**

    .. code:: python

        ADMINLTE2_USE_STRICT_POLICY = False

2.  If you are using function based views, read the :doc:`function_views`
    page and follow the steps in the
    :ref:`authorization/function_views:Loose Decorator Example` section to
    add view permissions that require permission to access.

3.  If you are using class based views, read the :doc:`class_views` page
    and follow the steps in the
    :ref:`authorization/class_views:Loose Mixin Example` section to add
    view permissions that require permission to access.


Strict Policy
-------------

This policy assumes users should have restricted access to links and views, by
default.

When enabled, all views that do not use one of the included
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins` will redirect all requests to the
:ref:`configuration/home:adminlte2_home_route` unless the route or url that
they are trying to access is explicitly listed in a whitelist.
The default whitelist contains the following standard anonymous routes as well
as the password change, :ref:`configuration/home:adminlte2_home_route`, media
routes, and websocket routes:

* login - As defined via the ``LOGIN_URL`` setting in ``settings.py``
* logout
* password_reset
* password_reset_done
* password_reset_confirm
* password_reset_complete
* password_change
* password_change_done
* home - As defined via the ``ADMINLTE2_HOME_ROUTE`` setting in ``settings.py``
* media url - As defined via the ``MEDIA_URL`` setting in ``settings.py``
  so long as it is not the default value of ``''``. See note below.
* websocket url - As defined via the ``WEBSOCKET_URL`` setting in
  ``settings.py``. Defaults to ``/ws/``.

.. important::

    The Home route is included in the whitelist because we believe that there
    should be at least one view that a logged in user can access after logging
    in.
    Even if they do not have any required permissions to see anything else on the site.
    The alternative would be to send them to the login page after a successful
    login, which we believe, even with messages, would be confusing to the
    user.

.. note::

    The ``MEDIA_URL`` is exempt from the login required
    processing so long as it has a value other than the default.

    By default, the ``MEDIA_URL`` setting is set to ``''``, the blank string.
    This automatically gets converted to the root URL ``'/'`` to ensure that
    it is a valid URL and that there will be no issues when running your app.

    If you leave the ``MEDIA_URL`` setting as the default and then try to
    serve media files from that location with the login required turned on,
    those files will not be able to be served to anonymous users.

Additionally, if a view does have required permissions or login required
criteria defined on the view, and the user does not meet that criteria, they
will be redirected to the
:ref:`configuration/home:adminlte2_home_route`
route.



Refer to the :doc:`../configuration/authorization` section for information about
the specific settings in settings.py mentioned below.

1.  Ensure that the ``ADMINLTE2_USE_STRICT_POLICY``
    is defined in ``settings.py`` and is set to ``True``.

    **settings.py**

    .. code:: python

        ADMINLTE2_USE_STRICT_POLICY = True

2.  If you are using function based views, read the :doc:`function_views`
    page and follow the steps in the
    :ref:`authorization/function_views:Strict Decorator Example` section
    to add view permissions that require permission to access.

3.  If you are using class based views, read the :doc:`class_views` page
    and follow the steps in the
    :ref:`authorization/class_views:Strict Mixin Example` section to add
    view permissions that require permission to access.

4.  Add any routes that do not require specific permissions and should
    be available to everyone to the ``ADMINLTE2_STRICT_POLICY_WHITELIST``
    in ``settings.py``

    **settings.py**

    .. code:: python

        ADMINLTE2_STRICT_POLICY_WHITELIST = [
            'tutorial'  # url_name of the route to the tutorial view.
        ]

Handling 404s and 403s
**********************

This section explains how the package handles 404 and 403 errors by default.
Additionally, it shows what options are available if you would like to do
something different than the default package behavior.

Handling 404 Errors
===================

404s have a built-in handling behavior. This can be disabled if you
do not want to use it, which will then just use the default Django handling.

Handling 404s with the Built-In Behavior
----------------------------------------

This package comes with built-in behavior to handle 404s, which is on by default
The built-in functionality is to add a warning message via the
`Django messages framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_
indicating that the page does not exist. It will additionally add a debug
message and log entry with specifics about what caused the 404 exception.
It then redirects to the
:ref:`configuration/home:adminlte2_home_route`
where the user can see those messages.

.. note::

    The actual exception specifics are only rendered in a Debug message.
    This means that developers who have their message level set to include
    debug messages can see it, but in production where debug messages should
    not be shown, it will be not rendered.

The package does have some exceptions to the above handling of 404s.
If the requested url is part of the **static files**, the **media files**,
a **favicon**, or part of a **special list** in the settings,
it will do the default Django 404 action by just raising a ``Http404`` error
and allowing Django to handle it.

The special setting that allows you to just raise a ``Http404`` error
is called ``ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST``.
This setting can be added to ``settings.py`` and must contain a list of
"starts with" patterns that should always be treated as actual 404s vs redirects
to the home page. This is good for requests that might come directly from a
browser via extensions or developer tools and are out of the developers control.
Using this setting will prevent the server from sending back the entire
home page for what should actually be a basic 404 response.

**settings.py**

    .. code:: python

        ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST = [
            "/.well-known/appspecific/com.chrome.devtools.json",
        ]


Handling 404s Manually
----------------------

If you do not want to use the built-in handling for 404 errors and would like
full control over how to handle them, you should disable the built-in behavior
with the following setting:

**settings.py**

    .. code:: python

        ADMINLTE2_REDIRECT_TO_HOME_ON_404 = False


Handling 403 Errors
===================

403s also have a built-in handling behavior. This can also be disabled if you
do not want to use it, which will then just use the default Django handling.

Handling 403s with the Built-In Behavior
----------------------------------------

To better understand how the built-in 403 handling works, we need
to clarify some things. Permission Denied (403) can be raised primarily in one
of two ways.

1.  You are using the :ref:`authorization/policies:strict policy`
    and you have not defined any permissions on a view that a user is
    trying to access.

2.  Regardless of the :ref:`authorization/policies:strict policy`,
    you have defined some required permissions on a view
    and the user does not meet the required criteria.

When this happens, we believe that it is good to do something different than
the default behavior that Django provides of just returning a 403 error.
We believe that it may be better to handle it as if it were a 404 so
that users are unaware that the location they are trying to access has an
actual endpoint that they do not have permission to access. It will make it
harder for bad actors to phish for endpoints that they should not know exist.

Just like the built-in functionality for 404s,
this package comes with built-in behavior to handle 403s, which is also on by
default. The built-in functionality is to also add a warning message via the
`Django messages framework <https://docs.djangoproject.com/en/dev/ref/contrib/messages/>`_
indicating that the page does not exist. It will additionally add a debug
message and log entry with specifics about what caused the 403 exception.
It then redirects to the
:ref:`configuration/home:adminlte2_home_route`
where the user can see those messages.

For 403s, there is another special setting that allows you to just raise a
``PermissionDenied`` error instead of having the package handle it. The setting
is called ``ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST``.
This setting can be added to ``settings.py`` and must contain a list of
"starts with" patterns that should always be treated as actual 403s vs redirects
to the home page.

This is good for sections of the project that may handle auth
differently. A good example would be APIs. You might have an app where all
endpoints are located at ``api/`` and instead of having 403s redirect to the
home page, you want to manually control what happens and send them back a
JSON response that explains the situation in JSON format. Adding ``api/`` to this
setting will then make it so that all urls that start with ``api/`` will skip
the built-in 403 handling.

**settings.py**

    .. code:: python

        ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST = [
            "api/",
        ]

Handling 403s Manually
----------------------

If you do not want to use the built-in handling for 403 errors and would like
full control over how to handle them, you should disable the built-in behavior
with the following setting:

**settings.py**

    .. code:: python

        ADMINLTE2_REDIRECT_TO_HOME_ON_403 = False


Customizing the built-in 404 and 403 messages
---------------------------------------------

If you would like to customize the messages that are shown to the user
when using the built-in 404 or 403 handling,
you can set the following settings in ``settings.py``.
This will also allow you to use different messages for 403 errors in the event
that you do not want it to operate the same as 404 errors.

**settings.py**

    .. code:: python

        ADMINLTE2_RESPONSE_404_DEBUG_MESSAGE = "Nothing to see here!"

        ADMINLTE2_RESPONSE_404_PRODUCTION_MESSAGE = "Nothing to see here!"

        ADMINLTE2_RESPONSE_403_DEBUG_MESSAGE = "You lack the power!"

        ADMINLTE2_RESPONSE_403_PRODUCTION_MESSAGE = "You lack the power!"

