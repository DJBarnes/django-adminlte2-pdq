Menu
****

General information
===================

There are three possible configurations (which can be used together) for
defining a menu in the django-adminlte2 package:

* `Static Menu Definition`_
* `Dynamic Menu Definition`_
* `Auto-Built Admin Menu`_

Static Menu Definition
----------------------

In its most basic configuration, the full sidebar is rendered by parsing the
contents of a Django setting called :ref:`configuration:adminlte2_menu`.
This setting will contain a menu definition consisting of reusable building
blocks in the form of either a
section_, separator_, node_, or tree_.
All of which work in conjunction to build out the menu.

Defining the menu in the settings file is best when:

* All (or part) of the sidebar content is static
* The only thing that may change is the visibility of entries, based on
  whether or not a user is authorized to see that particular thing
  (More information available on the :doc:`authorization` page)

Dynamic Menu Definition
-----------------------

In addition to defining the menu in the settings, it is also possible to pass
the menu definition to each template via the context. In this situation, the
context version will take precedence over the settings version.
This is great if you either:

* Need to have your menu generated dynamically from data in the database
* Have a combination of static and dynamic menu entries

See the :ref:`menu:advanced` section for more information regarding dynamic
menu generation, and how to create a menu that consists of a combination of both
static and dynamic content.

Auto-Built Admin Menu
---------------------

Django-Adminlte can also automatically add menu entries for each app, and each
corresponding model within. This effectively mimics the Django admin navigation,
within the menu bar.

By default, these admin menu entries can only be seen when the user is on a
`Django Admin page <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_.
But, it can be customized via some configuration options in the Django settings
(See the :ref:`configuration:menu configuration` and
:ref:`configuration:admin configuration` sections of
the :doc:`configuration` page for more information).


Additionally, the icons used for each admin menu entry can be customized as well
(See :ref:`menu:admin menu`).

----

Building Blocks
===============

The menu is built using a combination of the following 4 types of
building blocks:

* Section_
* Separator_
* Node_
* Tree_

Section
-------

A section will consist of section text and any nodes that
make up the remaining parts of the section. Neither the text nor the
nodes are required.

For Example:

* You can have no text and no nodes if you just want some extra space in the
  sidebar between other sections.
* You can have text with no nodes if you only want a header.
* You can have nodes without text if you want a blank header.

Generally speaking, most common implementation will consist of defining both
text and nodes.

Section Keys
^^^^^^^^^^^^
**text**

A string representing the section text that a user will see.

:Key: ``text``
:Type: ``string``
:Required: ``False``

**nodes**

A list of node_ dictionaries that will render out each sidebar link,
and/or a tree_ definition that contains additional nodes to render links.

:Key: ``nodes``
:Type: ``list``
:Required: ``False``

Section Example
^^^^^^^^^^^^^^^
.. code:: python

    {
        'text': 'Home',
        'nodes': []
    }


Separator
---------

A section with no text or nodes, but a key called separator that is set to
True. This will render out a physical line separating one section from the
next.

**text**

A blank string.

:Key: ``text``
:Type: ``string``
:Required: ``True``

**nodes**

An empty list.

:Key: ``nodes``
:Type: ``list``
:Required: ``True``

**separator**

Defined as ``True``.

:Key: ``separator``
:Type: ``bool``
:Required: ``True``

Separator Example
^^^^^^^^^^^^^^^^^
.. code:: python

    {
        'text': '',
        'nodes': [],
        'separator': True,
    }


Node
----

A node is a python dictionary that will create a clickable sidebar link with a
name and an icon in the sidebar.

Node Keys
^^^^^^^^^

**route**

A valid django route. If you are scaffolding your menu out and do
not have a valid route yet, just enter a ``#`` as a place holder.

:Key: ``route``
:Type: ``string``
:Required: ``True``

**text**

A string representing what will be rendered for the user to see.

:Key: ``text``
:Type: ``string``
:Required: ``False``

**icon**

Either a `Font-Awesome 4 <https://fontawesome.com/v4/icons/>`_ or
`Font-Awesome 5 <https://fontawesome.com/v5/search?m=free>`_ set of CSS classes.
All required classes needed to make the icon show up are must be listed.

:Key: ``icon``
:Type: ``string``
:Required: ``False``

**hook**

An optional string representing the name of a fully qualified function that can
be called to return the text for the node that should be rendered out.
This allows the ability to dynamically create the node's text.

:Key: ``hook``
:Type: ``string``
:Required: ``False``

.. note::

    Adminlte will try to import the value for this key as a function and then
    invoke the function and use it's results as the text for the node.

    The function should return either a string that will be used for both the
    text and the title text of the node, or a 2-tuple with string values for
    both text and title separately.

.. tip::

    This hook is best used for making a few nodes in an otherwise static menu
    dynamic. If you need a lot of dynamic nodes, the information in the
    advanced_ section might be more useful.


**url**

An optional string representing the url for the link.

:Key: ``url``
:Type: ``string``
:Required: ``False``

.. warning::

    When defining internal urls, it is **strongly** recommended that you avoid
    this key. Instead, preferably use the route key (and the Django route to
    define the view) for a node, rather than the actual URL. This key is
    generally reserved for defining external urls.

.. note::

    If you decide to use the url key, you must still provide the route key with
    a value of ``"#"`` as well since the sidebar is expecting that every node
    will have a route key.

.. tip::

    This url key is useful if you need to link to an external website rather
    than an internal link. External links must define any permissions directly
    on the node as there is no associated view to be able to pull permissions
    from. See the :doc:`authorization` page for more information.

**permissions**

An optional list of permissions as strings. The user must have all listed
permissions in order to see the node.

:Key: ``url``
:Type: ``list``
:Required: ``False``

.. warning::

    In general, you should use the functionality defined on the
    :doc:`authorization` page to add permissions to a View rather than directly
    to a node. Defining on the View will handle both hiding a node in the
    sidebar and preventing direct URL navigation without the need to
    additionally set the permissions on this node key.
    This key will **NOT** fully protect the link that the node is associated
    with.

.. tip::

    This key may be useful when you have an external link that needs to also
    be shown or hidden based on a list of permissions.


**one_of_permissions**

An optional list of permissions as strings. The user must have at least one of
these order to see the node.

:Key: ``url``
:Type: ``list``
:Required: ``False``

.. warning::

    In general, you should use the functionality defined on the
    :doc:`authorization` page to add permissions to a View rather than directly
    to a node. Defining on the View will handle both hiding a node in the
    sidebar and preventing direct URL navigation without the need to
    additionally set the permissions on this node key.
    This key will **NOT** fully protect the link that the node is associated
    with.

.. tip::

    This key may be useful when you have an external link that needs to also
    be shown or hidden based on a list of permissions.


**login_required**

An optional key on the node specifying whether a user must be logged in to
the system in order to see the node.

:Key: ``url``
:Type: ``bool``
:Required: ``False``

.. warning::

    In general, you should use the functionality defined on the
    :doc:`authorization` page to add a login required criteria to a View rather
    than directly to a node.
    Defining on the View will handle both hiding a node in the
    sidebar and preventing direct URL navigation without the need to
    additionally define that login is required on this node.
    This key will **NOT** fully protect the link that the node is associated
    with.

.. tip::

    This key may be useful when you have an external link that needs to also
    be shown or hidden based on a the user being logged in.


Node Example
^^^^^^^^^^^^
.. code:: python

    {
        'route': 'django_adminlte_2:home',
        'text': 'Home',
        'icon': 'fa fa-dashboard',
    }

Complex Node Example
^^^^^^^^^^^^^^^^^^^^

**Node**

.. code:: python

    {
        'route': '#',
        'text': 'Github',
        'icon': 'fa fa-github',
        'url': 'https://github.com',
        'hook': 'core.utils.home_link_text',
        'permissions': ['is_developer'],
    }

**core/utils.py**

.. code:: python

    def home_link_text(context):
        "Custom home link text"
        text = 'Home'
        if user.is_staff:
            text = 'Home!!!!!'
        return text


Tree
----

A tree is a python dictionary that will create an expandable entry with text
and an icon in the sidebar. In addition, the tree will contain other nodes
and/or trees as the children of the tree.

Trees can make a very large menu fit into a smaller space by utilizing the
ability to expand an collapse each tree section.

Tree Keys
^^^^^^^^^^^

**text**

A string representing what will be rendered for the user to see.

:Key: ``text``
:Type: ``string``
:Required: ``False``

**icon**

Either a `Font-Awesome 4 <https://fontawesome.com/v4/icons/>`_  or
`Font-Awesome 5 <https://fontawesome.com/v5/search?m=free>`_ set of CSS classes.
All icon classes required to make the icon show must be listed.

:Key: ``icon``
:Type: ``string``
:Required: ``False``

**nodes**

A list of node dictionaries that will render out each sidebar link,
or a tree that will contain more nodes.

:Key: ``nodes``
:Type: ``list``
:Required: ``False``

Tree Example
^^^^^^^^^^^^
.. code:: python

    {
        'text': 'Sample Tree',
        'icon': 'fa fa-leaf',
        'nodes': [],
    },

Tree Example with a Node
^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    {
        'text': 'Sample Tree',
        'icon': 'fa fa-leaf',
        'nodes': [
            {
                'route': 'django_adminlte_2:sample2',
                'text': 'Sample2',
                'icon': 'fa fa-building',
            },
        ],
    },

----

Static Menu Full Example
========================

**settings.py**

.. code:: python

    ADMINLTE2_MENU = [
        {
            'text': 'Home',
            'nodes': [
                {
                    'route': 'django_adminlte_2:home',
                    'text': 'Home',
                    'icon': 'fa fa-dashboard',
                },
                {
                    'route': 'django_adminlte_2:demo-css',
                    'text': 'Demo CSS',
                    'icon': 'fa fa-file'
                },
            ]
        },
        {
            'text': 'Profile',
            'nodes': [
                {
                    'route': 'password_change',
                    'text': 'Change Password',
                    'icon': 'fa fa-lock'
                }
            ]
        },
        {
            'text': 'Samples',
            'nodes': [
                {
                    'route': 'django_adminlte_2:sample1',
                    'text': 'Sample1',
                    'icon': 'fa fa-group',
                },
                {
                    'text': 'Sample Tree',
                    'icon': 'fa fa-leaf',
                    'nodes': [
                        {
                            'route': 'django_adminlte_2:sample2',
                            'text': 'Sample2',
                            'icon': 'fa fa-building',
                        },
                    ],
                },
            ],
        },
    ]

.. image:: ../img/menu/django-adminlte-2-static-menu.png
    :alt: Site with static menu using settings

----

Advanced
========

General
-------

This section will cover some advanced concepts for defining your menu.
The full menu definition technically consists of more than just what can be
defined in the settings file. In total, there are 4 main sections of the menu.
They are listed below and are rendered out in the order listed.

* ``ADMINLTE2_MENU_FIRST`` - Manually defined. Must be provided via a template
  context variable.
* ``ADMINLTE2_MENU`` - Manually defined, via either the Django settings or a
  template context variable.
* ``Admin_Menu`` - Automatically generated from installed Apps and models.
  Shown/hidden via a settings toggle. See `Admin Menu`_ for more details.
* ``ADMINLTE2_MENU_LAST`` - Manually defined. Must be provided via a template
  context variable.

.. note::
   In the below sections, the ``ADMINLTE2_MENU`` section is generally referred
   to as the "main menu", with the other menu sections being supplementary to
   support it.

Some of the topics here will include all 4 parts, while others will focus on
only some of those parts. The advanced topics include:

* :ref:`menu:moving the menu outside settings`
* :ref:`menu:making part of the menu dynamic`
* :ref:`menu:making the entire menu dynamic`

Moving The Menu Outside Settings
--------------------------------

More than likely your menu will grow in size over time and become a little
large to be living directly in the settings file. Although the menu does
technically have to live in the settings, there are some workarounds that you
can do so that your menu can be defined outside the direct settings file.

The most common approach is to make a separate file that will contain your
menu definition, and then just import that definition in your settings file.

Outside Settings Example
^^^^^^^^^^^^^^^^^^^^^^^^

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
-------------------------------

It's possible to make the menu dynamic, and generate from the database (or
some other dynamic data source) on each page load. This is accomplished by
sending the dynamic menu to the template, via the page context.

The context version will override the settings version. In addition, there are
two menu sections that are specifically meant to be dynamic and can only be
delivered by a template's context. Those sections are called
:ref:`menu:ADMINLTE2_MENU_FIRST and ADMINLTE2_MENU_LAST`.

ADMINLTE2_MENU_FIRST and ADMINLTE2_MENU_LAST
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The two new menu definitions that can be sent via a template context are
**ADMINLTE2_MENU_FIRST**, and **ADMINLTE2_MENU_LAST**, which render before or
after all other menu elements, respectively.

To rephrase, the menu sections render in the following order:

* ``ADMINLTE2_MENU_FIRST``
* ``ADMINLTE2_MENU``
* ``Admin_Menu``
* ``ADMINLTE2_MENU_LAST``

A practical use for this would be to define the main static menu using
the ``ADMINLTE2_MENU`` setting, and then define dynamic content
for the page via the context for a template, using either the
``ADMINLTE2_MENU_FIRST`` or ``ADMINLTE2_MENU_LAST`` key (or both keys).

You can see an example of this in the
:ref:`menu:Dynamic and Static Menu Full Example`

Main Menu Via Context
^^^^^^^^^^^^^^^^^^^^^

If you need the main menu to change dynamically, vs just adding dynamic content
before or after the static menu, you can send a template context variable
called ``ADMINLTE2_MENU`` to the template. This will override the static entry
defined in the Django settings, allowing this section to be dynamically defined
as well.

For an example, look at the
:ref:`menu:Dynamic and Static Menu Full Example` and pretend that rather than
using the ``ADMINLTE2_MENU_FIRST`` as the context variable in ``views.py``, you
are using ``ADMINLTE2_MENU``.

Making The Entire Menu Dynamic
------------------------------

If you need your menu to be fully dynamic with zero static content, you may
consider creating a menu context processor that could run on every request.
This can be used to send the needed menu context variable to each and every
template on every single request.

More information about how to make a context processor can be found in the
`Django docs <https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors>`_
.

----

Dynamic and Static Menu Full Example
====================================

**settings.py**

.. code:: python
    :name: settings.py

    ADMINLTE2_MENU = [
        {
            'text': 'Home',
            'nodes': [
                {
                    'route': 'django_adminlte_2:home',
                    'text': 'Home',
                    'icon': 'fa fa-dashboard',
                },
                {
                    'route': 'django_adminlte_2:demo-css',
                    'text': 'Demo CSS',
                    'icon': 'fa fa-file'
                },
            ]
        },
    ]

**urls.py**

.. code:: python
    :name: urls.py

    urlpatterns = [

        path('dynamic/', views.dynamic, name="dynamic"),
        ...
    ]

**views.py**

.. code:: python
    :name: views.py

    def dynamic(request):
        """Show default dynamic page"""

        dynamic_content = [
            {
                'text': 'Dynamic Stuff',
                'nodes': [
                    {
                        'route': 'dynamic',
                        'text': 'Dynamic',
                        'icon': 'fa fa-circle',
                    },
                ]
            },
        ]

        return render(
            request,
            'dynamic.html',
            {
                'ADMINLTE2_MENU_FIRST': dynamic_content
            }
        )

**dynamic.html**

.. code:: html+django
    :name: dynamic.html

    {% extends "adminlte2/base.html" %}
    {% load i18n %}
    {% block breadcrumbs %}
    <ol class="breadcrumb">
        {% include "admin/partials/_breadcrumb_home.html" %}
        <li>
            {% trans 'Dynamic' %}
        </li>
    </ol>
    {% endblock breadcrumbs %}
    {% block content %}
    <h1>This is the Dynamic page!</h1>
    {% endblock content %}

.. image:: ../img/menu/django-adminlte-2-dynamic-menu.png
    :alt: Site with static and dynamic menu using settings and context

----

Admin Menu
==========

Displaying Menu
---------------

By default, an automatic "Admin Menu" will appear on all
`Django Admin pages <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
.

This menu will create entries corresponding to each installed app, and each
corresponding model.

.. note::
   If you would like to also see the admin menu on non-admin pages, refer to the
   :ref:`configuration:adminlte2_include_admin_nav_on_main_pages`
   section of the :doc:`configuration` page.

Customizing Icons
-----------------

By default, the admin menu is rendered out with a filled circle
(``fa-circle``) as the icon for each app, and an empty circle (``fa-circle-o``)
for each model.

These default icons can be changed via some additional lines in the
corresponding
`Django Admin pages <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_
``admin.py`` definition file.

First-party App Example
^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^

If you have configured your site to show the Admin Home link in the sidebar,
there will be a link in the sidebar with the ``fa-superpowers`` icon.
You can change the icon for that link as well.

For information on how to enable the Admin Home link see the
:ref:`configuration:adminlte2_include_admin_home_link`
section of the :doc:`configuration` page.

In any ``admin.py`` file, call one additional method on the
**AdminMenu** to set the Admin Home link icon.

.. code:: python

    from django_adminlte_2.admin_menu import AdminMenu

    ...

    # Update icon for the Admin Home link.
    AdminMenu.set_admin_icon('fa fa-magic')


