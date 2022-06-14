General Information
*******************

In the context of the **Django-AdminLTE-2** package, the "menu" is the set of
navigational elements, displayed on the left-hand side of the default page
layout.

There are three possible configurations (which can be used together) for
defining a menu in the Django-AdminLTE-2 package:

* `Static Menu Definition`_
* `Dynamic Menu Definition`_
* `Auto-Built Admin Menu`_


Static Menu Definition
======================

In its most basic configuration, the full sidebar is rendered by parsing the
contents of a Django setting called :ref:`configuration/menu:adminlte2_menu`.
This setting will contain a menu definition consisting of four possible reusable
:doc:`building_blocks` (see
:ref:`menu/building_blocks:section`, :ref:`menu/building_blocks:separator`,
:ref:`menu/building_blocks:node`, and :ref:`menu/building_blocks:tree`).

Defining the menu in the settings file is best when:

* All (or part) of the sidebar content is static.
* The only thing that may change is the visibility of entries, based on
  whether or not a user is authorized to see that particular thing
  (More information available on the :doc:`../authorization/policies` page).


Dynamic Menu Definition
=======================

In addition to defining the menu in the settings, it is also possible to pass
the menu definition to each template via the context. In this situation, the
context version will take precedence over the settings version.
This is great if you either:

* Need to have your menu generated dynamically from data in the database.
* Have a combination of static and dynamic menu entries.

See the :doc:`advanced` section for more information regarding dynamic
menu generation, and how to create a menu that consists of a combination of both
static and dynamic content.


Auto-Built Admin Menu
=====================

Django-AdminLTE-2 also automatically updates the stylings of the site
`Django Admin pages <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_,
so that they match the same
`AdminLTE2 <https://adminlte.io/themes/AdminLTE/index2.html>`_ theme used by the
rest of the site.

As such, it makes sense that the Django-AdminLTE-2 package will generate a
corresponding set of menu nav elements, to allow navigation of these admin
pages.

By default, these admin menu entries will only be seen when the user is on a
Django Admin page. But this behavior can be customized via some configuration
options in the Django settings (See :doc:`../configuration/menu` and
:doc:`../configuration/admin`).


Additionally, the icons used for each admin menu entry can be customized as well
(See :doc:`admin`).
