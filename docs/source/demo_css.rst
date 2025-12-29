Demo CSS
********

This package provides a set of Demo CSS pages that demonstrate some of the
features of this package, and the css classes that can be applied to
various elements to style them.

Assuming you are including the default routes that come with this package

.. code:: python

    path('', include('adminlte2_pdq.urls')),

You can go to ``<domain>/demo-css`` to see the css demo homepage.
From there you can select various subpages, and then inspect any element
using your favorite browser to see which classes are required to replicate
the styling.


Additional CSS Features
=======================

AdminLTE PDQ provides various color stylings, largely using the colors
provided in the original AdminLte package.

However, PDQ provides a few points that the original does not:

* PDQ supports all available widgets in all supported colors.
  The original AdminLte largely only supported the "basic colors" (primary,
  info, success, warning, and debug) across all widgets, despite also
  providing additional colors that were inconsistently supported.

* Within the "demo css" pages, PDQ shows all widgets in all supported colors,
  both for debugging purposes, and so that the end-user can see exactly how
  all widgets will look.

* PDQ supports easily adding additional theme colors (or replacing existing
  ones). For details, see the example files provided under
  `adminlte2_pdq/static/adminlte2_pdq/css/extra-colors`.
