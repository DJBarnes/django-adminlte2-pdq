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
