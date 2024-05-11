"""Django-AdminLTE2-PDQ Middleware"""

# System Imports.
import warnings

# Third-Party Imports.
from django.http import Http404
from django.conf import settings
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

    def run_auth_checks(self, request, debug=True):
        """Various AdminLTE authentication checks upon User trying to access a view.

        Upon failure, user will be redirected accordingly.
        Redirects are determined by the LOGIN_REDIRECT_URL setting, and the ADMINLTE2_HOME_ROUTE setting.
        """
        if debug:
            debug_print.debug = True

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

        debug_print(debug_var.format('    LOGIN_REQUIRED: ', LOGIN_REQUIRED))
        debug_print(debug_var.format('    STRICT_POLICY: ', STRICT_POLICY))

        # Calculate data for decorated view, in order to determine permission logic.
        view_data = self.parse_request_data(request)

        # Handle if using login_required decorator within STRICT mode.
        if STRICT_POLICY and view_data['decorator_name'] == 'login_required':
            error_message = (
                'The login_required {view_perm_type} is not supported in AdminLtePdq STRICT mode. '
                'Having STRICT mode on implicitly assumes login and permissions are required '
                'for all views that are not in a whitelist setting.'
                '\n\n'
                'Also consider the allow_anonymous_access or allow_without_permissions {view_perm_type}s.'
            ).format(
                view_perm_type=view_data['view_perm_type'],
            )
            raise PermissionError(error_message)

        # Handle if using allow_anonymous_access or allow_without_permissions decorator in LOOSE mode.
        if not STRICT_POLICY and view_data['decorator_name'] in ['allow_anonymous_access', 'allow_without_permissions']:
            error_message = (
                'The {decorator_name} {view_perm_type} is not supported in AdminLtePdq LOOSE mode. '
                'This {view_perm_type} only exists for clarity of permission access in STRICT mode.'
            ).format(
                decorator_name=view_data['decorator_name'],
                view_perm_type=view_data['view_perm_type'],
            )
            raise PermissionError(error_message)

        if (
            # Is a permission view.
            view_data['decorator_name'] == 'permission_required'
            # And no permission values defined.
            and (not view_data['permissions'] and not view_data['one_of_permissions'])
        ):
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    "AdminLtePdq Warning: The {view_type} view '{view_name}' has permission "
                    "requirements, but does not have any permissions set. "
                    "This means that this view is inaccessible until permissions "
                    "are set for the view."
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                ).format(
                    view_type=view_data['view_type'],
                    view_name=view_data['view_name'],
                )
                # Create console warning message.
                warnings.warn(warning_message)
                # Create Django Messages warning.
                messages.warning(request, warning_message)
            else:
                # Error if in production mode.
                error_message = (
                    'Could not access requested page. The site is configured incorrectly. '
                    'Please contact the site administrator.'
                )
                # Create Django Messages warning.
                messages.warning(request, error_message)

        # Handle if view requires user login to proceed.
        # Determined by combination of the ADMINLTE2_USE_LOGIN_REQUIRED and ADMINLTE2_LOGIN_EXEMPT_WHITELIST settings.
        if LOGIN_REQUIRED and not self.verify_logged_in(request, view_data):
            # User not logged in and view requires login to access.

            debug_print(debug_error.format('Failed LoginRequired checks. Redirecting.'))

            # Redirect to login page.
            return redirect(LOGIN_URL + f'?next={request.path}')

        # Handle if view requires specific user permissions to proceed.
        # Determined by combination of the ADMINLTE2_USE_STRICT_POLICY and ADMINLTE2_STRICT_POLICY_WHITELIST settings.
        if (
            # Is STRICT mode.
            STRICT_POLICY
            # Is not a decorator allowing lesser permissions.
            and not view_data['decorator_name'] in ['allow_anonymous_access', 'allow_without_permissions']
            # Fails general checks for everything else.
            and not self.verify_strict_mode_permission_set(request, view_data)
        ):
            # No permissions defined on view or user failed permission checks.

            debug_print(debug_error.format('Failed PermissionRequired checks. Redirecting.'))

            # Redirect to home route.
            return redirect(HOME_ROUTE)

        if debug:
            debug_print.debug = False

        # User passed all tests, return requested response.
        response = self.get_response(request)
        if view_data['decorator_name']:
            response.decorator_name = view_data['decorator_name']
            response.login_required = view_data['login_required']
            response.permissions = view_data['permissions']
            response.one_of_permissions = view_data['one_of_permissions']
        return response

    def parse_request_data(self, request, debug=True):
        """Parses request data and generates dict of calculated values."""

        if debug:
            debug_print.debug = True

        # Initialize data structure.
        data_dict = {
            'path': request.path,
            'decorator_name': '',
        }

        # Try to get the view.
        try:
            resolver = resolve(data_dict['path'])
            data_dict['resolver'] = resolver

            # Determine if view function or view class.
            view_class = getattr(resolver.func, 'view_class', None)
            data_dict['view_class'] = view_class

            # Determine universal values.
            app_name = resolver.app_name
            current_url_name = resolver.url_name
            fully_qualified_url_name = f"{app_name}:{current_url_name}"

            if view_class:
                # Get class attributes.
                decorator_name = getattr(view_class, 'decorator_name', '')
                login_required = getattr(view_class, 'login_required', False)
                permissions = getattr(view_class, 'permission_required', [])
                one_of_permissions = getattr(view_class, 'permission_required_one', [])
                view_name = view_class.__qualname__
                view_type = 'class-based'
                view_perm_type = 'mixin'
            else:
                # Get function attributes.
                decorator_name = getattr(resolver.func, 'decorator_name', '')
                login_required = getattr(resolver.func, 'login_required', False)
                permissions = getattr(resolver.func, 'permissions', [])
                one_of_permissions = getattr(resolver.func, 'one_of_permissions', [])
                view_name = resolver.func.__qualname__
                view_type = 'function-based'
                view_perm_type = 'decorator'

            data_dict.update(
                {
                    'resolver': resolver,
                    'app_name': app_name,
                    'current_url_name': current_url_name,
                    'fully_qualified_url_name': fully_qualified_url_name,
                    'decorator_name': decorator_name,
                    'login_required': login_required,
                    'permissions': permissions,
                    'one_of_permissions': one_of_permissions,
                    'view_name': view_name,
                    'view_type': view_type,
                    'view_perm_type': view_perm_type,
                }
            )

        except Http404:
            data_dict.update({'resolver': None})

        debug_print(data_dict)

        if debug:
            debug_print.debug = False

        # Return parsed data.
        return data_dict

    def verify_logged_in(self, request, view_data, debug=False):
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

        # User not logged in. Still allow request for the following:
        return (
            # If url name exists in whitelist.
            view_data['current_url_name'] in LOGIN_EXEMPT_WHITELIST
            or view_data['fully_qualified_url_name'] in LOGIN_EXEMPT_WHITELIST
            # If path exists in whitelist.
            or view_data['path'] in LOGIN_EXEMPT_WHITELIST
            # If passes requirements for custom login hook (defined on a per-project basis).
            or self.login_required_hook(request)
            # If url is for media, as defined in settings.
            or self.verify_media_route(view_data['path'])
            # If url is for websockets, as defined in settings.
            or self.verify_websocket_route(view_data['path'])
        )

    def verify_strict_mode_permission_set(self, request, view_data, debug=False):
        """Verify view access based on permission/login requirements on the view object.

        :return: False if user cannot access view as per Strict Mode policy | True otherwise.
        """

        if debug:
            debug_print.debug = True

        debug_print('\n\n')
        debug_print(debug_header.format('AdminLtePdq Middleware verify_permission_set():'))
        debug_print(debug_var.format('    request: ', request))
        debug_print(debug_var.format('    type(request): ', request))

        exempt = False

        # If view, determine if function based or class based
        if view_data['resolver']:

            # Determine if request url is exempt. Is the case for the following:
            if (
                # If url name exists in whitelist.
                view_data['current_url_name'] in STRICT_POLICY_WHITELIST
                or view_data['fully_qualified_url_name'] in STRICT_POLICY_WHITELIST
                # If path exists in whitelist.
                or view_data['path'] in STRICT_POLICY_WHITELIST
                # If is the equivalent of the "Django Admin" app.
                or view_data['app_name'] == 'admin'
                # If url is for media, as defined in settings.
                or self.verify_media_route(view_data['path'])
                # If url is for websockets, as defined in settings.
                or self.verify_websocket_route(view_data['path'])
                # If url is for redirecting, as defined in settings.
                or self.verify_redirect_route(view_data['view_class'])
            ):
                # One or more conditions passed for url being exempt from checks.
                exempt = True

            # Allow request if any of the checks passed.
            if (
                # View is exempt from requirements.
                exempt
                # OR view didn't require permissions due to decorators.
                or view_data['decorator_name'] in ['allow_anonymous_access', 'allow_without_permissions']
                # OR user had the correct permissions.
                # For now, this check technically only works because we don't set these values
                # on the redirect-to-login requests. So they're populated if the user passes
                # decorator/mixin checks, and unpopulated otherwise.
                #
                # If we ever start populating these values on all requests, then
                # this logic will no longer work.
                or view_data['login_required']
                or view_data['permissions']
                or view_data['one_of_permissions']
            ):
                debug_print(debug_success.format('Passed permission checks OR url was exempt. Proceeding...'))
                debug_print('\n\n')

                return True

            # Decorator/Mixin failed checks, or Login Required not set.
            # Add messages, warnings, and return False.
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    "AdminLtePdq Warning: This project is set to run in strict mode, and "
                    "the {view_type} view '{view_name}' does not have any {view_perm_type}s set. "
                    "This means that this view is inaccessible until permission {view_perm_type}s "
                    "are set for the view, or the view is added to the "
                    "ADMINLTE2_STRICT_POLICY_WHITELIST setting."
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                ).format(
                    view_type=view_data['view_type'],
                    view_name=view_data['view_name'],
                    view_perm_type=view_data['view_perm_type'],
                )
                # Create console warning message.
                warnings.warn(warning_message)
                # Create Django Messages warning.
                messages.warning(request, warning_message)
            else:
                # Error if in production mode.
                error_message = (
                    'Could not access requested page. The site is configured incorrectly. '
                    'Please contact the site administrator.'
                )
                # Create Django Messages warning.
                messages.warning(request, error_message)

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
