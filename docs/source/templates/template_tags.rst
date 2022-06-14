Template Tags
*************

This package includes some template tags that are designed to add some useful
features to any project.

To use any of the following template tags you first need to load them at the
top of your template.

.. code:: html+django

    {% load adminlte_tags %}


----


render_form_error_summary
=========================

Determine if the context contains forms or formsets that should be
checked for errors, and then add any found errors to the context so they
can be rendered out at the top of the page.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_form_error_summary.html``

**Example:**

.. code:: html+django

    {% render_form_error_summary %}

render_fields
=============

Render given fields with optional labels vertically.

:param fields_to_render: List or tuple of fields to render out.
:param labels: Whether to use labels for fields. Defaults to True.
:param media: Media that needs to be used in the form. Defaults to None.
:return: Context to use with template.

:Tag Type: ``inclusion``
:Template: ``adminlte2/partials/_form.html``

**Example:**

.. code:: html+django

    {% render_fields fields %}

render_form
===========

Render a vertical form where fields are always below the label.

:param form: Form to render.
:param labels: Whether to use labels for fields. Defaults to True.
:param media: Media that needs to be used in the form. Defaults to None.
:return: Fields to render.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_form.html``

**Example:**

.. code:: html+django

    {% render_form form %}

render_horizontal_fields
========================

Render given fields with optional labels horizontally.

:param fields_to_render: List or tuple of fields to render.
:param labels: Whether to use labels for fields. Defaults to True.
:param media: Media that needs to be used in the form. Defaults to None.
:return: Context to use with template.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_horizontal_form.html``

**Example:**

.. code:: html+django

    {% render_horizontal_fields field %}

render_horizontal_form
======================

Render a horizontal form.

:param form: The form to render.
:param labels: Whether to use labels for fields. Defaults to True.
:param media: Media that needs to be used in the form. Defaults to None.
:return: Context for the template.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_horizontal_form.html``

**Example:**

.. code:: html+django

    {% render_horizontal_form form %}

render_horizontal_formset
=========================

Render a horizontal formset.

:param formset: The formset to render.
:param section_heading: The section header to render.
:return: Context for the template.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_horizontal_formset.html``

**Example:**

.. code:: html+django

    {% render_horizontal_formset formset section_heading %}

get_logout_url
==============

Get the log out URL from the settings.

:Type: ``simple``

**Example:**

.. code:: html+django

    {{ get_logout_url }}

get_home_url
============

Get the home URL from the settings and default to the django_adminlte_2 home.

:Type: ``simple``

**Example:**

.. code:: html+django

    {{ get_home_url }}

get_avatar_url
==============

Get a gravatar image url.
If no image is found, gravatar will return an image based on the 'default'
keyword. See http://en.gravatar.com/site/implement/images/ for more info.

This function will get the profile email in this order:

1. The 'email' argument,
2. The 'user' argument if it has an 'email' attribute.

:param context: Context that is not used.
:param user: User that may have an email that can be used for gravatar.
:param email: Email that can be used for gravatar.
:param size: Size if it needs to be overridden.
:param default: The default gravatar that will be used if no email.

:Type: ``simple``

**Example:**

.. code:: html+django

    {{ get_avatar_url }}

user_image_initials
===================

Show user gravatar, initials, or gravatar default mystery person as image

Attempt to use/create initials of the user in the style of a profile picture.
Overlay with the user's gravatar image or a blank one if the user does not
exist. If initials can not be created, change the gravatar default from blank
to the standard mystery person.

If the user is passed in, the user will be used for the base information.
Information can be overridden by other key word arguments.
If the user is NOT passed in, key word arguments for each piece of information
should be used.

:param context: Context for the template.
:param user: The user to use for information.
:param email: The email to use for information.
:param initials: The initials to use in place of generated ones.
:param first_name: The first name to use in place of the users.
:param last_name: The last name to use in place of the users.
:param size: Size if it needs to be overridden. Default is 25x25.
:return: Context for template.

:Type: ``inclusive``
:Template: ``adminlte2/partials/_user_image_initials.html``

**Example:**

.. code:: html+django

    {{ user_image_initials }}

