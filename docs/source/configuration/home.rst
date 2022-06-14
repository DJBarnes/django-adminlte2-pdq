Home Configuration
******************

There are various configuration options that can be set via Django Settings to
control the overall look, feel, and functionality of the package.
All settings are listed here for reference even though some of these settings
such as the :doc:`../menu/general_information` and
:doc:`../authorization` can become quite complex and have dedicated
documentation pages to better explain the full extent of these settings.


----


Base Configuration
==================

ADMINLTE2_HOME_ROUTE
--------------------

Set the "Home" route for you project so that the package knows
where to redirect users when they click a link that is designed
to take the user home.

:Type: ``string``
:Default: ``django_adminlte_2:home``

Example::

    ADMINLTE2_HOME_ROUTE = 'django_adminlte_2:home'


----


Logo & Skin Color Configuration
===============================

ADMINLTE2_LOGO_TEXT
-------------------

Set the Logo text for your site that will be shown in the top left of the top
bar.

.. note::

    If you would like to include html in your text, you will need to import
    and use ``mark_safe`` from ``django.utils.safestring``. Otherwise, your
    html will be escaped.

:Type: ``string``
:Default: ``AdminLTE``

Example::

    ADMINLTE2_LOGO_TEXT = 'My Awesome Site'


ADMINLTE2_LOGO_TEXT_SMALL
-------------------------

Set the small Logo text for your site that will be shown in the top left of the
top bar when the side bar is collapsed.

.. note::

    If you would like to include html in your text, you will need to import
    and use ``mark_safe`` from ``django.utils.safestring``. Otherwise, your
    html will be escaped.

:Type: ``string``
:Default: ``ALTE``

Example::

    ADMINLTE2_LOGO_TEXT = 'MAS'


ADMINLTE2_SKIN_CLASS
--------------------

Set the skin class to use for the site. Valid skin classes can be found on the
`AdminLTE documentation <https://adminlte.io/themes/AdminLTE/documentation/>`_
page.

:Type: ``string``
:Default: ``skin-blue``

Example::

    ADMINLTE2_SKIN_CLASS = 'skin-green-light'

