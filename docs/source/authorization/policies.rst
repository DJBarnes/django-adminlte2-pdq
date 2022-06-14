Access Policy
*************

The **Django-AdminLTE-2** package comes with built-in functionality to make it
easy to customize and manage user access and authorization policy.


.. note::

    This functionality mostly applies to the provided menu navigation elements.
    To properly manage user access, we recommend still using
    `standard Django practices <https://docs.djangoproject.com/en/dev/topics/auth/default/>`_
    to manage view access and user permissions.


Setting up authorization for the sidebar menu and its associated links requires
choosing a policy (see below), and then properly using
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins` provided by this package to set
permissions on various views.

Setting the permissions on the view has the added benefit of not only preventing
users from accessing a view, but also automatically hiding links on the sidebar
menu from the users that do not have access.


Choosing a Policy
=================

The first step in using and configuring authorization for views and sidebar
menu links is to determine what general policy you want to adhere to.
Your choices are:

1. :ref:`authorization/policies:Loose Policy` - By default all sidebar links are
   visible and accessible to the user.

   * Majority of sidebar links are visible to all users.
   * Link will still be visible if you set a permission on that route's view
     and that user has the correct permission.
   * Link will be hidden if you set a permission on that route's view and the
     user does not have the correct permission.


2. :ref:`authorization/policies:Strict Policy` - By default all sidebar links
   are hidden from the user.

   * Majority of sidebar links are hidden to all users.
   * Link will become visible if you set a permission on that route's view
     and that user has the correct permission.
   * Link will become visible if you put the route in an explicit whitelist
     defined in the settings.

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