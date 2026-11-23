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
* The middleware and the sidebar only read this package's decorators and
  mixins. They can't see the test in Django's ``user_passes_test`` decorator
  or ``UserPassesTestMixin``, so the view still runs the test, but the sidebar
  shows its link to every user who passes the policy's login and permission
  rules, including users who fail the test. Under the strict policy, a view
  with only a user test has no defined permissions, so the middleware blocks
  it until it also has ``allow_without_permissions``, a permission decorator
  or mixin, or a whitelist entry. When the test can be written as
  permissions, set ``permissions`` or ``one_of_permissions`` on the menu node
  to hide the link from users who fail it.


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


Login Redirects
===============

Redirects to the login page pass the requested URL, with its query string, as
``next``, and Django's ``LoginView`` sends the user there after they log in.

* Django's ``LoginView`` only follows ``next`` to pages on the same site, and
  goes to ``LOGIN_REDIRECT_URL`` for anything else, so ``next`` can't send
  users to another site. A custom login view needs the same check
  (``url_has_allowed_host_and_scheme``).
* The page that ``next`` leads to runs the same login and permission checks as
  any other request, so ``next`` doesn't let anyone past them.
* Under the login required and strict policies, every URL that requires login
  gets the same redirect, so ``next`` doesn't show which URLs exist.
* The requested URL appears in the login page's URL, so it ends up in browser
  history, in server logs, and in links people copy. Django's default
  ``SECURE_REFERRER_POLICY`` of ``"same-origin"`` keeps it out of requests to
  other sites. Avoid putting sensitive values in query strings.

To leave ``next`` out, set
:ref:`configuration/authorization:ADMINLTE2_USE_LOGIN_NEXT` to False. Every
login then goes to ``LOGIN_REDIRECT_URL``. The setting only applies to this
package's middleware, decorators, and mixins. Django's own, such as
``user_passes_test``, still add ``next`` unless you pass them
``redirect_field_name=None``.
