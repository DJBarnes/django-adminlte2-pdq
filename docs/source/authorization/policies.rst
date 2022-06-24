Authentication and Authorization Policy
***************************************

The **Django-AdminLTE-2** package comes with built-in functionality to make it
easy to customize and manage various user authentication and authorization
policies and scenarios.


.. note::

    This functionality heavily based on the
    `standard Django practices <https://docs.djangoproject.com/en/dev/topics/auth/default/>`_
    to manage view access and user permissions. We recommend reviewing that
    information before reading this section.

.. important::

    Django-AdminLTE-2 provides a middleware that is required for some of the
    available authentication and authorization scenarios from this package to
    function.

    If you haven't already done so, add this middleware to your middleware list
    in ``settings.py`` so that you can use the full potential of this package.

Setting up authentication for the package requires choosing whether or not you
would like to require that users be logged in to gain access to the majority of
views in your site or if anonymous users are able to see the same things that
logged in users can. If you would like to require that users are logged in to
visit the majority of your site, see the
:ref:`authorization/policies:login required`
section for more information on how to enable that.

Setting up authorization for the sidebar menu and its associated links requires
:ref:`authorization/policies:choosing a policy` and then properly using
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins` provided by this package to set
permissions on various views.

Setting the permissions on the view has the added benefit of not only preventing
users from accessing a view, but also automatically hiding links on the sidebar
menu from the users that do not have access.


Login Required
==============

If you would like to prevent users from accessing the majority of views in your
project unless they are signed in, you can require that people are logged in by
setting the ``ADMINLTE2_USE_LOGIN_REQUIRED`` setting in your ``settings.py``
file to ``True``.

When enabled, the included middleware will redirect all requests made by an
anonymous user to the login page unless the url that they are trying to access
is explicitly listed in a whitelist.
The default whitelist contains the following standard anonymous routes:

* login - As defined via the ``LOGIN_URL`` setting in ``settings.py``
* logout
* password_reset
* password_reset_done
* password_reset_confirm
* password_reset_complete

If you would like to add additional routes to this list, you can do so by
adding either the route name or url to the ``ADMINLTE2_LOGIN_EXEMPT_WHITELIST``
setting in your ``settings.py`` file.

.. code:: python

    ADMINLTE2_LOGIN_EXEMPT_WHITELIST = [
        'two_factor_confirm',
    ]

.. tip::

    If the majority of your routes do not require being logged in and you only
    have a handful that do, it is better to leave the
    ``ADMINLTE2_USE_LOGIN_REQUIRED`` undefined or set to ``False`` and instead
    use the
    :ref:`authorization/function_views:login required decorator` or
    :ref:`authorization/class_views:login required mixin` on the specific
    views that require login.

Choosing a Policy
=================

The first step in using and configuring authorization for views and sidebar
menu links is to determine what general policy you want to adhere to.
Your choices are:

1. :ref:`authorization/policies:Loose Policy` - By default all sidebar links and
   associated views are visible and accessible to the user.

   * Majority of sidebar links and associated views are visible to all users.
   * Link will still be visible and accessible if you set a permission on that
     route's view and that user has the correct permission.
   * Link will be hidden and associated views blocked if you set a permission on
     that route's view and the user does not have the correct permission.


2. :ref:`authorization/policies:Strict Policy` - By default all sidebar links
   and associated views are hidden from the user.

   * Majority of sidebar links are hidden to all users.
   * Link will become visible and accessible if you set a permission on that
     route's view and that user has the correct permission.
   * Link will become visible and accessible if you put the route in an explicit
     whitelist defined in the settings.

   .. important::

       The strictness in this policy is related to the visibility of sidebar
       menu links only.

       If no permissions are set on a corresponding view, the sidebar menu link
       is not visible, but the user can still technically gain access to the
       page assuming that they know the url and directly go to it. To
       completely block users from a route, you **Must** define
       a permission on the view or handle it with some other form of permission
       checking provided by Django.

Once you have determined what general policy you want to follow, use
the corresponding section to properly set up and configure authorization.


Loose Policy
============

This policy assumes users should be able to see and access links and views, by
default.

Refer to the :doc:`../configuration/authorization` section for information about
the specific settings in settings.py mentioned below.

1. Ensure that the ``ADMINLTE2_USE_STRICT_POLICY``
   is either not defined in ``settings.py``, or is set to ``False`` if it is
   defined.

2. If you are using function based views, read the :doc:`function_views`
   page and follow the steps in the
   :ref:`authorization/function_views:Loose Decorator Example` section to
   add view permissions that require permission to access.

3. If you are using class based views, read the :doc:`class_views` page
   and follow the steps in the
   :ref:`authorization/class_views:Loose Mixin Example` section to add
   view permissions that require permission to access.


Strict Policy
=============

This policy assumes users should have restricted access to links and views, by
default.

Refer to the :doc:`../configuration/authorization` section for information about
the specific settings in settings.py mentioned below.

1. Ensure that the ``ADMINLTE2_USE_STRICT_POLICY``
   is defined in ``settings.py`` and is set to ``True``.

2. If you are using function based views, read the :doc:`function_views`
   page and follow the steps in the
   :ref:`authorization/function_views:Strict Decorator Example` section
   to add view permissions that require permission to access.

3. If you are using class based views, read the :doc:`class_views` page
   and follow the steps in the
   :ref:`authorization/class_views:Strict Mixin Example` section to add
   view permissions that require permission to access.

4. Add any routes that do not require a specific permission and should
   be available to everyone to the ``ADMINLTE2_STRICT_POLICY_WHITELIST``
   in ``settings.py``
