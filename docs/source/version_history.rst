Version History
***************


0.2.0 - Internal Auth Logic Rework
==================================

* Overhaul of existing auth logic to be more consistent and reliable.

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
