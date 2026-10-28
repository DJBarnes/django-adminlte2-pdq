Version History
***************

Unreleased
==========

* Extra color classes are now generated from one palette and cover every
  AdminLTE color plus ``default``, ``error``, and ``indigo``: backgrounds
  (``bg-{color}``, ``bg-{color}-active``), text, code tints
  (``code-{color}``), alerts, boxes, buttons, callouts, carousels
  (``carousel-{color}``), dropdown menus (``dropdown-menu-{color}``), labels,
  modals, table rows and cells, bordered tables (``table-border-{color}``),
  and tooltips (``tooltip-{color}``). Classes that AdminLTE or Bootstrap
  already define are not changed, except table header and footer rows.

* Table header and footer rows (``thead``, ``tfoot``) with Bootstrap's
  ``success``, ``info``, ``warning``, or ``danger`` classes now take the color
  itself, as the package's other colors do, instead of Bootstrap's pale tint.
  Body rows keep Bootstrap's colors.

* Colors are CSS custom properties named ``--pdq-{color}-{part}``, defined in
  ``adminlte2_pdq/css/extra-colors/color-variables.css``. Redefine them in
  your own CSS to change a color.

* Add dark mode: dark versions of the AdminLTE skins, ``skin-blue-dark``,
  ``skin-black-dark``, ``skin-purple-dark``, ``skin-yellow-dark``,
  ``skin-red-dark``, and ``skin-green-dark``. The dark mode CSS is always
  loaded and only applies under a dark skin class, so a page can switch modes
  by changing the body's skin class.

* **The site now follows the browser's light or dark mode by default.** Users
  whose browser or operating system is set to dark mode see the dark version
  of the site's skin. Light mode is unchanged. Set
  ``ADMINLTE2_SKIN_FOLLOW_BROWSER = False`` to always use
  ``ADMINLTE2_SKIN_CLASS``. ``ADMINLTE2_SKIN_CLASS_LIGHT`` and
  ``ADMINLTE2_SKIN_CLASS_DARK`` choose the skins used in each mode. The
  script that follows the browser loads in the new ``skin_follow_browser``
  block of ``adminlte2/base.html``.

* Add ``python -m adminlte2_pdq.color_css --custom NAME BASE``, which prints
  the CSS for a project's own color: its custom properties and every color
  class.

* Existing extra color classes now use AdminLTE's color values:

  * ``*-black``: ``#2b2b2b`` is now ``#111`` (AdminLTE's ``bg-black``).
  * ``*-gray``: ``#b5bbc8`` is now ``#d2d6de`` with ``#000`` text
    (AdminLTE's ``bg-gray``).
  * ``alert-default``, ``callout-default``, and ``tooltip-default`` use the
    ``btn-default`` grey, ``#f4f4f4``.
  * ``alert-primary``, ``callout-primary``, and ``tooltip-primary``:
    ``#337ab7`` is now ``#3c8dbc`` (AdminLTE's primary).
  * Table row, cell, and code tints are computed from each color and keep
    part of its lightness and saturation, so colors that share a hue (navy,
    blue, and primary) stay apart. ``success``, ``info``, ``warning``, and
    ``danger`` use Bootstrap's own pale tints. Header and footer cells use the
    solid color. Text on code tints is ``#444``.
  * Button hover colors and callout and modal border colors for the extra
    colors follow AdminLTE's convention (5% and 10% darker).
  * Text on lime is ``#444``.

* Lime backgrounds (``bg-lime``) use dark text instead of white.

* Tooltip colors now work on any element with a ``tooltip-{color}`` class or
  a ``data-tooltip-color`` attribute. Previously they did not apply, because
  AdminLTE creates tooltips inside ``<body>``.

* Add utility classes ``pdq-flex``, ``pdq-flex-row``, ``pdq-flex-column``,
  ``pdq-flex-center``, ``pdq-flex-wrap``, ``pdq-flex-grow``,
  ``pdq-flex-grow-children``, ``pdq-underline``, ``pdq-no-underline``,
  ``pdq-clear-border``, and ``pdq-clear-background``.

* Add ``full-span-link``: an ``<a>`` tag with this class covers its parent
  alert, callout, info box, small box, state widget, or table cell, making the
  whole element clickable.

* The ``wiggle`` animation is turned off for users who prefer reduced motion.

* Static files moved into ``css/`` and ``js/`` folders under
  ``adminlte2_pdq/``. The old paths still work and are deprecated:

  * ``extra-features/extra-features.css``: now
    ``css/extra-colors/color-variables.css``,
    ``css/extra-colors/extra-colors.css``, and
    ``css/extra-features/extra-features.css``.
  * ``extra-features/header-breadcrumb-overlap-fix.css``: now part of
    ``css/extra-features/extra-features.css``.
  * ``extra-features/extra-features.js``,
    ``extra-features/header-breadcrumb-overlap-fix.js``, and
    ``extra-features/sidebar-state.js``: now in ``js/extra-features/``.
  * ``conflicts/conflicts.css`` and ``conflicts/conflicts.js``: now
    ``css/conflicts/conflicts.css`` and ``js/conflicts/conflicts.js``.
  * ``conflicts/django-admin-conflicts.css``: now
    ``css/conflicts/django_admin_conflicts.css``.

* The demo CSS page is now a set of pages under ``/demo-css/``: typography,
  widgets, general UI and color palette, alerts, basic and specialized
  buttons, carousels, labels and tooltips, modals, full-span links, standard
  and solid boxes, tables, and forms. The demo pages have their own sidebar
  menu. Its Profile and Samples sections appear only when their routes are
  registered.

* Add the ``ADMINLTE2_DEMO_CSS_COLORS`` setting: the colors shown on the demo
  CSS pages, as ``{name: hex value}``.

* The ``adminlte2/demo_css.html`` template is deprecated. It now extends
  ``adminlte2_demo_css/home.html``.

* The first item of the default sidebar menu is now labeled "Dashboard"
  instead of "Home".

* ``adminlte2_pdq.views`` is now a package. Views are still importable from
  ``adminlte2_pdq.views``.

* The ``styles_main_fixes`` template block contains four new blocks:
  ``styles_main_fixes__color_variables``,
  ``styles_main_fixes__extra_colors``,
  ``styles_main_fixes__extra_features``, and
  ``styles_main_fixes__dark_mode``.

* Add the ``ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST`` setting. Paths
  that start with an entry in this list raise ``PermissionDenied`` on a failed
  permission check instead of redirecting to the home page.

* Setting ``ADMINLTE2_REDIRECT_TO_HOME_ON_403`` to ``False`` now turns off the
  redirect to the home page for both the middleware and the
  ``PermissionRequiredMixin``. Views without a permission decorator or mixin
  raise ``PermissionDenied``.

* The login redirect now keeps the query string of the requested page in the
  ``next`` parameter, URL-encodes it, and supports a URL name in
  ``LOGIN_URL``.

* Fix the sidebar menu growing on every request when
  ``ADMINLTE2_MENU_FIRST`` is provided through view context.

* Fix a ``KeyError`` when a sidebar tree contains a nested tree without a
  ``route``.

* Fix sidebar nodes being marked active when they should not be.

* Fix ``ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST`` matching only exact
  paths instead of path prefixes.

* Fix the 403 production message being shown twice in strict mode for views
  without a decorator.

* Under the login-required and strict policies, an anonymous user who
  requests an unknown URL is now sent to the login page, the same as for a
  page that exists, instead of to the home page and then the login page. The
  response no longer shows which URLs exist, and the 404 message no longer
  appears on the login page. This also applies when
  ``ADMINLTE2_REDIRECT_TO_HOME_ON_404`` is ``False``.

* In production, a view that requires permissions but defines none no longer
  causes a server error (500). The middleware logs the problem at the
  ``ERROR`` level on the ``adminlte2_pdq.middleware`` logger, and the user
  gets the same response as for any page they can't access: the login page
  when not logged in, otherwise the 403 handling.

* The package's route settings now use the ``ADMINLTE2_`` prefix:
  ``ADMINLTE2_LOGOUT_URL``, ``ADMINLTE2_PASSWORD_RESET_ROUTE``,
  ``ADMINLTE2_PASSWORD_RESET_DONE_ROUTE``,
  ``ADMINLTE2_PASSWORD_RESET_CONFIRM_ROUTE``,
  ``ADMINLTE2_PASSWORD_RESET_COMPLETE_ROUTE``, ``ADMINLTE2_REGISTER_ROUTE``,
  ``ADMINLTE2_PASSWORD_CHANGE_ROUTE``, ``ADMINLTE2_PASSWORD_CHANGE_DONE_ROUTE``,
  and ``ADMINLTE2_WEBSOCKET_URL``. The old names (``LOGOUT_URL``,
  ``PWD_RESET_ROUTE``, ``REGISTER_ROUTE``, ``PWD_CHANGE``, ``WEBSOCKET_URL``,
  and so on) still work with a deprecation warning and will be removed in a
  future release.

* Documentation: new pages for styling and dark mode, the demo CSS classes,
  and the known route settings. Every authorization setting is now listed in
  the authorization configuration page.

0.2.1 - Filters, Commands, Messages, 404s, and Tree Nodes
=========================================================

* Add New Template filters

  * ``dict_get`` which allows getting a dict value by key where the key can be
    a variable vs the literal key. Defaults to None if not found.

  * ``multiply`` which allows for multiplying two numbers together.

  * ``divide`` which allows for dividing the first number by the second.

  * ``modulo`` which allows for remainder after dividing the first number by the
    second.

* Update and fix bugs in management commands

  * Update the ``showperms`` command to:

    * Optionally show the **has_perm** text that should be used when testing if a
      user has permissions.

    * Optionally hide the default Django permissions from the output.

  * Update the ``showroutes`` command to allow hiding all admin routes.

  * Fix some bugs that prevented some of the commands from working correctly.

* Update how messages are displayed

  * Breaking Change - The colors for the Info and Debug level messages have
    been swapped. Info is now dark blue and Debug is light blue. This aligns
    better with what users will expect to see.

  * The colors to use for each message are now fully configurable via
    overriding the ``_messages.html`` partial template and changing the class
    to use for each message type.

* Update how 404s work

  * There is a new Whitelist that can be used to whitelist url patterns that
    should return a 404 instead of redirecting to the home page. This is useful
    for non-view endpoints like static files which should just be a 404.

  * Update the default message for 403 and 404s to be a little more vague.
    Detailed messages still exist in the logging and during debugging.

* Add ability to add links for root tree nodes.

  * When this is done, the text is a clickable link and the caret is the
    part that will handle the expansion and collapse of the tree node.

  * If there is no link for the root tree node, then the entire text and
    caret will control the expansion and collapse of the tree node.

* Refactor the main middleware to read better and be organized in a consistent
  way.

* Pylint and Testing Improvements

  * Fix many pylint errors including changing many uses of ``.format`` to
    f-strings.

  * Improve testing to handle testing majority of possible edge cases.

  * Testing now has 100% code coverage

* Update base CSS and JS packages including adminlte2.

* General smaller bugfixes, such as for trailing slashes.


0.2.0 - Internal Auth Logic Rework
==================================

* Overhaul of existing auth logic to be more consistent and reliable.

  * Add support for Django 5.0, 5.1, and 5.2.

  * Middleware, decorator, and mixin logic have been reworked to better align
    with the intended functionality while remaining 100% backward compatible.

  * Testing has been improved to better catch edge cases and ensure full
    alignment with the intended functionality.

* Created project warnings/errors for authentication instances that don't make
  sense.

  * For example, the ``login_required`` decorator will raise a warning when
    used on a view that is login whitelisted. Because functionality is
    effectively being duplicated.

* Two new decorators:

  * ``allow_anonymous_access`` - Usable in STRICT or LOGIN_REQUIRED
    authentication modes, allows a given view to be accessible by any user.
    This state was previously only achievable with whitelists.

  * ``allow_without_permissions`` - Usable in STRICT authentication mode,
    allows a given view to be accessible by any users that are logged in,
    regardless of the permissions they have. This state was previously only
    achievable with whitelists.

* Two new mixins to match above decorators:

  * ``AllowAnonymousAccess`` - Handles the same as the
    ``allow_anonymous_access`` decorator.

  * ``AllowWithoutPermissions`` - Handles the same as the
    ``allow_without_permissions`` decorator.

* General smaller bugfixes, such as for sidebar logic.


0.1.7 - Bugfixes & Quality of Life
==================================

* Updated some templates to allow better control of block tag overriding.

* Several bugfixes, particularly with handling of forms and formsets.


0.1.6 - Bugfix for Default Route Handling in Strict Mode
========================================================

* Correct bug where password change routes were not exempt by default in
  STRICT mode.


0.1.5 - Auth Mode Bugfixes
==========================

* Several bugfixes related to incorrect logic when in LOGIN_REQUIRED or STRICT
  modes.


0.1.4 - Datetime Widget Settings
================================

* Add support for new settings that change what widget is used when
  auto-rendering forms with date, time, and datetime fields.


0.1.3 - Fix Potential Django Front End Conflicts & Add Middleware Auth Hook
===========================================================================

* Fix potential CSS conflicts with Django Admin css.

* Correct block usage naming conventions.

* Add auth hook to middleware handling, to allow for custom methods of
  authenticating users for view access, on a per-site basis.


0.1.2 - Bugfix for Strict Mode Being Too Strict
===============================================

* Fix bug where middleware would unconditionally deny all admin pages.
