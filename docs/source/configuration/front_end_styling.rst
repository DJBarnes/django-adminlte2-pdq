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

Example, with some of the package's colors and one of the project's own::

    # adminlte2_pdq.generate_color_css doesn't read any settings, so it can be imported in settings.py.
    from adminlte2_pdq.generate_color_css import COLORS_BY_NAME

    ADMINLTE2_DEMO_CSS_COLORS = {
        **{name: COLORS_BY_NAME[name].base for name in ("primary", "success", "warning", "danger")},
        "brand": "#6610f2",
    }

.. warning::

    Don't import ``adminlte2_pdq.constants`` in ``settings.py``. It reads every
    ``ADMINLTE2_*`` setting when it is imported, so settings defined after the
    import are ignored.


ADMINLTE2_CONSISTENT_COLORS
---------------------------

Whether each color name is one color on every class. By default, colors look
exactly as in AdminLTE and Bootstrap, where some classes use shades that
differ from the rest of their color (see :ref:`demo_css:Color classes`).

When True, the page also loads
``adminlte2_pdq/css/extra-colors/consistent-colors.css``, and:

* Bootstrap's ``bg-primary``, ``bg-info``, ``bg-success``, ``bg-warning``, and
  ``bg-danger`` look like AdminLTE's ``bg-light-blue``, ``bg-aqua``,
  ``bg-green``, ``bg-yellow``, and ``bg-red``, and get ``bg-{color}-active``
  classes. Bootstrap's ``text-{color}`` classes for the same colors look like
  AdminLTE's.
* Table header and footer rows with Bootstrap's ``success``, ``info``,
  ``warning``, and ``danger`` classes take the color itself, as every other
  color does.
* Buttons of these colors, and ``btn-default``, use the color's AdminLTE
  shades when focused, pressed, or disabled, and for their badge.
* The default box and label are the light gray of the default button's edge,
  ``--pdq-default-border``, instead of AdminLTE's darker gray, which is the
  ``gray`` color.

These classes still use the color variables, so a changed color applies to
them too.

:Type: ``bool``
:Default: ``False``

Example::

    ADMINLTE2_CONSISTENT_COLORS = True


----


Dark Mode
=========

The package adds a dark version of each AdminLTE skin color:

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

In the Django admin pages, the skin decides between light and dark, as in the
rest of the site. Django admin's own dark mode, which follows the browser, is
not used: under a light skin the admin stays light even when the browser is
in dark mode, and under a dark skin it uses dark mode's colors.

By default, the site follows the browser's light or dark mode setting: it uses
:ref:`configuration/home:ADMINLTE2_SKIN_CLASS_LIGHT` when the
browser is in light mode and
:ref:`configuration/home:ADMINLTE2_SKIN_CLASS_DARK` when it is in
dark mode, and switches when the browser's setting changes. To always use
:ref:`configuration/home:ADMINLTE2_SKIN_CLASS`, set
:ref:`configuration/home:ADMINLTE2_SKIN_FOLLOW_BROWSER` to
``False``.

The dark mode CSS is always loaded and only applies under a dark skin class.
To switch between light and dark mode from your own code, for example from a
button or a user setting, turn off browser following and replace the skin
class on ``<body>``:

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

``styles_main_fixes__consistent_colors``
    Loads ``adminlte2_pdq/css/extra-colors/consistent-colors.css`` when
    ``ADMINLTE2_CONSISTENT_COLORS`` is True.

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

Most of the package's JavaScript loads in the ``scripts_main_fixes`` block of
``adminlte2/partials/_scripts.html``. The scripts that follow the browser's
light or dark mode and remember the sidebar's state load in the
``skin_follow_browser`` and ``sidebar_state`` blocks of ``adminlte2/base.html``.

.. note::

    The package requires a browser that supports CSS custom properties. All
    current browsers do; Internet Explorer does not.


Where Third-Party Files Load From
=================================

The package's own CSS and JavaScript always load from its static files. The
third-party libraries it uses (jQuery, jQuery UI, Bootstrap, Font Awesome,
AdminLTE, DataTables, Inputmask, and the date pickers) load from one of two
places, depending on the template variable ``debug``:

* When ``debug`` is True, from the package's static files, under
  ``third-party/``.
* Otherwise, from ``cdnjs.cloudflare.com`` and ``cdn.datatables.net``. Each
  file has an integrity hash, so the browser refuses a file that differs from
  the one the package was tested with.

Django sets ``debug`` only when ``DEBUG`` is True, the
``django.template.context_processors.debug`` context processor is installed,
and the request comes from an address in ``INTERNAL_IPS``. So a development
site without ``INTERNAL_IPS`` loads the libraries from the CDNs too.

To always load them from the static files, for example on a network without
internet access, or with a Content Security Policy that doesn't allow the
CDNs, override the two partial templates in your project:

**adminlte2/partials/_styles.html**

.. code:: html+django

    {% extends "adminlte2/partials/_styles.html" %}

    {% block styles_prod %}
      {% include "adminlte2/partials/_styles/_styles_debug.html" %}
    {% endblock styles_prod %}

**adminlte2/partials/_scripts.html**

.. code:: html+django

    {% extends "adminlte2/partials/_scripts.html" %}

    {% block scripts_prod %}
      {% include "adminlte2/partials/_scripts/_scripts_debug.html" %}
    {% endblock scripts_prod %}
