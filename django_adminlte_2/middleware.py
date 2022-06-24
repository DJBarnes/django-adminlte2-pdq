"""Django-AdminLTE-2 Middleware"""

# System Imports.
import warnings

from django.conf import settings
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve




# Known routes that should never require being logged in.
LOGIN_URL = getattr(settings, 'LOGIN_URL', '/accounts/login')
LOGOUT_ROUTE = getattr(settings, 'LOGOUT_ROUTE', 'logout')
PWD_RESET_ROUTE = getattr(settings, 'PWD_RESET_ROUTE', 'password_reset')
PWD_RESET_DONE_ROUTE = getattr(settings, 'PWD_RESET_DONE_ROUTE', 'password_reset_done')
PWD_RESET_CONFIRM_ROUTE = getattr(settings, 'PWD_RESET_CONFIRM_ROUTE', 'password_reset_confirm')
PWD_RESET_COMPLETE_ROUTE = getattr(settings, 'PWD_RESET_COMPLETE_ROUTE', 'password_reset_complete')

# Known routes that should never have a permission check done.
HOME_ROUTE = getattr(settings, 'ADMINLTE2_HOME_ROUTE', 'django_adminlte_2:home')

# List of known routes that should never require being logged in.
LOGIN_EXEMPT_WHITELIST = [
    LOGIN_URL,
    LOGOUT_ROUTE,
    PWD_RESET_ROUTE,
    PWD_RESET_DONE_ROUTE,
    PWD_RESET_CONFIRM_ROUTE,
    PWD_RESET_COMPLETE_ROUTE,
]
# List of known routes that should never require permissions to access.
STRICT_POLICY_WHITELIST = [
    HOME_ROUTE,
]

# Add any user defined list of exempt urls to the constant.
LOGIN_EXEMPT_WHITELIST += getattr(settings, 'ADMINLTE2_LOGIN_EXEMPT_WHITELIST', [])
STRICT_POLICY_WHITELIST += getattr(settings, 'ADMINLTE2_STRICT_POLICY_WHITELIST', [])

# Get whether or not we are using LoginRequired and PermissionRequired
LOGIN_REQUIRED = getattr(settings, 'ADMINLTE2_USE_LOGIN_REQUIRED', False)
VIEW_STRICT_POLICY = getattr(settings, 'ADMINLTE2_USE_VIEW_STRICT_POLICY', False)


class AuthMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than ones defined in LOGIN_EXEMPT_ENDPOINTS.
    Exemptions to this requirement can optionally be specified with the
    ADMINLTE2_LOGIN_EXEMPT_WHITELIST setting in your settings.py file.
    (which you can copy from your urls.py).
    If a user tries to access one of these routes, they will be redirected to
    the LOGIN_URL defined in settings.

    Additionally, if the ADMINLTE2_USE_VIEW_STRICT_POLICY setting is enabled,
    users will be prevented from accessing a route if the view for that route
    does not have permissions or login_required defined on that view.
    If a user tries to access one of these routes, they will be redirected to
    the ADMINLTE2_HOME_ROUTE defined in settings which is the only route that
    is exempt by default. If you would like to add additional exempt routes,
    you can add them to the ADMINLTE2_STRICT_POLICY_WHITELIST setting in your
    settings.py file.

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'user'), (
            'The Django-AdminLTE-2 AuthMiddleware'
            ' requires authentication middleware to be installed. Edit your'
            ' MIDDLEWARE_CLASSES setting to insert'
            ' "django.contrib.auth.middleware.AuthenticationMiddleware". If that doesn\'t'
            ' work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes'
            '"django.core.context_processors.auth".'
        )

        # If the Login Required is turned on.
        if LOGIN_REQUIRED:
            # Verify user logged in.
            if self.verify_logged_in(request):
                # If View Strict Policy is turned on.
                if VIEW_STRICT_POLICY:
                    # Verify view has defined permissions.
                    if self.verify_permission_set(request):
                        # All checks out, return requested response.
                        return self.get_response(request)
                    else:
                        # No permissions defined on view, redirect to home route.
                        return redirect(HOME_ROUTE)
                else:
                    # User Logged in, return requested response.
                    return self.get_response(request)
            else:
                # Not logged in, redirect to login page.
                return redirect(LOGIN_URL + f'?next={request.path}')
        else:
            # If View Strict Policy is turned on.
            if VIEW_STRICT_POLICY:
                # Verify view has defined permissions.
                if self.verify_permission_set(request):
                    # All checks out, return requested response.
                    return self.get_response(request)
                else:
                    # No permissions defined on view, redirect to home route.
                    return redirect(HOME_ROUTE)
            else:
                # User Logged in, return requested response.
                return self.get_response(request)

    #     if LOGIN_REQUIRED:
    #         return self.login_required(request)
    #     else:
    #         return self.check_for_view_strict_policy(request)

    # def login_required(self, request):
    #     if self.verify_logged_in(request):
    #         return self.check_for_view_strict_policy(request)
    #     else:
    #         # Not logged in, redirect to login page.
    #         return redirect(LOGIN_URL + f'?next={request.path}')


    # def check_for_view_strict_policy(self, request):
    #     if VIEW_STRICT_POLICY:
    #         return self.view_strict_policy_required(request)
    #     else:
    #         return self.get_response(request)


    # def view_strict_policy_required(self, request):
    #     # Verify view has defined permissions.
    #     if self.verify_permission_set(request):
    #         # All checks out, return requested response.
    #         return self.get_response(request)
    #     else:
    #         # No permissions defined on view, redirect to home route.
    #         return redirect(HOME_ROUTE)


    def verify_logged_in(self, request):
        """Verify User Logged In"""

        if request.user.is_authenticated:
            return True
        else:
            path = request.path
            current_url_name = resolve(path).url_name

            if current_url_name in LOGIN_EXEMPT_WHITELIST or path in LOGIN_EXEMPT_WHITELIST:
                return True
            else:
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

            # Determine if request url is exempt.
            current_url_name = view.url_name
            if current_url_name in STRICT_POLICY_WHITELIST or path in STRICT_POLICY_WHITELIST:
                exempt = True

            view_class = getattr(view.func, 'view_class', None)
            if view_class:
                # Get attributes
                permissions = getattr(view_class, 'permission_required', [])
                one_of_permissions = getattr(view_class, 'permission_required_one', [])
                login_required = getattr(view_class, 'login_required', False)
            else:
                # Get attributes
                permissions = getattr(view.func, 'permissions', [])
                one_of_permissions = getattr(view.func, 'one_of_permissions', [])
                login_required = getattr(view.func, 'login_required', False)

        # If there are permissions, or login_required
        if exempt or permissions or one_of_permissions or login_required:
            return True

        # Permissions or Login Required not set, add messages, warnings, and return False
        warning_message = (
            f"The view {view.func.__qualname__} does not have the permission,"
            " one_of_permission, or login_required attribute set and the option"
            " ADMINLTE2_USE_VIEW_STRICT_POLICY is set to True. This means that"
            " this view is inaccessible until permissions are set on the view"
        )
        warnings.warn(warning_message)
        messages.debug(request, warning_message)
        return False
