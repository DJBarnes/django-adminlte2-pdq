Menu
****

General information
===================

In its most basic configuration, the full sidebar is rendered by parsing the
contents of a Django setting called :ref:`configuration:adminlte2_menu`.
This setting will contain a menu definition consisting of reusable building
blocks in the form of either a
section_, separator_, node_, or tree_.
In the case of a tree, more building blocks are used to define the contents of
the tree.

Defining the menu in the settings file is best when the
sidebar content is static and the only thing that may change is the
visibility of entries based on whether or not a user is authorized
to see that particular thing.

For information on how to show/hide nodes based on authorization
see the :doc:`authorization` page.

In addition to defining the menu in the settings, it is also possible to pass
the menu definition to each template via the context. In this situation, the
context version will take precedence over the settings version.
This is great if you need to have your menu generated dynamically from data in
the database or a combination of static and dynamic entries.
See the :ref:`menu:advanced` section for more information regarding dynamic
menu generation and how to create a menu that consists of a combination of both
static and dynamic content.

Adminlte will also automatically add menu entries for the entire admin.
This will consist of entries for each app as well as each model.
By default, these admin menu entries can only be seen when the user is on an
admin page. But, this can be customized via some configuration settings defined
in the Django settings.
See the :ref:`configuration:menu configuration`
and :ref:`configuration:admin configuration` sections of
the :doc:`configuration` page for more information about those options.
Additionally, the icons used for each admin menu entry can be customized.
See the :ref:`menu:admin menu` section for information on how to customize the
admin menu.


Building Blocks
===============

The menu is built using a combination of the following 4 types of
building blocks described below.

Section
-------

A section will consist of section text and any nodes that
make up the remaining parts of the section. Neither the text nor the
nodes are required.
You can have no text and no nodes if you just want some extra space in the
sidebar between other sections.
You can have text with no nodes if you only want a header.
You can have nodes without text if you want a blank header for you nodes.
The most common implementation however will consist of defining both.

Section Fields
^^^^^^^^^^^^^^
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

Node Fields
^^^^^^^^^^^

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

Either a Font-Awesome 4 or 5 set of CSS classes. All required classes needed
to make the icon show up are required to be listed. More information about
Font-Awesome can be found at:
`Font-Awesome 4 <https://fontawesome.com/v4/icons/>`_ or
`Font-Awesome 5 <https://fontawesome.com/v5/search?m=free>`_.

:Key: ``icon``
:Type: ``string``
:Required: ``False``

**url**

An optional string representing the url for the link. It is **strongly**
recommended that you use the route key and the route for a view when defining
where a node will take the user rather than the actual URL.
However, you can specify the url key with a value of the url to take the user
to if desired.

:Key: ``url``
:Type: ``string``
:Required: ``False``

.. note::

    If you decide to use the url key, you must still provide the route key with
    a value of **"#"** as well since the sidebar is expecting that every node
    will have a route key.

.. tip::

    This url key is useful if you need to link to an external website rather
    than an internal link. External links must define any permissions directly
    on the node as there is no associated view to be able to pull permissions
    from. See the :doc:`authorization` page for more information.

**hook**

An optional string representing the name of a fully qualified function that can
be called to return the text for the node that should be rendered out.
This allows the ability to dynamically create the node's text.

Adminlte will try to import the value of this field as a function and then
invoke the function and use it's results as the text for the node.
The function should return either a string that will be used for both the text
and the title text of the node, or a 2-tuple with string values for both text
and title separately.

.. tip::

    This hook is best used for making a few nodes in an otherwise static menu
    dynamic. If you need a lot of dynamic nodes, the information in the
    advanced_ section might be more useful.


**permission**

TODO: Add this section.


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

**Menu**

.. code:: python

    {
        'route': '#',
        'text': 'Home',
        'icon': 'fa fa-dashboard',
        'url': 'https://github.com',
        'hook': 'core.utils.home_link_text',
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
and an icon in the sidebar.
In addition, the tree will contain other nodes and/or trees as the children of
the tree.
The use of trees can make a very large menu fit into a smaller space by
utilizing the ability to expand an collapse each tree.

Tree Fields
^^^^^^^^^^^

**text**

A string representing what will be rendered for the user to see.

:Key: ``text``
:Type: ``string``
:Required: ``False``

**icon**

Either a Font-Awesome 4 or 5 set of CSS classes. All required
to make the icon show up are required.

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



Advanced
========

General
-------

If you need your menu, or part of your menu to be dynamic and generated
from data in the database on each page load you can send the dynamic
menu to the template via the context. The context version will override
the settings version.

In addition to being able to send your dynamic menu to the template.

A practical use for this would be to define the main static menu using
the ``ADMINLTE2_MENU`` setting, and then defining dynamic content
for the page via the context for a template using the
``ADMINLTE2_MENU_FIRST`` key.

See the `Dynamic and Static Menu Full Example`_ section for a demonstration
on how to do this.


MENU_FIRST and MENU_LAST
------------------------
TODO: Add this section.

Main Menu Via Context
---------------------
TODO: Add this section.

Fully Dynamic Menu
------------------
TODO: Add this section.




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


Admin Menu
==========

Displaying Menu
---------------
TODO: Add this section.

Customizing icons
-----------------
TODO: Add this section.
