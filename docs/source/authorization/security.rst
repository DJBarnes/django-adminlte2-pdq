Security
********

This page explains what the package's authentication and authorization
protect, and what they don't. See :doc:`policies` for how to set them up.


The Middleware Protects Views, the Sidebar Only Hides Links
===========================================================

``adminlte2_pdq.middleware.AuthMiddleware`` decides who can open each view.
The sidebar menu shows or hides links with the same rules, so users don't see
links they can't open, but hiding a link doesn't protect its page: anyone can
type the URL.

* The login required and strict policies, and the whitelists, only work with
  the middleware installed. Without it, the decorators and mixins still check
  login and permissions on the views that use them, the same as Django's own,
  but every other view is public.
* The ``permissions``, ``one_of_permissions``, and ``login_required`` keys on
  a menu node only hide that link. Set permissions on the view instead (see
  :doc:`function_views` and :doc:`class_views`).


Each Policy's Default
=====================

* :ref:`authorization/policies:loose policy` (the default): every view is
  public unless its decorator or mixin requires login or permissions.
* :ref:`authorization/policies:login required`: every view requires login,
  unless its route is in a login whitelist or its view uses
  ``allow_anonymous_access``.
* :ref:`authorization/policies:strict policy`: every view requires login and
  defined permissions, unless it is whitelisted or uses one of the ``allow_*``
  decorators or mixins. A view that requires permissions but defines none
  can't be opened by anyone, superusers included, and the
  ``adminlte2_pdq.W001`` system check lists it.

Superusers pass every permission check of a view that defines permissions, and
see every sidebar link.


Whitelists Skip the Checks
==========================

A route in a whitelist skips the matching check for everyone:

* ``ADMINLTE2_LOGIN_EXEMPT_WHITELIST`` and
  ``ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST`` skip the login check, so the page
  is public under the login required policy.
* ``ADMINLTE2_STRICT_POLICY_WHITELIST`` and
  ``ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST`` skip the permission check under
  the strict policy. The page still requires login, unless it is also in a
  login whitelist.
* A view with ``allow_without_permissions`` whose route is also in a login
  whitelist needs neither login nor permissions, so it is public.

The fuzzy whitelists match every path that starts with an entry. An entry of
``/api`` also matches ``/apiary/``, so end entries with ``/``.

Only add a route to a whitelist when everyone who can reach it may see it.


Files and Websockets Are Not Checked
====================================

The middleware never checks paths under ``STATIC_URL``, ``MEDIA_URL``, and
``ADMINLTE2_WEBSOCKET_URL``, or ``/favicon.ico`` (see
:ref:`configuration/known_routes:file and websocket routes`). Files served
under ``MEDIA_URL`` are public to anyone who has the URL. Serve private
uploads from a view that checks permissions instead, and check permissions in
your websocket consumers.


Middleware Hooks
================

``AuthMiddleware`` has two methods for projects to override in a subclass:
``login_required_hook(request)`` and ``permission_required_hook(request)``.
When one returns ``True``, the request passes that check, for every view. Keep
them narrow, and test them like any other access rule.


403 and 404 Responses
=====================

* Under the login required and strict policies, anonymous users get the same
  response for every URL that requires login, whether or not it exists: a
  redirect to the login page. Paths in
  ``ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST`` are the exception,
  because they always get Django's 404 response.
* Under the loose policy, pages are public, so a URL that exists loads and an
  unknown URL is redirected or returns a 404.
* By default, a logged-in user without a view's permissions is redirected
  home with a message, the same as for a page that doesn't exist, instead of
  getting Django's 403 response. The default 403 and 404 production messages
  are the same, so the message doesn't tell a page the user lacks permission
  for apart from a page that doesn't exist. Changing one of them makes them
  different.
* With ``DEBUG`` on, the 403 message names the view, and the middleware warns
  about misconfigured views in messages. As with Django's own debug page,
  never turn ``DEBUG`` on for a site that other people can reach.
