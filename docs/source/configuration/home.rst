Home Configuration
******************

`Django settings <https://docs.djangoproject.com/en/dev/topics/settings/>`_ can
be used to customize and control the overall look, feel, and functionality of
the **Django-AdminLTE2-PDQ** package.

All settings are listed here for reference, even though some of these settings
(such as the :doc:`../menu/general_information` and
:doc:`Authorization <../authorization/policies>`) can become quite complex,
to the point that they have dedicated documentation pages to better explain
the full extent of these settings.


----


Base Configuration
==================

ADMINLTE2_HOME_ROUTE
--------------------

Set the "Home" route for your project. This tells the package where to redirect
users when they click a link that is designed to take the user home.

For additional routes defined in settings, see :doc:`./known_routes`.

:Type: ``string``
:Default: ``adminlte2_pdq:home``

Example::

    ADMINLTE2_HOME_ROUTE = 'adminlte2_pdq:home'


----


Logo & Skin Color Configuration
===============================

ADMINLTE2_LOGO_TEXT
-------------------

Set the Logo text for your site. This will be shown in the top left of the top
bar, when the sidebar is expanded.

.. note::

    If you would like to include HTML in your text, you will need to import
    and use ``mark_safe`` from ``django.utils.safestring``. Otherwise, your
    HTML will be escaped.

:Type: ``string``
:Default: ``AdminLTE``

Example::

    ADMINLTE2_LOGO_TEXT = 'My Awesome Site'


ADMINLTE2_LOGO_TEXT_SMALL
-------------------------

Set the small Logo text for your site. This will be shown in the top left of the
top bar, when the sidebar is collapsed.

.. note::

    If you would like to include HTML in your text, you will need to import
    and use ``mark_safe`` from ``django.utils.safestring``. Otherwise, your
    HTML will be escaped.

:Type: ``string``
:Default: ``ALTE``

Example::

    ADMINLTE2_LOGO_TEXT_SMALL = 'MAS'


ADMINLTE2_SKIN_CLASS
--------------------

Set the skin class to use for the site. Valid skin classes can be found on the
`AdminLTE documentation <https://adminlte.io/themes/AdminLTE/documentation/>`_
page.

The package adds a dark version of each AdminLTE skin color:
``skin-blue-dark``, ``skin-black-dark``, ``skin-purple-dark``,
``skin-yellow-dark``, ``skin-red-dark``, and ``skin-green-dark``.

By default the site follows the browser's light or dark mode, and this setting
is the starting point for the light and dark skins. It is used as-is when
browser following is off. See :ref:`configuration/front_end_styling:Dark Mode`.

:Type: ``string``
:Default: ``skin-blue``

Example::

    ADMINLTE2_SKIN_CLASS = 'skin-green-light'


ADMINLTE2_SKIN_FOLLOW_BROWSER
-----------------------------

Whether the site follows the browser's light or dark mode setting. When
``True``, a script that runs before the page is drawn replaces the skin class
with :ref:`configuration/home:ADMINLTE2_SKIN_CLASS_LIGHT` or
:ref:`configuration/home:ADMINLTE2_SKIN_CLASS_DARK`. When
``False``, the site always uses :ref:`configuration/home:ADMINLTE2_SKIN_CLASS`.

:ref:`configuration/home:ADMINLTE2_SKIN_CLASS` is also used when the browser
has JavaScript turned off.

:Type: ``bool``
:Default: ``True``

Example::

    ADMINLTE2_SKIN_FOLLOW_BROWSER = False


ADMINLTE2_SKIN_CLASS_LIGHT
--------------------------

The skin class to use when following the browser and the browser is in light
mode. The value is used as given, so it can be any skin class.

:Type: ``string``
:Default: :ref:`configuration/home:ADMINLTE2_SKIN_CLASS`, or its ``-light``
    version when that is a dark skin (``skin-blue-dark`` becomes
    ``skin-blue-light``)

Example::

    ADMINLTE2_SKIN_CLASS_LIGHT = 'skin-blue-light'


ADMINLTE2_SKIN_CLASS_DARK
-------------------------

The skin class to use when following the browser and the browser is in dark
mode. The value is used as given, so it can be any skin class.

:Type: ``string``
:Default: the ``-dark`` version of the
    :ref:`configuration/home:ADMINLTE2_SKIN_CLASS` color (``skin-blue``
    becomes ``skin-blue-dark``)

Example::

    ADMINLTE2_SKIN_CLASS_DARK = 'skin-purple-dark'

