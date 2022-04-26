Authorization
*************

Setting up authorization for the sidebar and its associated links requires
choosing a Policy_ and then properly using some provided Decorators_ or Mixins_
to set permissions on various views.

Policy
======

There area a few options that can be used to control whether or not a
user can see and has access to routes defined on the sidebar.
The first step in using and configuring this correctly is to determine
what general policy you want to adhere to. Your choices are:

1. `Loose Policy`_ - By default all sidebar nodes are visible and accessible to
   the user.

   * Majority of sidebar nodes are visible and accessible to all users
   * Node will still be visible if you set a permission on that route's view
     and that user has the correct permission
   * Node will be hidden if you set a permission on that route's view and the
     user does not have permission


2. `Strict Policy`_ - By default all sidebar nodes are hidden and inaccessible to
   the user.

   * Majority of sidebar nodes are hidden and inaccessible to all users
   * Node will become visible if you set a permission on that route's view
     and that user has the correct permission
   * Node will become visible if you put the route in an explicit whitelist
     defined in the settings.

Once you have determined what general policy you want to follow, use
the following sections to properly set up and configure authorization.

Loose Policy
------------

Use the following steps to finish out your policy.
Refer to the :doc:`configuration` section for information about the specific
settings in settings.py mentioned below.

1. Ensure that the ``ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS``
   is either not defined in ``settings.py``, or set to ``False`` if it is.

2. If you are using function based views, follow the steps in the
   `Loose Decorator Example`_ section to add permissions to views that require
   permission to access.

3. If you are using class based views, follow the steps in the
   `Loose Mixin Example`_ section to add permissions to views that require
   permission to access.

Strict Policy
-------------

Use the following steps to finish out your policy.
Refer to the :doc:`configuration` section for information about the specific
settings in settings.py mentioned below.

1. Ensure that the ``ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS``
   is defined in ``settings.py`` and is set to ``True``.

2. If you are using function based views, follow the steps in the
   `Strict Decorator Example`_ section to add permissions to views that require
   permission to access.

3. If you are using class based views, follow the steps in the
   `Strict Mixin Example`_ section to add permissions to views that require
   permission to access.

4. Add any routes that do not require a specific permission and should
   be available to everyone to the ``ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST``
   in ``settings.py``

Function based views
====================

Decorators
----------

There are two decorators that can be used on a view to control whether a
user has access to both the view, and the visibility of any nodes in the
sidebar that link to that view.

Requires All permissions
^^^^^^^^^^^^^^^^^^^^^^^^

``@requires_all_permissions``

This decorator will list all required permissions for the view. It uses
Django's default permission checking to know whether to show the view to
the user, but also adds the required property to the view so that the
permissions are required to see the equivalent node on the sidebar.


Requires One Permission
^^^^^^^^^^^^^^^^^^^^^^^

``@requires_one_permission``

This decorator will list the permissions that a user must have at least one
of in order to access the view and see the associated sidebar node.

Decorator Examples
------------------

Requires All permissions
^^^^^^^^^^^^^^^^^^^^^^^^

In this example, if the user does not have all of the permissions that we
define on this decorator, the user will not be able to access this View nor
will they see a sidebar menu entry that maps to this View. However, if the user
does have all of these permissions, they will see the sidebar link and have
access.

Example::

    @requires_all_permissions([
        'auth.add_group',
        'auth.change_group',
        'auth.delete_group'
    ])
    def sample1(request):
        """Show default sample1 page"""
        return render(request, 'adminlte2/sample1.html', {})

Requires One Permission
^^^^^^^^^^^^^^^^^^^^^^^

In this example, if the user does not have at least one of the permissions that
we define on this decorator, the user will not be able to access this View nor
will they see a sidebar menu entry that maps to this View. However, if the user
has at least one of any of these permissions, they will see the sidebar link
and have access.

Example::

    @requires_one_permission([
        'auth.add_permission',
        'auth.change_permission',
        'auth.delete_permission'
    ])
    def sample2(request):
        """Show default sample2 page"""
        return render(request, 'adminlte2/sample2.html', {})

Loose Decorator Example
^^^^^^^^^^^^^^^^^^^^^^^

Strict Decorator Example
^^^^^^^^^^^^^^^^^^^^^^^^


Class based views
====================

Mixins
------

Mixin Examples
--------------

Requires All permissions
^^^^^^^^^^^^^^^^^^^^^^^^

Requires One Permission
^^^^^^^^^^^^^^^^^^^^^^^

Loose Mixin Example
^^^^^^^^^^^^^^^^^^^

Strict Mixin Example
^^^^^^^^^^^^^^^^^^^^
