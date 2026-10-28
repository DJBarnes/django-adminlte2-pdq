Styling Configuration
*********************

These settings and template blocks control the package's extra CSS. For the
color classes the CSS provides, see :doc:`../demo_css`.


----


Settings
========

ADMINLTE2_DEMO_CSS_COLORS
-------------------------

The colors shown on the :doc:`../demo_css` pages, as a dictionary of color
name to hex value. The hex value is only displayed on the color palette page.
Use this setting to remove colors from the demo pages, or to add colors you
have added to your project (see :ref:`demo_css:Adding a color`).

This setting only affects the demo pages. It does not add or remove CSS.

:Type: ``dict``
:Default: the package colors, in this order: ``default``, ``primary``,
    ``info``, ``success``, ``warning``, ``danger``, ``navy``, ``blue``,
    ``teal``, ``olive``, ``lime``, ``orange``, ``fuchsia``, ``indigo``,
    ``purple``, ``maroon``, ``gray``, ``black``

Example::

    from adminlte2_pdq.constants import DEMO_CSS_COLORS

    ADMINLTE2_DEMO_CSS_COLORS = {**DEMO_CSS_COLORS, "brand": "#6610f2"}


----


Dark Mode
=========

To use dark mode, set :ref:`configuration/home:ADMINLTE2_SKIN_CLASS` to one of
the dark skins:

* ``skin-blue-dark``
* ``skin-black-dark``
* ``skin-purple-dark``
* ``skin-yellow-dark``
* ``skin-red-dark``
* ``skin-green-dark``

Each dark skin uses the header color of the AdminLTE skin with the same name,
a dark sidebar, and dark page content. Dark mode covers Bootstrap and AdminLTE
elements, the package's color classes, the login page, and the Django admin
pages.

Example::

    ADMINLTE2_SKIN_CLASS = 'skin-blue-dark'

The dark mode CSS is always loaded and only applies under a dark skin class.
To switch between light and dark mode without reloading the page, for example
from a button or a user setting, replace the skin class on ``<body>``:

.. code:: javascript

    $('body').removeClass('skin-blue').addClass('skin-blue-dark');

The package does not store a user's choice. Projects that offer a choice keep
it themselves, for example in a user profile or a cookie, and override the
``skin_class`` block of ``adminlte2/base.html`` to render the chosen class.


Styling your own elements
-------------------------

Dark mode's colors are CSS custom properties that are defined under the dark
skin classes. Use them to style your own elements in dark mode:

==============================  ============================================
Property                        Used for
==============================  ============================================
``--pdq-dark-page``             Page background
``--pdq-dark-surface``          Boxes, panels, and modals
``--pdq-dark-raised``           Raised elements: input addons, wells
``--pdq-dark-border``           Borders
``--pdq-dark-border-strong``    Hover borders
``--pdq-dark-text``             Text
``--pdq-dark-text-soft``        Secondary text
``--pdq-dark-text-muted``       Muted text
==============================  ============================================

For example:

.. code:: css

    .skin-blue-dark .my-widget {
        color: var(--pdq-dark-text);
        background-color: var(--pdq-dark-surface);
    }


----


Template Blocks
===============

The package's CSS loads in the ``styles_main_fixes`` block of
``adminlte2/partials/_styles.html``. Each part has its own block, so a project
can replace or remove one part:

``styles_main_fixes__color_variables``
    Loads ``adminlte2_pdq/css/extra-colors/color-variables.css``.

``styles_main_fixes__extra_colors``
    Loads ``adminlte2_pdq/css/extra-colors/extra-colors.css``.

``styles_main_fixes__extra_features``
    Loads ``adminlte2_pdq/css/extra-features/extra-features.css``.

``styles_main_fixes__dark_mode``
    Loads ``adminlte2_pdq/css/dark-mode/dark-skins.css`` and
    ``adminlte2_pdq/css/dark-mode/dark-mode.css``.

For example, to load your own colors after the package's colors, override
``adminlte2/partials/_styles.html`` in your project:

.. code:: html+django

    {% extends "adminlte2/partials/_styles.html" %}
    {% load static %}

    {% block styles_main_fixes__extra_colors %}
      {{ block.super }}
      <link rel="stylesheet" href="{% static 'css/brand.css' %}">
    {% endblock styles_main_fixes__extra_colors %}

The package's JavaScript loads in the ``scripts_main_fixes`` block of
``adminlte2/partials/_scripts.html``.

.. note::

    The package requires a browser that supports CSS custom properties. All
    current browsers do; Internet Explorer does not.
