Front End Styling Configuration
*******************************

This package contains all of the AdminLTE2 default styles, and then some.
For example, AdminLTE2 provides some reusable HTML elements with color themes that
are inconsistently supported across elements.

This package fixes the color themes to work uniformly across all elements, and
even adds a few additional color options.

All settings on this page relate to said front end elements and color options.


CSS_COLORS_DICT
---------------

All implemented front-end elements are displayed in the :doc:`../demo_css` page.

You can modify this dictionary if you wish to change which values appear
on said demo css page. Such as to remove unwanted colors, or add new custom colors.

Note that to add custom colors, you will also need to add appropriate CSS files.
This setting only modifies package logic on the demo css pages, to check for CSS
files with a name that matches the value listed here.

See package files at ``static/adminlte2_pdq/css/extra-colors/``
for implementation examples.


:Type: ``dict``
:Default: {
            "default": "#f4f4f4",
            "primary": "#3c8dbc",
            "info": "#00c0ef",
            "success": "#00a65a",
            "warning": "#f39c12",
            "danger": "#dd4b39",
            "navy": "#001f3f",
            "blue": "#1a94db",
            "teal": "#39cccc",
            "olive": "#3d9970",
            "lime": "#01ff70",
            "orange": "#ff851b",
            "fuchsia": "#f012be",
            "indigo": "#a35cd8",
            "purple": "#605ca8",
            "maroon": "#d81b60",
            "gray": "#d2d6de",
            "black": "#2b2b2b",
        }

Example::

    CSS_COLORS_DICT = {
        "color_name_1": "#ABABAB",
        "color_name_2": "#AABBCC",
        "color_name_3": "#ABCABC",
    }
