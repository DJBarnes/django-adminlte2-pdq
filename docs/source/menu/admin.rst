Admin Menu
**********


Displaying the Admin Menu
=========================

As mentioned previously, the AdminLTE package can
:ref:`Auto-Build an Admin Page menu<menu/general_information:Auto-Built Admin Menu>`.
By default, this will appear on all
`Django Admin pages <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_,.

To configure this admin menu to also show on non-admin pages, refer to
:ref:`configuration/menu:adminlte2_include_admin_nav_on_main_pages`.


Customizing Icons
=================

By default, the admin menu is rendered out with a filled circle
(``fa-circle``) as the icon for each app, and an empty circle (``fa-circle-o``)
for each model.

These default icons can be changed via some additional lines in the
corresponding
`Django Admin pages <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
``admin.py`` definition file.


First-party App Example
-----------------------

See the below example where a fictitious Blog app and, Post and Comment models
have their icons updated to be something more useful.

.. note:: The Django ``admin.site.register`` lines have been included for clarity.

**blog/admin.py**

.. code:: python

    from django_adminlte_2.admin_menu import AdminMenu

    ...

    # Register Post model with admin.
    admin.site.register(Post)
    # Update icon for Post model in admin menu.
    AdminMenu.set_model_icon('Post', 'fa fa-pencil-square-o')

    # Register Comment model with admin.
    admin.site.register(Post)
    # Update icon for Comment model in admin menu.
    AdminMenu.set_model_icon('Comment', 'fa fa-comment')

    # Update icon for Blog app in admin menu.
    AdminMenu.set_app_icon('Blog', 'fa fa-newspaper-o')


Third-Party App Example
-----------------------

Setting the icons does not need to be in the ``admin.py`` file for the app it
is configuring.

If you would like to update the icons for apps that you do not control,
such as the **User** and **Group** under the
**Authentication and Authorization** app, you can do that same work as
above, but in any ``admin.py`` file.

In this case, the **User** and **Group** model icons can be configured from
the ``admin.py`` file in our example Blog app.

**blog/admin.py**

.. code:: python

    from django_adminlte_2.admin_menu import AdminMenu

    ...

    # Update icon for User model in admin menu.
    AdminMenu.set_model_icon('User', 'fa fa-user')
    # Update icon for Group model in admin menu.
    AdminMenu.set_model_icon('Group', 'fa fa-group')
    # Update icon for Authentication and Authorization app in admin menu.
    AdminMenu.set_app_icon('Authentication and Authorization', 'fa fa-user')


Admin Home Link
---------------

If you have configured your site to show the Admin Home link in the sidebar,
there will be a link in the sidebar with the ``fa-superpowers`` icon.
You can change the icon for that link as well.

For information on how to enable the Admin Home link see
:ref:`configuration/admin:adminlte2_include_admin_home_link`.

In any ``admin.py`` file, call one additional method on the
**AdminMenu** to set the Admin Home link icon.

.. code:: python

    from django_adminlte_2.admin_menu import AdminMenu

    ...

    # Update icon for the Admin Home link.
    AdminMenu.set_admin_icon('fa fa-magic')


Admin Tri-Cog
=============

By default when viewing a
`Django Admin page <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_,
there is a tri-cog icon in the top right corner of the top bar.

This cog can be clicked to show additional information, via a popup sidebar.
Within this sidebar, there will be between zero and three different sections
shown, depending on the value defined for
:ref:`configuration/admin:ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS`.

Each of these three sections will show different content. If only one section is
enabled, then it automatically spans the area of the entire sidebar. If more
than one section is displayed, then navigational tabs are automatically created
at the top of the sidebar, to allow easy switching between the displayed
sections.

If all of the tabs are turned off, the entire tri-cog icon and associated
button will be removed and the user dropdown will shift to the right.

The default behavior is to populate this popup sidebar with the
"Recent Activity" section of the django admin. The other two sections are hidden
by default.
