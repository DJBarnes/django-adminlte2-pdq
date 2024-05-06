"""Django-AdminLTE2-PDQ Middleware"""

# System Imports.
import warnings

# Third-Party Imports.
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve
from django.views.generic.base import RedirectView

# Internal Imports.
from .constants import (
    # General settings.
    LOGIN_REQUIRED,
    LOGIN_EXEMPT_WHITELIST,
    STRICT_POLICY,
    STRICT_POLICY_WHITELIST,
    LOGIN_URL,
    HOME_ROUTE,
    MEDIA_ROUTE,
    WEBSOCKET_ROUTE,
    # Debugging settings.
    TEXT_BLUE,
    TEXT_CYAN,
    TEXT_GREEN,
    TEXT_PURPLE,
    TEXT_RED,
    TEXT_RESET,
    TEXT_YELLOW,
)
from .utlis import debug_print


# Module Variables.
debug_header = '{0}{1}{2}'.format(TEXT_CYAN, '{0}', TEXT_RESET)
debug_var = '{0}{1}{2}{3}'.format(TEXT_PURPLE, '{0}', TEXT_RESET, '{1}')
debug_info = '{0}{1}{2}'.format(TEXT_BLUE, '{0}', TEXT_RESET)
debug_success = '{0}{1}{2}'.format(TEXT_GREEN, '{0}', TEXT_RESET)
debug_warn = '{0}{1}{2}'.format(TEXT_YELLOW, '{0}', TEXT_RESET)
debug_error = '{0}{1}{2}'.format(TEXT_RED, '{0}', TEXT_RESET)


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
        return self.run_auth_checks(request)

    def run_auth_checks(self, request, debug=False):
        """Various AdminLTE authentication checks upon User trying to access a view.

        Upon failure, user will be redirected accordingly.
        Redirects are determined by the LOGIN_REDIRECT_URL setting, and the ADMINLTE2_HOME_ROUTE setting.
        """
        if debug:
            debug_print.debug = True

        debug_print('\n\n')
        debug_print(debug_header.format('AdminLtePdq Middleware run_auth_checks():'))
        debug_print(debug_var.format('    type(request): ', type(request)))
        debug_print(debug_var.format('    dir(request): ', dir(request)))

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

        # Handle if view requires user login to proceed.
        # Determined by combination of the ADMINLTE2_USE_LOGIN_REQUIRED and ADMINLTE2_LOGIN_EXEMPT_WHITELIST settings.
        if LOGIN_REQUIRED and not self.verify_logged_in(request):
            # User not logged in and view requires login to access.

            debug_print(debug_error.format('Failed LoginRequired checks. Redirecting.'))

            # Redirect to login page.
            return redirect(LOGIN_URL + f'?next={request.path}')

        # Handle if view requires specific user permissions to proceed.
        # Determined by combination of the ADMINLTE2_USE_STRICT_POLICY and ADMINLTE2_STRICT_POLICY_WHITELIST settings.
        if STRICT_POLICY and not self.verify_permission_set(request):
            # No permissions defined on view or user failed permission checks.

            debug_print(debug_error.format('Failed PermissionRequired checks. Redirecting.'))

            # Redirect to home route.
            return redirect(HOME_ROUTE)

        # User passed all tests, return requested response.
        return self.get_response(request)

    def verify_logged_in(self, request, debug=False):
        """Checks to verify User is logged in, for views that require it."""
        if debug:
            debug_print.debug = True

        debug_print('\n\n')
        debug_print(debug_header.format('AdminLtePdq Middleware verify_logged_in():'))
        debug_print(debug_var.format('    request: ', request))
        debug_print(debug_var.format('    type(request): ', type(request)))

        # If user is already authenticated, just return true.
        if request.user.is_authenticated:
            debug_print(debug_success.format('Is Authenticated. Proceeding...'))
            debug_print('\n\n')

            return True

        # Determine some variable values.
        path = request.path
        resolver = resolve(path)
        app_name = resolver.app_name
        current_url_name = resolver.url_name
        fully_qualified_url_name = f"{app_name}:{current_url_name}"

        debug_print('')
        debug_print(debug_var.format('    path: ', path))
        debug_print(debug_var.format('    resolver: ', resolver))
        debug_print(debug_var.format('    app_name: ', app_name))
        debug_print(debug_var.format('    current_url_name: ', current_url_name))
        debug_print(debug_var.format('    fully_qualified_url_name: ', fully_qualified_url_name))

        # User not logged in. Still allow request for the following:
        return (
            # If url name exists in whitelist.
            current_url_name in LOGIN_EXEMPT_WHITELIST
            or fully_qualified_url_name in LOGIN_EXEMPT_WHITELIST
            # If path exists in whitelist.
            or path in LOGIN_EXEMPT_WHITELIST
            # If passes requirements for custom login hook (defined on a per-project basis).
            or self.login_required_hook(request)
            # If url is for media, as defined in settings.
            or self.verify_media_route(path)
            # If url is for websockets, as defined in settings.
            or self.verify_websocket_route(path)
        )

    def verify_permission_set(self, request, debug=False):
        """Verify Permission Set"""
        if debug:
            debug_print.debug = True

        debug_print('\n\n')
        debug_print(debug_header.format('AdminLtePdq Middleware verify_permission_set():'))
        debug_print(debug_var.format('    request: ', request))
        debug_print(debug_var.format('    type(request): ', request))

        exempt = False
        path = request.path

        # Try to get the view.
        try:
            view = resolve(path)
        except Http404:
            view = None

        debug_print(debug_var.format('    path: ', path))
        debug_print(debug_var.format('    view: ', view))
        debug_print(debug_var.format('    is_view: ', bool(view)))

        # If view, determine if function based or class based
        if view:
            # Get the view class
            view_class = getattr(view.func, 'view_class', None)

            # Determine some variable values.
            current_url_name = view.url_name
            app_name = view.app_name
            fully_qualified_url_name = f"{app_name}:{current_url_name}"

            # Determine if request url is exempt. Is the case for the following:
            if (
                # If url name exists in whitelist.
                current_url_name in STRICT_POLICY_WHITELIST
                or fully_qualified_url_name in STRICT_POLICY_WHITELIST
                # If path exists in whitelist.
                or path in STRICT_POLICY_WHITELIST
                # If is the equivalent of the "Django Admin" app.
                or app_name == 'admin'
                # If url is for media, as defined in settings.
                or self.verify_media_route(path)
                # If url is for websockets, as defined in settings.
                or self.verify_websocket_route(path)
                # If url is for redirecting, as defined in settings.
                or self.verify_redirect_route(view_class)
            ):
                # One or more conditions passed for url being exempt from checks.
                exempt = True

            debug_print('')
            debug_print(debug_var.format('    view_class: ', view_class))
            debug_print(debug_var.format('    is_view_class: ', bool(view_class)))
            debug_print(debug_var.format('    current_url_name: ', current_url_name))
            debug_print(debug_var.format('    app_name: ', app_name))
            debug_print(debug_var.format('    fully_qualified_url_name: ', fully_qualified_url_name))
            debug_print(debug_var.format('    exempt: ', exempt))

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

            debug_print('')
            debug_print(debug_var.format('    permissions: ', permissions))
            debug_print(debug_var.format('    one_of_permissions: ', one_of_permissions))
            debug_print(debug_var.format('    login_required: ', login_required))
            debug_print(debug_var.format('    view_name: ', view_name))
            debug_print(debug_var.format('    view_type: ', view_type))
            debug_print(debug_var.format('    view_perm_type: ', view_perm_type))

            # Allow request if any of the checks passed.
            if exempt or permissions or one_of_permissions or login_required:
                debug_print(debug_success.format('Passed permission checks OR url was exempt. Proceeding...'))
                debug_print('\n\n')

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

        debug_print('')
        debug_print(debug_error.format('Failed to pass auth checks.'))
        debug_print('\n\n')

        # If we made it this far, then failed all checks, return False.
        return False

    def login_required_hook(self, request):
        """Hook that can be overridden in subclasses to add additional ways
        to pass the login required criteria. Should return either True or False."""
        return False

    def permission_required_hook(self, request):
        """Hook that can be overridden in subclasses to add additional ways
        to pass the login required criteria. Should return either True or False."""
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
