Template Tags
=============

This package includes some template tags that are designed to add some useful
features to any project.

render_form_error_summary
^^^^^^^^^^^^^^^^^^^^^^^^^

Determine if the context contains forms or formsets that should be
checked for errors, and then add any found errors to the context so they
can be rendered out at the top of the page.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_form_error_summary.html``

Example:

.. code:: html+django

    {% render_form_error_summary %}

render_fields
^^^^^^^^^^^^^

Render given fields with optional labels vertically.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_form.html``

Example:

.. code:: html+django

    {% render_fields fields %}

render_form
^^^^^^^^^^^

Render a vertical form.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_form.html``

Example:

.. code:: html+django

    {% render_form form %}

render_horizontal_fields
^^^^^^^^^^^^^^^^^^^^^^^^

Render given fields with optional labels horizontally.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_horizontal_form.html``

Example:

.. code:: html+django

    {% render_horizontal_fields field %}

render_horizontal_form
^^^^^^^^^^^^^^^^^^^^^^^^^

Render a horizontal form.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_horizontal_form.html``

Example:

.. code:: html+django

    {% render_horizontal_form form %}

render_horizontal_formset
^^^^^^^^^^^^^^^^^^^^^^^^^

Render a horizontal formset.

:Type: ``inclusion``
:Template: ``adminlte2/partials/_horizontal_formset.html``

Example:

.. code:: html+django

    {% render_horizontal_formset formset section_heading %}

get_logout_url
^^^^^^^^^^^^^^

Get the log out URL from the settings.

:Type: ``simple``

Example:

.. code:: html+django

    {{ get_logout_url }}

get_home_url
^^^^^^^^^^^^

Get the home URL from the settings.

:Type: ``simple``

Example:

.. code:: html+django

    {{ get_home_url }}

get_avatar_url
^^^^^^^^^^^^^^

Get a gravatar image url.
If no image is found, gravatar will return an image based on the 'default'
keyword. See http://en.gravatar.com/site/implement/images/ for more info.

This function will get the profile email in this order:
The 'email' argument,
The 'user' argument if it has an 'email' attribute.

:Type: ``simple``

Example:

.. code:: html+django

    {{ get_avatar_url }}

user_image_initials
^^^^^^^^^^^^^^^^^^^

Show user gravatar, initials, or gravatar default mystery person as image

Attempt to use/create initials of the user in the style of a profile picture.
Overlay with the user's gravatar image or a blank one if the user does not
exist. If initials can not be created, change the gravatar default from blank
to the standard mystery person.

If the user is passed in, the user will be used for the base information.
Information can be overridden by other key word arguments.
If the user is NOT passed in, key word arguments for each piece of information
should be used.

Keyword arguments:
user - the user to use for information
email - the email to use in place of the users
initials - the initials to use in place of generated ones from user
first_name - the first name to use in place of the users
last_name the last name to use in place of the users
size - the size of the image. Default is 25X25px

:Type: ``inclusive``
:Template: ``adminlte2/partials/_user_image_initials.html``

Example:

.. code:: html+django

    {{ user_image_initials }}

