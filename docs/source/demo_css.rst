Demo CSS
********

The package includes a set of demo pages that show AdminLTE's elements and the
package's extra CSS. Inspect an element in your browser to see which classes
produce a given style.

With the package's routes included in your project:

.. code:: python

    path('', include('adminlte2_pdq.urls')),

the demo pages are at ``<domain>/demo-css/``. The demo pages have their own sidebar
menu, which links to each page: typography, widgets, general UI and the color palette, alerts, basic and
specialized buttons, carousels, labels and tooltips, modals, full-span links,
standard and solid boxes, tables, and forms.

The demo pages work under every policy: for everyone under the loose policy,
and for every logged-in user under the login required and strict policies, as
the home page does. They are in the default strict policy whitelist (see
:ref:`authorization/policies:strict policy`).

To change which colors the demo pages show, see
:ref:`configuration/front_end_styling:ADMINLTE2_DEMO_CSS_COLORS`.


Colors
======

The package supports these colors on every element:

``default``, ``primary``, ``info``, ``success``, ``warning``, ``danger``,
``navy``, ``blue``, ``teal``, ``olive``, ``lime``, ``orange``, ``fuchsia``,
``purple``, ``maroon``, ``black``, ``gray``, and ``indigo``.

These names are equivalent:

* ``primary`` and ``light-blue``
* ``info`` and ``aqua``
* ``success`` and ``green``
* ``warning`` and ``yellow``
* ``danger``, ``red``, and ``error``

Every color except ``default``, ``error``, and ``indigo`` is AdminLTE's, with
AdminLTE's values. Text on ``lime``, ``gray``, and ``default`` is dark.

.. note::

    For background classes, use AdminLTE's names: ``bg-light-blue``,
    ``bg-aqua``, ``bg-green``, ``bg-yellow``, and ``bg-red``. Bootstrap defines
    ``bg-primary``, ``bg-info``, ``bg-success``, ``bg-warning``, and
    ``bg-danger`` as pale tints, and the package leaves them unchanged.


Color classes
-------------

AdminLTE colors some elements only for some colors. The package adds the
missing classes, so each element below works with every color. Replace
``{color}`` with a color name.

=========================  ==================================================
Element                    Classes
=========================  ==================================================
Background                 ``bg-{color}``, ``bg-{color}-active``
Text                       ``text-{color}``
Code                       ``<code class="code-{color}">`` (pale tint)
Alert                      ``alert alert-{color}``
Box                        ``box box-{color}``, ``box box-solid box-{color}``
Button                     ``btn btn-{color}``
Callout                    ``callout callout-{color}``
Carousel                   ``carousel carousel-{color}`` (controls, caption,
                           and indicators)
Dropdown menu              ``dropdown-menu dropdown-menu-{color}``
Label                      ``label label-{color}``
Modal                      ``modal modal-{color}``
Table row or cell          ``<tr class="{color}">``, ``<td class="{color}">``
Bordered table             ``table table-bordered table-border-{color}``
Tooltip                    ``tooltip-{color}`` class or
                           ``data-tooltip-color="{color}"`` attribute on the
                           element that has the tooltip
=========================  ==================================================

Classes that AdminLTE or Bootstrap already define, such as ``btn-primary``,
``label-danger``, and ``bg-maroon``, look the same as with AdminLTE alone, in
every state (hover, focus, pressed, and disabled). They use the package's color
variables too, so changing a color changes every class of that color (see
:ref:`demo_css:Changing a color`).

Some of these classes keep shades that differ from the rest of their color,
because AdminLTE and Bootstrap draw them differently:

* Bootstrap's ``bg-primary``, ``bg-info``, ``bg-success``, ``bg-warning``, and
  ``bg-danger`` are pale tints (``bg-primary`` is a darker blue), and its
  ``text-{color}`` classes for the same colors are darker shades. AdminLTE's
  names for these colors, such as ``bg-aqua`` and ``text-red``, are the color
  itself.
* Table rows and cells with Bootstrap's ``success``, ``info``, ``warning``,
  and ``danger`` classes are a pale tint, header and footer rows included. For
  every other color, header and footer rows take the color itself.
* AdminLTE only replaces a Bootstrap button's normal and hover colors. Its
  focus, pressed, and disabled states and its badge keep Bootstrap's shades.
* AdminLTE's default box and label are a darker gray than its default button.
* The package's own ``bg-{color}`` classes also color the border, which shows
  on app buttons (``btn-app``). AdminLTE's ``bg-{color}`` classes don't.

To draw all of these except the borders in their color's AdminLTE shades, so
that each color name is one color everywhere, set
:ref:`configuration/front_end_styling:ADMINLTE2_CONSISTENT_COLORS` to True.


Changing a color
----------------

Each color is a set of CSS custom properties, defined in
``adminlte2_pdq/css/extra-colors/color-variables.css``:

====================================  =====================================
Property                              Used for
====================================  =====================================
``--pdq-{color}-base``                Main color
``--pdq-{color}-text``                Text on the main color
``--pdq-{color}-active``              ``bg-{color}-active``, modal headers
                                      and footers
``--pdq-{color}-hover``               Button hover and borders, alert
                                      borders
``--pdq-{color}-border``              Callout and modal borders
``--pdq-{color}-light-accent``        Code tint and table body rows
``--pdq-{color}-light-accent-text``   Text on the light accent
``--pdq-{color}-table-hover``         Table row hover
====================================  =====================================

Bootstrap's colors (``default``, ``primary``, ``info``, ``success``,
``warning``, and ``danger``) have more properties, for the classes that keep
Bootstrap's shades:

============================================  ================================
Property                                      Used for
============================================  ================================
``--pdq-{color}-bootstrap-btn``               Button badge, disabled button on
                                              hover
``--pdq-{color}-bootstrap-btn-border``        Disabled button border on hover
``--pdq-{color}-bootstrap-btn-text``          Button text (for ``default``, only
                                              when focused, hovered, or pressed)
``--pdq-{color}-bootstrap-btn-hover``         Focused or ``.active`` button
``--pdq-{color}-bootstrap-btn-hover-border``  Button border on hover and when
                                              pressed
``--pdq-{color}-bootstrap-btn-focus-border``  Focused button border
``--pdq-{color}-bootstrap-btn-pressed``       Button pressed while focused or
                                              hovered
``--pdq-{color}-bootstrap-bg``                ``bg-{color}`` (not ``default``)
``--pdq-{color}-bootstrap-bg-hover``          Linked ``bg-{color}`` on hover
``--pdq-{color}-bootstrap-text``              ``text-{color}`` (not
                                              ``default``)
``--pdq-{color}-bootstrap-text-hover``        Linked ``text-{color}`` on hover
``--pdq-default-box-label``                   Default box and label
============================================  ================================

To change a color, generate new values for all of its properties with the
``generate_color_css`` management command, and load the file after the
package's CSS (see :ref:`demo_css:Generating a color`):

.. code:: bash

    python manage.py generate_color_css light-blue '#87ceeb'

The file sets every property of the color, including the Bootstrap shades,
which follow the new color: its buttons use the new color in every state, its
``bg-{color}`` is a pale tint of it, and its ``text-{color}`` a darker shade.
Each property is a separate value, so redefining only ``--pdq-{color}-base``
by hand leaves the other shades as they were.

To go back to the package's color, delete the file, or stop loading it.

The alternate names ``light-blue``, ``aqua``, ``green``, ``yellow``, ``red``,
and ``error`` use the properties of ``primary``, ``info``, ``success``,
``warning``, and ``danger``, so changing ``info`` also changes ``aqua``. To
change only ``aqua``, generate values for ``aqua``.


Adding a color
--------------

To add a color, generate its CSS with the ``generate_color_css`` management
command, and load the file after the package's CSS (see
:ref:`demo_css:Generating a color`):

.. code:: bash

    python manage.py generate_color_css brand '#6610f2'

The file has the color's properties and every color class for ``brand``.

To show the new color on the demo pages, add it to
:ref:`configuration/front_end_styling:ADMINLTE2_DEMO_CSS_COLORS`.


Generating a color
------------------

.. code:: bash

    python manage.py generate_color_css NAME BASE [options]

``NAME`` is the color's name: lowercase letters, digits, and hyphens,
starting with a letter. A package color's name, such as ``info`` or
``light-blue``, gives that color new values. Any other name adds a color.
``BASE`` is the color itself, as a hex value, such as ``'#6610f2'``. Every
other shade is derived from it.

Options:

* ``--active '#5b0cdd'``: the darker shade for ``bg-{color}-active`` and modal
  headers. Defaults to the base color darkened by 5%.
* ``--dark-text`` or ``--light-text``: dark or white text on the color.
  Defaults to whichever is easier to read.
* ``--output PATH``: the file to write. Defaults to ``css/colors/NAME.css`` in
  the first ``STATICFILES_DIRS`` directory, or ``NAME.css`` in the current
  directory when ``STATICFILES_DIRS`` is empty.
* ``--force``: replace the file if it exists. Otherwise the command asks
  first.

After writing the file, the command prints how to load it. Load it after the
package's colors, in the ``styles_main_fixes__extra_colors`` block, by adding
``adminlte2/partials/_styles.html`` to your project's templates:

.. code:: html+django

    {% extends "adminlte2/partials/_styles.html" %}
    {% load static %}

    {% block styles_main_fixes__extra_colors %}
      {{ block.super }}
      <link rel="stylesheet" href="{% static 'css/colors/brand.css' %}">
    {% endblock styles_main_fixes__extra_colors %}


Other classes
=============

Full-span links
---------------

An ``<a>`` tag with the ``full-span-link`` class covers its parent element,
which makes the whole element clickable. Supported parents are alerts,
callouts, info boxes, small boxes, state widgets, and table cells. Other
parents need ``position: relative``.

.. code:: html

    <div class="small-box bg-aqua">
        <a href="/reports/" class="full-span-link"></a>
        <div class="inner"><h3>150</h3><p>Reports</p></div>
    </div>


Utility classes
---------------

==============================  ===============================================
Class                           Effect
==============================  ===============================================
``pdq-flex``                    ``display: flex``
``pdq-flex-row``                Flex container, row direction
``pdq-flex-column``             Flex container, column direction
``pdq-flex-center``             Centers flex items on both axes
``pdq-flex-wrap``               Wraps flex items
``pdq-flex-grow``               The element grows to fill the space
``pdq-flex-grow-children``      Every child grows to fill the space
``pdq-underline``               Underlined text
``pdq-no-underline``            No underline
``pdq-clear-border``            Transparent border that keeps its width
``pdq-clear-background``        Transparent background
``wiggle``                      Repeating wiggle animation (off for users who
                                prefer reduced motion)
==============================  ===============================================

AdminLTE's own ``no-border`` class removes a border entirely.
