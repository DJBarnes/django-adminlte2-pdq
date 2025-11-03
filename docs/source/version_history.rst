Version History
***************

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
