"""Django-AdminLTE2-PDQ Middleware"""

# System Imports.
import warnings

from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve
from django.views.generic.base import RedirectView

from .constants import (
    LOGIN_REQUIRED,
    LOGIN_EXEMPT_WHITELIST,
    STRICT_POLICY,
    STRICT_POLICY_WHITELIST,
    LOGIN_URL,
    HOME_ROUTE,
    MEDIA_ROUTE,
    WEBSOCKET_ROUTE,
)


class AuthMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than ones defined in LOGIN_EXEMPT_ENDPOINTS.
    Exemptions to this requirement can optionally be specified with the
    ADMINLTE2_LOGIN_EXEMPT_WHITELIST setting in your settings.py file.
    (which you can copy from your urls.py).
    If a user tries to access one of these routes, they will be redirected to
    the LOGIN_URL defined in settings.

    Additionally, if the ADMINLTE2_USE_STRICT_POLICY setting is enabled,
    users will be prevented from accessing a route if the view for that route
    does not have permissions or login_required defined on that view.
    If a user tries to access one of these routes, they will be redirected to
    the ADMINLTE2_HOME_ROUTE defined in settings which is the only
    non-login required route that is exempt by default.
    If you would like to add additional exempt routes, you can add them to the
    ADMINLTE2_STRICT_POLICY_WHITELIST setting in your settings.py file.

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Ensure user object is accessible for Authentication checks.
        if not hasattr(request, 'user'):
            # Django SessionMiddleware is required to use Django AuthenticationMiddleware.
            # Django AuthenticationMiddleware is what gives us access to user object in request.
            # Django MessageMiddleware is required to display messages to user on middleware failure for a view.
            raise ImportError(
                'The Django-AdminLTE2-PDQ AuthMiddleware requires Django authentication middleware to be installed. '
                'Edit your MIDDLEWARE_CLASSES setting to include:\n\n'
                ' * "django.contrib.sessions.middleware.SessionMiddleware",\n'
                ' * "django.contrib.auth.middleware.AuthenticationMiddleware",\n'
                ' * "django.contrib.messages.middleware.MessageMiddleware",\n'
                ' * "adminlte2_pdq.middleware.AuthMiddleware",\n'
                '\nNote that ordering of above middleware DOES matter.\n\n'
                'If the above doesn\'t solve this error, then ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes'
                ' "django.core.context_processors.auth" as well.'
            )

        # If the Login Required is turned on.
        if LOGIN_REQUIRED and not self.verify_logged_in(request):
            # Not logged in, redirect to login page.
            return redirect(LOGIN_URL + f'?next={request.path}')

        # If View Strict Policy is turned on.
        if STRICT_POLICY and not self.verify_permission_set(request):
            # No permissions defined on view, redirect to home route.
            return redirect(HOME_ROUTE)

        # User passed all tests, return requested response.
        return self.get_response(request)

    def verify_logged_in(self, request):
        """Verify User Logged In"""

        # If user is already authenticated, just return true.
        if request.user.is_authenticated:
            return True

        # Get the path and current url name and if either listed in exempt whitelist, return true
        path = request.path
        resolver = resolve(path)
        app_name = resolver.app_name
        current_url_name = resolver.url_name
        fully_qualified_url_name = f"{app_name}:{current_url_name}"
        return (
            current_url_name in LOGIN_EXEMPT_WHITELIST
            or fully_qualified_url_name in LOGIN_EXEMPT_WHITELIST
            or path in LOGIN_EXEMPT_WHITELIST
            or self.login_required_hook(request)
            or self.verify_media_route(path)
            or self.verify_websocket_route(path)
        )

    def login_required_hook(self, request):
        """Hook that can be overridden in subclasses to add additional ways
        to pass the login required criteria. Should return either True or False."""
        return False

    def verify_permission_set(self, request):
        """Verify Permission Set"""

        # Default to None for everything
        permissions = None
        one_of_permissions = None
        login_required = None
        view = None
        exempt = False

        path = request.path

        # Try to get the view.
        try:
            view = resolve(path)
        except Http404:
            view = None

        # If view, determine if function based or class based
        if view:

            # Get the view class
            view_class = getattr(view.func, 'view_class', None)

            # Determine if request url is exempt.
            current_url_name = view.url_name
            app_name = view.app_name
            fully_qualified_url_name = f"{app_name}:{current_url_name}"
            if (
                current_url_name in STRICT_POLICY_WHITELIST
                or fully_qualified_url_name in STRICT_POLICY_WHITELIST
                or path in STRICT_POLICY_WHITELIST
                or app_name == 'admin'
                or self.verify_media_route(path)
                or self.verify_websocket_route(path)
                or self.verify_redirect_route(view_class)
            ):
                exempt = True

            if view_class:
                # Get attributes
                permissions = getattr(view_class, 'permission_required', [])
                one_of_permissions = getattr(view_class, 'permission_required_one', [])
                login_required = getattr(view_class, 'login_required', False)
                view_name = view_class.__qualname__
                view_type = 'class-based'
                view_perm_type = 'attribute'
            else:
                # Get attributes
                permissions = getattr(view.func, 'permissions', [])
                one_of_permissions = getattr(view.func, 'one_of_permissions', [])
                login_required = getattr(view.func, 'login_required', False)
                view_name = view.func.__qualname__
                view_type = 'function-based'
                view_perm_type = 'decorator'

            # If there are permissions, or login_required
            if exempt or permissions or one_of_permissions or login_required:
                return True

            # Permissions or Login Required not set, add messages, warnings, and return False
            warning_message = (
                f"The {view_type} view '{view_name}' does not have the"
                " permission_required, one_of_permission, or login_required"
                f" {view_perm_type} set and the option ADMINLTE2_USE_STRICT_POLICY is"
                " set to True. This means that this view is inaccessible until"
                " either permissions are set on the view or the url_name for the"
                " view is added to the ADMINLTE2_STRICT_POLICY_WHITELIST setting."
            )
            warnings.warn(warning_message)
            messages.debug(request, warning_message)

        # Failed somewhere along the way, return false.
        return False

    def verify_media_route(self, path):
        """Verify that the path of the request is not a MEDIA URL"""
        return_val = False
        if MEDIA_ROUTE and MEDIA_ROUTE != '/':
            return_val = path.startswith(MEDIA_ROUTE)
        return return_val

    def verify_websocket_route(self, path):
        """Verify that the path of the request is not a WEBSOCKET URL"""
        return_val = False
        if WEBSOCKET_ROUTE and WEBSOCKET_ROUTE != '/':
            return_val = path.startswith(WEBSOCKET_ROUTE)
        return return_val

    def verify_redirect_route(self, view_class):
        """Verify that the view class is a RedirectView"""
        return view_class and view_class == RedirectView
