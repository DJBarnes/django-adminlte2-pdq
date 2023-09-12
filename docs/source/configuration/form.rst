Form and Field Configuration
============================

ADMINLTE2_DATETIME_WIDGET
-------------------------

Set the DateTime widget to use with rendering out a DateTime form field.
By default, this will be ``native`` which will just use the HTML5 native widgets.
Additionally, you can use ``jquery`` to use the JS jquery-datetimepicker.js library.

.. note::

    This setting only affects how the form field is rendered out.
    For ``native`` this means changing the input type to ``datetime-local``.
    For the other option, this means keeping its type ``text`` but adding an
    icon to indicate that it should be a datetime field.
    Aside from loading the needed JS library, it does not add any additional JS
    to make the chosen library work. That is left up to you.

:Type: ``string``
:Default: ``native``

Example::

    ADMINLTE2_DATETIME_WIDGET = 'jquery'


ADMINLTE2_DATE_WIDGET
-------------------------

Set the Date widget to use with rendering out a Date form field.
By default, this will be ``native`` which will just use the HTML5 native widgets.
Additionally, you can use either ``bootstrap`` or ``jquery`` to use either the
JS bootstrap-datepicker.js library or the jquery-datetimepicker.js library.

.. note::

    This setting only affects how the form field is rendered out.
    For ``native`` this means changing the input type to ``date``.
    For the other options, this means keeping its type ``text`` but adding an
    icon to indicate that it should be a date field.
    Aside from loading the needed JS library, it does not add any additional JS
    to make the chosen library work. That is left up to you.

:Type: ``string``
:Default: ``native``

Example::

    ADMINLTE2_DATE_WIDGET = 'jquery'


ADMINLTE2_TIME_WIDGET
-------------------------

Set the Time widget to use with rendering out a Time form field.
By default, this will be ``native`` which will just use the HTML5 native widgets.
Additionally, you can use ``jquery`` to use the JS jquery-datetimepicker.js library.

.. note::

    This setting only affects how the form field is rendered out.
    For ``native`` this means changing the input type to ``time``.
    For the other option, this means keeping its type ``text`` but adding an
    icon to indicate that it should be a time field.
    Aside from loading the needed JS library, it does not add any additional JS
    to make the chosen library work. That is left up to you.

:Type: ``string``
:Default: ``native``

Example::

    ADMINLTE2_TIME_WIDGET = 'jquery'

ADMINLTE2_BOLD_REQUIRED_FIELDS
------------------------------

Set whether required fields on a form should render out with bolded labels to
denote that the field is required when using any of the template tags that
help render out forms.

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_BOLD_REQUIRED_FIELDS = False

ADMINLTE2_ASTERISK_REQUIRED_FIELDS
----------------------------------

Set whether required fields on a form should render out an asterisk next to the
labels for a form field to denote that the field is required when using any of
the template tags that help render out forms.

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_ASTERISK_REQUIRED_FIELDS = False
