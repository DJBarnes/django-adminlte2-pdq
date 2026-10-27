Demo CSS
********

The package includes a set of demo pages that show AdminLTE's elements and the
package's extra CSS. Inspect an element in your browser to see which classes
produce a given style.

With the package's routes included in your project:

.. code:: python

    path('', include('adminlte2_pdq.urls')),

the demo pages are at ``<domain>/demo-css/``. The demo home page links to each
page: typography, widgets, general UI and the color palette, alerts, basic and
specialized buttons, carousels, labels and tooltips, modals, full-span links,
standard and solid boxes, tables, and forms.

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

Classes that AdminLTE or Bootstrap already define keep their stock look. For
example, ``btn-primary`` and ``label-danger`` are unchanged, and table
rows with Bootstrap's ``success``, ``info``, ``warning``, and ``danger``
classes keep Bootstrap's colors.


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
``--pdq-{color}-hover``               Button hover and borders, alert
                                      borders
``--pdq-{color}-border``              Callout and modal borders
``--pdq-{color}-light-accent``        Code tint and table body rows
``--pdq-{color}-light-accent-text``   Text on the light accent
``--pdq-{color}-table-hover``         Table row hover
====================================  =====================================

To change a color, redefine its properties in a stylesheet that loads after
the package's CSS. For example:

.. code:: css

    :root {
        --pdq-indigo-base: #6610f2;
        --pdq-indigo-active: #5b0cdd;
    }


Adding a color
--------------

To add a color, generate its CSS and load the result after the package's CSS:

.. code:: bash

    python -m adminlte2_pdq.color_css --custom brand '#6610f2' > static/css/brand.css

This prints the custom properties and every color class for ``brand``. Options:

* ``--active '#5b0cdd'``: the darker shade for ``bg-brand-active`` and modal
  headers. Defaults to the base color darkened by 5%.
* ``--dark-text``: use dark text instead of white, for light colors.

To show the new color on the demo pages, add it to
:ref:`configuration/front_end_styling:ADMINLTE2_DEMO_CSS_COLORS`.


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
