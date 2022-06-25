Authentication and Authorization Policy
***************************************

The **Django-AdminLTE-2** package comes with built-in functionality to make it
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

    Django-AdminLTE-2 provides a middleware that is required for some of the
    available authentication and authorization scenarios from this package to
    function.

    If you haven't already done so, add this middleware to your middleware list
    in ``settings.py`` so that you can use the full potential of this package.

Authentication
==============

Setting up authentication for the package requires choosing whether or not you
would like to require that users be logged in to gain access to the majority of
views in your site or if anonymous users are able to see the same things that
logged in users can.

If you would like to require that users are logged in to
visit the majority of your site, see the
:ref:`authorization/policies:login required`
section for more information on how to enable that.

Login Required
--------------

If you would like to prevent anonymous users from accessing the majority of
the views in your site, you can require that people are logged in by
setting the ``ADMINLTE2_USE_LOGIN_REQUIRED`` setting in your ``settings.py``
file to ``True``.

**settings.py**

.. code:: python

    ADMINLTE2_USE_LOGIN_REQUIRED = True

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
adding either the route name or url for the endpoint to the
``ADMINLTE2_LOGIN_EXEMPT_WHITELIST`` setting in your ``settings.py`` file.

**settings.py**

.. code:: python

    ADMINLTE2_LOGIN_EXEMPT_WHITELIST = [
        'two_factor_confirm',  # url_name of route to two factor confirmation
    ]

.. tip::

    If the majority of your routes do not require being logged in and you only
    have a handful that do, it is better to leave the
    ``ADMINLTE2_USE_LOGIN_REQUIRED`` undefined or set to ``False`` and instead
    use the
    :ref:`authorization/function_views:login required decorator` or
    :ref:`authorization/class_views:login required mixin` on the specific
    views that do require being logged in.


Authorization
=============

Setting up authorization for the package requires
:ref:`authorization/policies:choosing a policy` and then properly using
:ref:`authorization/function_views:Decorators` or
:ref:`authorization/class_views:Mixins`
provided by this package to set permissions on various views.

Setting the permissions on the view with the
:ref:`authorization/function_views:Decorators` and
:ref:`authorization/class_views:Mixins`
provided by this package will still prevent a user from accessing a view that
they do not have permission to access. Just like the ones provided by
`Django <https://docs.djangoproject.com/en/dev/topics/auth/default/#limiting-access-to-logged-in-users>`_.
But, they will additionally automatically hide sidebar links from the user for
those views.


Choosing a Policy
-----------------

The first step in using and configuring authorization for views and sidebar
menu links is to determine what general policy you want to adhere to.
Regardless of whether you have :ref:`authorization/policies:login required`
turned on or off, knowing what type of policy you want to achieve is critical.

Your choices are:

1.  :ref:`authorization/policies:Loose Policy` - By default all sidebar links and
    associated views are visible and accessible to the user.

    * Majority of sidebar links and associated views are visible to all users.
    * Sidebar links will still be visible and accessible if you set a required
      permission on that route's view and that user has the correct required
      permission to access that view.
    * Sidebar links will be hidden and associated views blocked if you set a
      required permission on that route's view and the user does not have the
      correct permission to access that view.

    .. warning::

        If you have :ref:`authorization/policies:login required`
        turned off and you opt for the
        :ref:`authorization/policies:Loose Policy`
        you  will be allowing all users, both logged in and anonymous, access
        to every view in your site that does not have a required permission
        defined.


2.  :ref:`authorization/policies:Strict Policy` - By default all sidebar links
    and associated views are hidden from the user.

    * Majority of sidebar links are hidden to all users.
    * Sidebar links will become visible and accessible if you set a required
      permission on that route's view and that user has the correct
      required permission.
    * Sidebar links will become visible and accessible if you put the route in
      an explicit whitelist defined in the settings.

    .. note::

        With the :ref:`authorization/policies:Strict Policy`, if you forget to
        add a permission to a view, the view will be inaccessible to everyone
        except superusers.
        This is a good way to ensure that you don't accidentally create a
        feature that everyone automatically has access to.
        You have to explicitly think about what permission is required for the
        feature and set that on the view before anyone can gain access to it.

Once you have determined what general policy you want to follow, use
the corresponding section to properly set up and configure authorization.


Loose Policy
------------

This policy assumes users should be able to see and access links and views, by
default.

Refer to the :doc:`../configuration/authorization` section for information about
the specific settings in settings.py mentioned below.

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

4.  Add any routes that do not require a specific permission and should
    be available to everyone to the ``ADMINLTE2_STRICT_POLICY_WHITELIST``
    in ``settings.py``

    **settings.py**

    .. code:: python

        ADMINLTE2_STRICT_POLICY_WHITELIST = [
            'tutorial'  # url_name of route to tutorial view.
        ]

    .. important::

        The **Strict Policy** whitelist comes with some default views that you
        do not have to worry about adding to the
        ``ADMINLTE2_STRICT_POLICY_WHITELIST`` setting.
        They include:

        * login - As defined via the ``LOGIN_URL`` setting in ``settings.py``
        * logout
        * password_reset
        * password_reset_done
        * password_reset_confirm
        * password_reset_complete
        * home - As defined via the ``ADMINLTE2_HOME_ROUTE`` setting in
          ``settings.py``

        |

        The Home route is included in the whitelist because we believe that
        there should be at least one view that a logged in user can access
        after logging in.
        Even if they do not have any permissions to see anything else in the
        site.
        The alternative would be to send them to the login page after
        logging in, which we believe would be confusing.
        Even if there were messages explaining why.

