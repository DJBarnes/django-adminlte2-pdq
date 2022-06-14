Building Blocks
***************


The menu is built using a combination of the following 4 types of
building blocks:

* Section_
* Separator_
* Node_
* Tree_


Section
=======

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
------------
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
---------------

.. code:: python

    {
        'text': 'Home',
        'nodes': []
    }


Separator
=========

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
-----------------

.. code:: python

    {
        'text': '',
        'nodes': [],
        'separator': True,
    }


Node
====

A node is a python dictionary that will create a clickable sidebar link with a
name and an icon in the sidebar.


Node Keys
---------

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
All required classes needed to make the icon show up must be listed.

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
    doc:`advanced` section might be more useful.


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
    from. See the :doc:`../authorization/policies` page for more information.

**permissions**

An optional list of permissions as strings. The user must have all listed
permissions in order to see the node.

:Key: ``url``
:Type: ``list``
:Required: ``False``

.. warning::

    In general, you should use the functionality defined on the
    :doc:`../authorization/policies` page to add permissions to a View rather
    than directly to a node. Defining on the View will handle both hiding a
    node in the sidebar and preventing direct URL navigation without the need to
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
    :doc:`../authorization/policies` page to add permissions to a View rather
    than directly to a node. Defining on the View will handle both hiding a
    node in the sidebar and preventing direct URL navigation without the need to
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
    :doc:`../authorization/policies` page to add a login required criteria to a
    View rather than directly to a node.
    Defining on the View will handle both hiding a node in the
    sidebar and preventing direct URL navigation without the need to
    additionally define that login is required on this node.
    This key will **NOT** fully protect the link that the node is associated
    with.

.. tip::

    This key may be useful when you have an external link that needs to also
    be shown or hidden based on a the user being logged in.


Node Example
------------

.. code:: python

    {
        'route': 'django_adminlte_2:home',
        'text': 'Home',
        'icon': 'fa fa-dashboard',
    }


Complex Node Example
--------------------

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
====

A tree is a python dictionary that will create an expandable entry with text
and an icon in the sidebar. In addition, the tree will contain other nodes
and/or trees as the children of the tree.

Trees can make a very large menu fit into a smaller space by utilizing the
ability to expand an collapse each tree section.


Tree Keys
---------

**text**

A string representing what will be rendered for the user to see.

:Key: ``text``
:Type: ``string``
:Required: ``False``

**icon**

Either a `Font-Awesome 4 <https://fontawesome.com/v4/icons/>`_ or
`Font-Awesome 5 <https://fontawesome.com/v5/search?m=free>`_ set of CSS classes.
All required classes needed to make the icon show up must be listed.

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
------------
.. code:: python

    {
        'text': 'Sample Tree',
        'icon': 'fa fa-leaf',
        'nodes': [],
    },


Tree Example with a Node
------------------------

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


Tree Example with sub-tree and a Node
-------------------------------------
.. code:: python

    {
        'text': 'Sample Tree',
        'icon': 'fa fa-leaf',
        'nodes': [
            {
                'text': 'Sub Tree',
                'icon': 'fa fa-box',
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
