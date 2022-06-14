General Information
*******************


There are three possible configurations (which can be used together) for
defining a menu in the django-adminlte2 package:

* `Static Menu Definition`_
* `Dynamic Menu Definition`_
* `Auto-Built Admin Menu`_


Static Menu Definition
======================

In its most basic configuration, the full sidebar is rendered by parsing the
contents of a Django setting called :ref:`configuration/menu:adminlte2_menu`.
This setting will contain a menu definition consisting of reusable building
blocks in the form of either a
:ref:`menu/building_blocks:section`, :ref:`menu/building_blocks:separator`,
:ref:`menu/building_blocks:node`, or :ref:`menu/building_blocks:tree`.
All of which work in conjunction to build out the menu.

Defining the menu in the settings file is best when:

* All (or part) of the sidebar content is static
* The only thing that may change is the visibility of entries, based on
  whether or not a user is authorized to see that particular thing
  (More information available on the :doc:`../authorization/policies` page)


Dynamic Menu Definition
=======================

In addition to defining the menu in the settings, it is also possible to pass
the menu definition to each template via the context. In this situation, the
context version will take precedence over the settings version.
This is great if you either:

* Need to have your menu generated dynamically from data in the database
* Have a combination of static and dynamic menu entries

See the :doc:`advanced` section for more information regarding dynamic
menu generation, and how to create a menu that consists of a combination of both
static and dynamic content.


Auto-Built Admin Menu
=====================

Django-Adminlte can also automatically add menu entries for each app, and each
corresponding model within. This effectively mimics the Django admin navigation,
within the menu bar.

By default, these admin menu entries can only be seen when the user is on a
`Django Admin page <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_.
But, it can be customized via some configuration options in the Django settings
(See the :doc:`../configuration/menu` and :doc:`../configuration/admin` pages).


Additionally, the icons used for each admin menu entry can be customized as well
(See :doc:`admin_menu`).
