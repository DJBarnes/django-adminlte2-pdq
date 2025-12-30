Advanced
********


General
=======

This section will cover some advanced concepts for defining your menu.
The full menu definition technically consists of more than just what can be
defined in the settings file. In total, there are 4 main sections of the menu.
They are listed below and are rendered out in the order listed.

* ``ADMINLTE2_MENU_FIRST`` - Manually defined. Must be provided via a template
  context variable.
* ``ADMINLTE2_MENU`` - Manually defined, via either the Django settings or a
  template context variable.
* ``Admin_Menu`` - Automatically generated from installed Apps and models.
  Shown/hidden via a settings toggle. See :doc:`admin` for more details.
* ``ADMINLTE2_MENU_LAST`` - Manually defined. Must be provided via a template
  context variable.

.. note::
   In the below sections, the ``ADMINLTE2_MENU`` section is generally referred
   to as the "main menu", with the other menu sections being supplementary to
   support it.

Some of the topics here will include all 4 parts, while others will focus on
only some of those parts. The advanced topics include:

* :ref:`menu/advanced:moving the menu outside settings`
* :ref:`menu/advanced:making part of the menu dynamic`
* :ref:`menu/advanced:making the entire menu dynamic`


Moving The Menu Outside Settings
================================

More than likely, your menu will grow in size over time and become a little
large to be living directly in the settings file. Although the menu variable
does technically have to live in the settings, some workarounds
allow defining the menu outside of the direct settings file.

The most common approach is to make a separate file that will contain your
menu definition, and then just import that definition in your settings file.


Example
-------

**my_django_project/menu.py**

.. code:: python

    ADMINLTE2_MENU = [
        {
            'text': 'Home',
            'nodes': [
                {
                    'route': 'home',
                    'text': 'Home',
                    'icon': 'fa fa-dashboard',
                },
            ]
        },
    ]

**my_django_project/settings.py**

.. code:: python

    try:
        from .menu import ADMINLTE2_MENU
    except ImportError:
        pass


Making Part Of The Menu Dynamic
===============================

It's possible to make the menu dynamic and generate it from the database (or
some other dynamic data source) on each page load. This is accomplished by
sending the dynamic menu to the template, via the page context.

If the menu is defined in both settings and the context, the context version
will always take precedence and override the settings version.

In addition, two menu sections are specifically meant to be
dynamic, and can only be delivered by a template's context. Those sections are
called ``ADMINLTE2_MENU_FIRST`` and ``ADMINLTE2_MENU_LAST``.


ADMINLTE2_MENU_FIRST and ADMINLTE2_MENU_LAST
--------------------------------------------

The two new menu definitions that can be sent via a template context are
``ADMINLTE2_MENU_FIRST``, and ``ADMINLTE2_MENU_LAST``, which render before or
after all other menu elements, respectively.

To rephrase, the menu sections render in the following order:

* ``ADMINLTE2_MENU_FIRST``
* ``ADMINLTE2_MENU``
* ``Admin_Menu`` (Note: This is not a variable, but rather the menu generated
  from the standard "Django Admin" views. For details, see
  :ref:`menu/admin:Displaying the Admin Menu`.)
* ``ADMINLTE2_MENU_LAST``

A practical use for this would be to define the main static menu using
the ``ADMINLTE2_MENU`` setting, and then define dynamic content
for the page via the context for a template, using either the
``ADMINLTE2_MENU_FIRST`` or ``ADMINLTE2_MENU_LAST`` key (or both keys).

You can see an example of this in the
:ref:`menu/examples:Dynamic and Static Menu Example`


Main Menu Via Context
---------------------

If you need the main menu to change dynamically, vs just adding dynamic content
before or after the static menu, you can send a template context variable
called ``ADMINLTE2_MENU`` to the template. This will override the static entry
defined in the Django settings, allowing this section to be dynamically defined
as well.

For an example, look at the
:ref:`menu/examples:Dynamic and Static Menu Example` and pretend that rather
than using the ``ADMINLTE2_MENU_FIRST`` as the context variable in ``views.py``,
you are using ``ADMINLTE2_MENU``.


Making The Entire Menu Dynamic
==============================

Via View Context Data
---------------------

If you need your menu to be more dynamic, you may consider generating and passing
menu data within your views.
This will allow the view to send custom menu values on a per-request basis,
optionally only overriding the "static" AdminLte PDQ menus on views that need it.

For example, in a class-based view, you may accomplish this with the following:

.. code:: python

    def get_context_data(self, **kwargs):

        ...

        # Override AdminLte menus with our custom ones.
        context["ADMINLTE2_MENU_FIRST"] = CUSTOM_MENU_FIRST
        context["ADMINLTE2_MENU"] = CUSTOM_MENU_STANDARD
        context["ADMINLTE2_MENU_LAST"] = CUSTOM_MENU_LAST

        ...

        # Return updated context.
        return context

For examples on how to define these menu variables, see
:doc:`examples` and :doc:`building_blocks`.

Note that you do not have to provide all three variables.
You can provide only those needed, and AdminLte PDQ will handle accordingly.
Any values not overridden in your view will resort to the "default" state.

These variables do the following:

* ``ADMINLTE2_MENU`` - The "base" menu displayed in AdminLte PDQ.

  * Providing this variable will override the static menu that normally
    displays on the sidebar.

  * If the project variable
    :ref:`configuration/menu:adminlte2_include_admin_nav_on_main_pages` is
    set to True AND the user accessing the view is a "staff" user, then
    this will display directly above the generated "Django Admin" menu.

* ``ADMINLTE2_MENU_FIRST`` - An additional menu section, which will always
  display at the top of the sidebar, above all other menus.

* ``ADMINLTE2_MENU_LAST`` - An additional menu section, which will always
  display at the bottom of the sidebar, below all other menus.


Via Context Processors
----------------------

If you need your menu to be fully dynamic with zero static content, you may
consider creating a menu context processor that could run on every request.
This can be used to send the needed menu context variable to each and every
template on every single request.

More information about how to make a context processor can be found in the
`Django docs <https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors>`_
.
