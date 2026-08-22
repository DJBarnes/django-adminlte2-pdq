Authentication and Authorization Overview
*****************************************

The **Django-AdminLTE2-PDQ** package comes with built-in functionality to make it
easy to customize and manage various user page access.

In short, this can be boiled down to three "policy modes" provided by the package:

* **Django Default (Aka, "Loose" Authentication Mode)** -
  All site pages are open to everyone by default, and require decorators/mixins
  to limit access.

  * While less secure, this comes as the package default, so that out-of-the-box
    behavior matches Django's default behavior as closely as possible.

* **"Login-Required" Authentication Mode** - All site pages are only accessible
  to users that have logged in.
  Aka, all site pages are behind a login wall by default.

  * This is moderately more secure than the Django default.
    It ensures that developers cannot "forget" to secure a page, unintentionally
    giving access to the larger world.
    However, this mode defaults to allowing any logged-in user to access any page,
    so it's still not optimally secure.

* **"Strict" Authentication Mode** - All pages are only accessible by users that
  have logged in AND have the correct permissions to access.
  This means that in order to be valid, all site pages must declare which user
  permissions they require for access.

  * Depending on view type (function or class), this is done via decorators (for
    functions) or class variables (for mixins and class views).


Each of these policies are defined via package settings.
See :doc:`../configuration/authorization` for details on how to implement these
settings.

For further details on how each policy mode behaves, see :doc:`./policies`.


Use Case Examples & Modifying Default Policy Behavior
=====================================================

The above policies only describe the default behavior of a given view.

This package fully supports modifying behavior for any view to handle as needed,
via either project whitelists, or by using decorators and mixins on individual
views.
Any view can be modified in any way, you will never be "locked in" to the default
behavior of your chosen policy.

For example:

* Maybe you have a site that you largely want visible to the public. So you can
  leave it "Loose" mode.
  Perhaps for a few views, you modify them to be behind a login wall, and for very
  specific management views, you opt in to use the "permission required" logic.

* You might have a site that largely should be available for anyone within a given
  organization to access.
  So you put the site into "Login Required" mode, so that as soon as someone is
  logged in, they can see most pages by default.
  Then anything meant for the public or meant for administration, you modify
  accordingly with decorators/mixins.

* Perhaps you have a site for a company with many departments.
  Each department should be isolated, and only able to see what's relevant to
  that department. So you opt into "Strict" mode.
  Then for the few views that should be visible to any department, you use
  decorators/mixins to change access to "login required only".


This is just an overview of a few possible scenarios this package can help with.

Note that obviously you can manually program all of this yourself, without the
help of this package.
However, this package already does the heavy lifting for you, working to keep
all of this logic easy to call and modify, with just a few short lines per view.


For specific details on using decorators to modify function view logic, see
:doc:`./function_views`.

For specific details on using mixins to modify class view logic, see
:doc:`./class_views`.
