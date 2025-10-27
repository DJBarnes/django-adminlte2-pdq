"""Django-AdminLTE2-PDQ Middleware"""

# System Imports.
import logging
import warnings

# Third-Party Imports.
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import redirect
from django.urls import resolve, is_valid_path
from django.utils.http import escape_leading_slashes
from django.views.generic.base import RedirectView

# Internal Imports.
from .constants import (
    REDIRECT_TO_HOME_ON_403,
    REDIRECT_TO_HOME_ON_404,
    LOGIN_REQUIRED,
    LOGIN_EXEMPT_WHITELIST,
    LOGIN_EXEMPT_FUZZY_WHITELIST,
    RESPONSE_403_DEBUG_MESSAGE,
    RESPONSE_403_PRODUCTION_MESSAGE,
    RESPONSE_404_DEBUG_MESSAGE,
    RESPONSE_404_PRODUCTION_MESSAGE,
    STRICT_POLICY_SERVE_404_FUZZY_WHITELIST,
    STRICT_POLICY,
    STRICT_POLICY_WHITELIST,
    STRICT_POLICY_FUZZY_WHITELIST,
    LOGIN_URL,
    HOME_ROUTE,
    MEDIA_ROUTE,
    STATIC_ROUTE,
    WEBSOCKET_ROUTE,
)


logger = logging.getLogger(__name__)


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

    def run_auth_checks(self, request):
        """Various AdminLTE authentication checks upon User trying to access a view.

        Upon failure, user will be redirected accordingly.
        Redirects are determined by the LOGIN_REDIRECT_URL setting, and the ADMINLTE2_HOME_ROUTE setting.

        # TODO: I really don't like how much heavy lifting this middleware is doing.
            Consider trying to offload logic to decorators/mixins in the future, if possible.
            Some of this has to be in the middleware, due to
        """

        # Ensure user object is accessible for Authentication checks and messages is available.
        if not hasattr(request, "user") or not hasattr(request, "_messages"):
            # Django SessionMiddleware is required to use Django AuthenticationMiddleware.
            # Django AuthenticationMiddleware is what gives us access to user object in request.
            # Django MessageMiddleware is required to display messages to user on middleware failure for a view.
            raise ImproperlyConfigured(
                "The Django-AdminLTE2-PDQ AuthMiddleware requires Django authentication middleware to be installed. "
                "Edit your MIDDLEWARE_CLASSES setting to include:\n\n"
                ' * "django.contrib.sessions.middleware.SessionMiddleware",\n'
                ' * "django.contrib.auth.middleware.AuthenticationMiddleware",\n'
                ' * "django.contrib.messages.middleware.MessageMiddleware",\n'
                ' * "adminlte2_pdq.middleware.AuthMiddleware",\n'
                "\nNote that ordering of above middleware DOES matter.\n\n"
                "If the above doesn't solve this error, then ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes"
                ' "django.core.context_processors.auth" as well.'
            )

        # Calculate data for decorated view, in order to determine permission logic.
        view_data = self.parse_request_data(request)

        # Handle if an invalid url was entered.
        if view_data["resolver"] is None:

            # Verify that the path is not for static, media, favicon, or part of whitelist, in which case a 404 is okay.
            # Everything else should be an actual view. So, a redirect to the home page makes sense.
            if (
                # Is a special route where 404s are okay
                self.is_special_route(view_data)
                # Verify if whitelisted route
                or view_data["path"] in STRICT_POLICY_SERVE_404_FUZZY_WHITELIST
                # Site setup to handle 404s manually
                or not REDIRECT_TO_HOME_ON_404
            ):
                raise Http404()

            # Entered url does not correspond to any view. Redirect to home route.
            if settings.DEBUG:
                # Handle output when DEBUG = True.
                if len(RESPONSE_404_DEBUG_MESSAGE) > 0:
                    messages.warning(request, RESPONSE_404_DEBUG_MESSAGE)
                    logger.warning(RESPONSE_404_DEBUG_MESSAGE)
            else:
                # Handle output when DEBUG = False.
                if len(RESPONSE_404_PRODUCTION_MESSAGE) > 0:
                    messages.warning(request, RESPONSE_404_PRODUCTION_MESSAGE)

            # Redirect to home route.
            return redirect(HOME_ROUTE)

        # Raise errors on conflicting decorator/mixin states.
        self.check_main_error_states(request, view_data)

        # Handle if view requires user login to proceed.
        # Determined by combination of the ADMINLTE2_USE_LOGIN_REQUIRED and ADMINLTE2_LOGIN_EXEMPT_WHITELIST settings.
        if (LOGIN_REQUIRED or view_data["login_required"]) and not self.verify_logged_in(request, view_data):
            # User not logged in and view requires login to access.

            # Redirect to login page.
            return redirect(LOGIN_URL + f"?next={request.path}")

        # Check any post login error states.
        # NOTE: This call need to happen after we do the above Login Required checking.
        self.check_post_login_check_error_states(request, view_data)

        # Handle if view requires specific user permissions to proceed.
        # Determined by combination of the ADMINLTE2_USE_STRICT_POLICY and ADMINLTE2_STRICT_POLICY_WHITELIST settings.
        permission_required = view_data["decorator_name"] in ("permission_required", "permission_required_one")
        if (STRICT_POLICY or permission_required) and not self.verify_permissions(request, view_data):
            # Apply potential warnings
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = RESPONSE_403_DEBUG_MESSAGE.format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                )
            else:
                warning_message = RESPONSE_403_PRODUCTION_MESSAGE
            # Create Django Messages warning.
            messages.warning(request, warning_message)
            # Site setup to use built-in 403 handling
            if REDIRECT_TO_HOME_ON_403:
                # Redirect to home route.
                return redirect(HOME_ROUTE)
            else:
                raise PermissionDenied()

        # User passed all tests or wants to handle 403s manually,
        # return requested response.
        response = self.get_response(request)
        if view_data["decorator_name"]:
            response.admin_pdq_data = view_data

        return response

    def check_main_error_states(self, request, view_data):
        """Check for various conflicting decorator/mixin states, raise error upon finding any."""

        # Check if view is in any whitelists.
        is_login_whitelisted = self.is_login_whitelisted(view_data)
        is_perm_whitelisted = self.is_permission_whitelisted(view_data)
        view_defines_permissions = bool(view_data["one_of_permissions"]) or bool(view_data["full_permissions"])

        # Pull out some data from the view_data for easier processing
        view_decorator_name = view_data["decorator_name"]
        view_type = view_data["view_type"]
        view_name = view_data["view_name"]
        view_perm_type = view_data["view_perm_type"]

        # Get the actual name of the decorator used based on whether it is a function-based or class-based view.
        if view_perm_type == "decorator":
            decorator_name = view_decorator_name
        else:
            decorator_name = view_decorator_name.replace("_", " ").title().replace(" ", "")

        # Handle if using login_required decorator within STRICT mode or Login Required mode.
        if (STRICT_POLICY or LOGIN_REQUIRED) and view_decorator_name == "login_required":

            # Determine some error message values based on mode.
            if STRICT_POLICY:
                mode_type = "STRICT"
                mode_text = "login and permissions are"
                if view_perm_type == "decorator":
                    related_decorators = "'allow_anonymous_access' or 'allow_without_permissions'"
                else:
                    related_decorators = "'AllowAnonymousAccess' or 'AllowWithoutPermissions'"
                pluralize = "s"
            else:
                mode_type = "LOGIN REQUIRED"
                mode_text = "login is"
                if view_perm_type == "decorator":
                    related_decorators = "'allow_anonymous_access'"
                else:
                    related_decorators = "'AllowAnonymousAccess'"
                pluralize = ""

            # Display error message.
            error_message = (
                f"AdminLtePdq Error: The '{decorator_name}' {view_perm_type} is not supported in AdminLtePdq "
                f"{mode_type} mode. Having {mode_type} mode on implicitly assumes {mode_text} required "
                "for all views that are not in a whitelist setting."
                "\n\n"
                f"Also consider the {related_decorators} {view_perm_type}{pluralize}."
            )
            raise ImproperlyConfigured(error_message)

        # Handle if using allow_anonymous_access or allow_without_permissions decorator in mode that doesn't make sense.
        if (
            # Using allow_anonymous or allow_without_permissions in Loose mode.
            (
                (not STRICT_POLICY and not LOGIN_REQUIRED)
                and view_decorator_name in ["allow_anonymous_access", "allow_without_permissions"]
            )
            # Or using allow_without_permissions outside of strict mode.
            or (not STRICT_POLICY and view_decorator_name == "allow_without_permissions")
        ):
            # Determine some error message values based on mode.
            if not STRICT_POLICY and not LOGIN_REQUIRED:
                mode_type = "LOOSE"
            else:
                mode_type = "LOGIN REQUIRED"

            # Display error message.
            error_message = (
                f"AdminLtePdq Error: The '{decorator_name}' {view_perm_type} is not supported in AdminLtePdq "
                f"{mode_type} mode. This {view_perm_type} only exists for clarity of permission access in STRICT mode."
            )
            raise ImproperlyConfigured(error_message)

        # Handle if view is strict-mode whitelisted but using a decorator/mixin state that doesn't make sense.
        if is_perm_whitelisted:
            # Whitelisted, yet using a decorator that requires permissions. Raise error.
            if view_decorator_name == "permission_required":
                error_message = (
                    f"AdminLtePdq Error: The {view_type} view '{view_name}' has a permission {view_perm_type}, "
                    "but is in the ADMINLTE2_STRICT_POLICY_WHITELIST setting. Please remove one."
                )
                raise ImproperlyConfigured(error_message)

            # Whitelisted, and using a decorator that also removes permissions. Raise warning.
            if view_decorator_name == "allow_without_permissions":
                warning_message = (
                    f"AdminLtePdq Warning: The {view_type} view '{view_name}' has an '{decorator_name}' "
                    f"{view_perm_type}, but is also in the ADMINLTE2_STRICT_POLICY_WHITELIST. These two effectively "
                    "achieve the same functionality."
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

        # Handle if view is login whitelisted but using a decorator/mixin state that doesn't make sense.
        if is_login_whitelisted:
            # Whitelisted, yet using a decorator that requires login. Raise error.
            if view_decorator_name == "login_required":
                error_message = (
                    f"AdminLtePdq Error: The {view_type} view '{view_name}' has a '{decorator_name}' "
                    f"{view_perm_type}, but is in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST setting. Please remove one."
                )
                raise ImproperlyConfigured(error_message)

            # Whitelisted, and using a decorator that also removes permissions. Raise warning.
            if view_decorator_name == "allow_anonymous_access":
                warning_message = (
                    f"AdminLtePdq Warning: The {view_type} view '{view_name}' has an '{decorator_name}' "
                    f"{view_perm_type}, but is also in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST. These two effectively "
                    "achieve the same functionality."
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

            # Handle if whitelists don't make sense.
            # Specifically if view is login whitelisted, but permissions are still required in some way.
            # In such a case, the user still requires login for permissions, so the login whitelist does nothing.

            # Determine if permissions are still required and if they are negated properly.
            requires_permissions = STRICT_POLICY or view_decorator_name == "permission_required"
            permission_required_not_negated = not (
                is_perm_whitelisted or view_decorator_name == "allow_without_permissions"
            )

            if (
                # It is login whitelisted AND (See above if)
                # Requires permissions via Strict or decorator
                requires_permissions
                # And that permission requirement is not negated somehow
                and permission_required_not_negated
            ):
                if view_perm_type == "decorator":
                    suggested_decorator = "allow_without_permissions"
                else:
                    suggested_decorator = "AllowWithoutPermissions"

                warning_message = (
                    f"AdminLtePdq Warning: The {view_type} view '{view_name}' is login whitelisted, but the view "
                    "still requires permissions. A user must login to have permissions, so the login whitelist is "
                    "redundant and probably not achieving the desired effect. Correct this by adding the view to "
                    "the permission whitelist setting (ADMINLTE2_STRICT_POLICY_WHITELIST), or by adding the "
                    f"'{suggested_decorator}' {view_perm_type}."
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

        # Handle if view is a permission view but does NOT have permission requirements defined.
        # Determine if is a class-based view.
        is_class_based = view_type == "class-based"
        # Determine if is view that should require permissions
        is_perm_view = (
            # Has decorator or mixin explicitly saying that permission is required.
            view_decorator_name == "permission_required"
            # Or, we are a non-whitelisted, class-based view, with no other mixins, in strict mode.
            or (
                # In Strict Mode
                STRICT_POLICY
                # and is a class based view, which implicitly assumes permission required. (unlike function-based)
                and is_class_based
                # and there is no mixin on the view (We called it decorator regardless of mixin or decorator)
                and not view_decorator_name
                # The view is not whitelisted and thus should have some permissions defined on it.
                and not is_perm_whitelisted
                # The view is not a redirect view
                and not self.verify_redirect_route(view_data["view_class"])
            )
        )
        if (
            # Is a permission view.
            # view_decorator_name == "permission_required"
            is_perm_view
            # And no permission values defined.
            and not view_defines_permissions
        ):
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    f"AdminLtePdq Warning: The {view_type} view '{view_name}' has permission "
                    "requirements, but does not have any permissions set. "
                    "This means that this view is inaccessible until permissions "
                    "are set for the view.\n"
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)
            else:
                # Error if in production mode.
                raise ImproperlyConfigured(RESPONSE_404_PRODUCTION_MESSAGE)

        # Handle if view is permission exempt view, but has permission requirements defined.
        if (
            # Is permission exempt view.
            view_decorator_name == "allow_without_permissions"
            # But permission values are defined.
            and view_defines_permissions
        ):
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    f"AdminLtePdq Warning: The {view_type} view '{view_name}' is permission exempt, "
                    "but has some permission requirements set. "
                    "This means that this view is accessible to anyone authenticated, and the "
                    "permissions are ineffective.\n"
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

    def check_post_login_check_error_states(self, request, view_data):
        """Check for various permission required errors
        TODO: See if there is a way to combine this with the other error states above
        Though it might be hard because this check currently needs to happen
        after we handle redirecting for login required checks."""

        view_missing_decorators = view_data["decorator_name"] not in [
            "login_required",
            "permission_required",
            "allow_anonymous_access",
            "allow_without_permissions",
        ]

        view_type = view_data["view_type"]

        # Handle if using Strict mode and there are no permission set on the view.
        if (
            # In strict mode
            STRICT_POLICY
            # and view is function-based
            and view_type == "function-based"
            # and missing decorators
            and view_missing_decorators
            # and the view is not exempt from requiring permissions
            and not self.view_is_permission_exempt(request, view_data)
            # and the view does not have any one of permissions set
            and not view_data["one_of_permissions"]
            # and the view does not have any full permissions set
            and not view_data["full_permissions"]
            # and not login required
            and not view_data["login_required"]
        ):

            view_name = view_data["view_name"]
            view_perm_type = view_data["view_perm_type"]

            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    "AdminLtePdq Warning: This project is set to run in strict mode, and "
                    f"the {view_type} view '{view_name}' does not have any {view_perm_type}s set. "
                    f"This means that this view is inaccessible until permission {view_perm_type}s "
                    "are set for the view, or the view is added to the "
                    "ADMINLTE2_STRICT_POLICY_WHITELIST setting."
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)
            else:
                # Error if in production mode.
                # Create Django Messages warning.
                messages.warning(request, RESPONSE_403_PRODUCTION_MESSAGE)

    def parse_request_data(self, request):
        """Parses request data and generates dict of calculated values."""

        # Handle if the path is missing the trailing slash.
        if self.should_redirect_with_slash(request):
            path = self.get_full_path_with_slash(request)
        else:
            path = request.path_info

        # Initialize default data structure.
        # This is our fallback if view is not using AdminLtePdq logic.
        data_dict = {
            "path": path,
            "decorator_name": "",
            "allow_anonymous_access": False,
            "login_required": False,
            "allow_without_permissions": False,
            "one_of_permissions": None,
            "full_permissions": None,
        }

        # Try to get the view.
        try:
            resolver = resolve(data_dict["path"])
            data_dict["resolver"] = resolver

            # Determine if view function or view class.
            view_class = getattr(resolver.func, "view_class", None)
            data_dict["view_class"] = view_class

            # Determine universal values.
            app_name = resolver.app_name
            current_url_name = resolver.url_name
            fully_qualified_url_name = f"{app_name}:{current_url_name}"
            data_dict["app_name"] = app_name
            data_dict["current_url_name"] = current_url_name
            data_dict["fully_qualified_url_name"] = fully_qualified_url_name

            # Get extra AdminLtePdq data, if available.
            if view_class:
                # Is class-based view.

                # Get AdminLte class data dict.
                admin_pdq_data = getattr(view_class, "admin_pdq_data", {})
            else:
                # Is function-based view. Get AdminLte function data dict.
                admin_pdq_data = getattr(resolver.func, "admin_pdq_data", {})

            # Process data.
            if view_class:
                # Processing a class-based view.
                # Get class attributes.
                data_dict["view_name"] = view_class.__qualname__
                data_dict["view_type"] = "class-based"
                data_dict["view_perm_type"] = "mixin"

                if admin_pdq_data or STRICT_POLICY:
                    if admin_pdq_data:
                        data_dict["decorator_name"] = admin_pdq_data.get("decorator_name", "")
                        data_dict["allow_anonymous_access"] = admin_pdq_data.get("allow_anonymous_access", False)
                        data_dict["login_required"] = admin_pdq_data.get("login_required", False)
                        data_dict["allow_without_permissions"] = admin_pdq_data.get("allow_without_permissions", False)
                    else:
                        # No Mixins used, use default data_dict as admin_pdq_data and also set on view.
                        # NOTE: We only set this default in class-based views.
                        # Function-based will still need a decorator to set the required perms.
                        admin_pdq_data = data_dict
                        view_class.admin_pdq_data = data_dict

                    # Because we seem unable to get the "updated" class attributes,
                    # and only have access to the original literal class-level values,
                    # we seem unable to rely on the data dict for this.
                    permission_required_one_value = getattr(view_class, "permission_required_one", None)
                    permission_required_value = getattr(view_class, "permission_required", None)

                    # Sanitize values.
                    if permission_required_one_value is not None:
                        # Is populated. Make sure it's the correct format.
                        if isinstance(permission_required_one_value, tuple):
                            # Correct format, pass.
                            pass
                        elif isinstance(permission_required_one_value, list):
                            # Is an iterable type, but not the expected one. Reformat.
                            permission_required_one_value = tuple(permission_required_one_value)
                        else:
                            # Is some other type. Put into a tuple and hope it works out.
                            permission_required_one_value = (permission_required_one_value,)
                    if permission_required_value is not None:
                        # Is populated. Make sure it's the correct format.
                        if isinstance(permission_required_value, tuple):
                            # Correct format, pass.
                            pass
                        elif isinstance(permission_required_value, list):
                            # Is an iterable type, but not the expected one. Reformat.
                            permission_required_value = tuple(permission_required_value)
                        else:
                            # Is some other type. Put into a tuple and hope it works out.
                            permission_required_value = (permission_required_value,)

                    # Save to data dict.
                    data_dict["one_of_permissions"] = permission_required_one_value
                    data_dict["full_permissions"] = permission_required_value

                    # Update data on the class itself.
                    view_class.admin_pdq_data["one_of_permissions"] = data_dict["one_of_permissions"]
                    view_class.admin_pdq_data["full_permissions"] = data_dict["full_permissions"]

            else:
                # Processing a function-based view.
                # Get function attributes.
                data_dict["view_name"] = resolver.func.__qualname__
                data_dict["view_type"] = "function-based"
                data_dict["view_perm_type"] = "decorator"

                # Handle for AdminLtePdq-specific attributes.
                if admin_pdq_data:
                    data_dict["decorator_name"] = admin_pdq_data.get("decorator_name", "")
                    data_dict["allow_anonymous_access"] = admin_pdq_data.get("allow_anonymous_access", False)
                    data_dict["login_required"] = admin_pdq_data.get("login_required", False)
                    data_dict["allow_without_permissions"] = admin_pdq_data.get("allow_without_permissions", False)

                    permission_required_one_value = getattr(resolver.func, "permission_required_one", None)
                    permission_required_value = getattr(resolver.func, "permission_required", None)

                    data_dict["one_of_permissions"] = permission_required_one_value
                    data_dict["full_permissions"] = permission_required_value

        except Http404:
            # Request was 404, not valid page.
            data_dict.update({"resolver": None})

        # Return parsed data.
        return data_dict

    def should_redirect_with_slash(self, request):
        """
        Return True if settings.APPEND_SLASH is True and appending a slash to
        the request path turns an invalid path into a valid one.
        """
        if settings.APPEND_SLASH and not request.path_info.endswith("/"):
            urlconf = getattr(request, "urlconf", None)
            current_is_not_valid = not is_valid_path(request.path_info, urlconf)
            appended_slash_is_valid = is_valid_path(f"{request.path_info}/", urlconf)
            if current_is_not_valid and appended_slash_is_valid:
                view = appended_slash_is_valid.func
                return getattr(view, "should_append_slash", True)
        return False

    def get_full_path_with_slash(self, request):
        """
        Return the full path of the request with a trailing slash appended.

        Raise a RuntimeError if settings.DEBUG is True and request.method is
        DELETE, POST, PUT, or PATCH.
        """
        new_path = request.get_full_path(force_append_slash=True)
        # Prevent construction of scheme relative urls.
        new_path = escape_leading_slashes(new_path)
        if settings.DEBUG and request.method in ("DELETE", "POST", "PUT", "PATCH"):
            raise RuntimeError(
                "You called this URL via %(method)s, but the URL doesn't end "
                "in a slash and you have APPEND_SLASH set. Django can't "
                "redirect to the slash URL while maintaining %(method)s data. "
                "Change your form to point to %(url)s (note the trailing "
                "slash), or set APPEND_SLASH=False in your Django settings."
                % {
                    "method": request.method,
                    "url": request.get_host() + new_path,
                }
            )
        return new_path

    def verify_logged_in(self, request, view_data):
        """Checks to verify User is logged in, for views that require it."""

        # If user is already authenticated, just return true.
        if request.user.is_authenticated:
            return True

        # User not logged in. Still allow request for the following:
        return (
            # View has allow_anonymous decorator.
            view_data["allow_anonymous_access"] is True
            # If url name exists in whitelist.
            or self.is_login_whitelisted(view_data)
            # If passes requirements for custom login hook (defined on a per-project basis).
            or self.login_required_hook(request)
            # If url is for a special route that does not need processing
            or self.is_special_route(view_data)
        )

    def verify_permissions(self, request, view_data):
        """Checks to verify User passes the permission checks, for views that require it."""

        # If user passes perm check, just return true.
        if self.user_passes_perms(request, view_data):
            return True

        # User does not pass perms check. Still allow request for the following:
        return self.view_is_permission_exempt(request, view_data)

    def user_passes_perms(self, request, view_data):
        """Checks to verify User has required permissions, for views that require it."""

        # Default to failing.
        passed_one_of_perms_check = False
        passed_full_perms_check = False
        # Only allow passing if at least one of the types of perms are set on the view.
        # NOTE: This will help ensure that if the PermissionRequired mixin is used, the user must
        # fill out the `permission_required` attribute for the view to pass perm checks.
        at_least_one_set = False

        if view_data["one_of_permissions"]:
            at_least_one_set = True
            # Partial set exists. Must have at least one of any.
            if any(request.user.has_perm(perm) for perm in view_data["one_of_permissions"]):
                passed_one_of_perms_check = True
        else:
            # No partial set to pass. Default to true.
            passed_one_of_perms_check = True

        if view_data["full_permissions"]:
            at_least_one_set = True
            # Full set exists. Must have all.
            if all(request.user.has_perm(perm) for perm in view_data["full_permissions"]):
                passed_full_perms_check = True
        else:
            # No full set to pass. Default to true.
            passed_full_perms_check = True

        # Return true if passes both checks.
        return at_least_one_set and passed_one_of_perms_check and passed_full_perms_check

    def view_is_permission_exempt(self, request, view_data):
        """Return whether the view is exempt from requiring permissions in strict mode."""
        return (
            # View has allow_anonymous decorator.
            view_data["allow_anonymous_access"] is True
            # View has allow_anonymous decorator.
            or view_data["allow_without_permissions"] is True
            # If url name exists in whitelist.
            or self.is_permission_whitelisted(view_data)
            # If is the equivalent of the "Django Admin" app.
            or view_data["app_name"] == "admin"
            # If passes requirements for custom login hook (defined on a per-project basis).
            or self.permission_required_hook(request)
            # If url is for a special route that does not need processing
            or self.is_special_route(view_data)
            # If url is for redirecting.
            or self.verify_redirect_route(view_data["view_class"])
        )

    def is_login_whitelisted(self, view_data):
        """Determines if view is login-whitelisted. Used for login_required mode or strict mode."""

        # Fetch out path and url names and default to blank string.
        path = view_data.get("path", "")
        url_name = view_data.get("current_url_name", "")
        full_url_name = view_data.get("fully_qualified_url_name", "")

        # In "standard" exemption list.
        # Verify whether each path var is not an empty string and is in the whitelist.
        whitelisted_directly = (
            (path and path in LOGIN_EXEMPT_WHITELIST)
            or (url_name and url_name in LOGIN_EXEMPT_WHITELIST)
            or (full_url_name and full_url_name in LOGIN_EXEMPT_WHITELIST)
        )

        # In "app-wide" exemption list.
        # Verify whether path var is not an empty string and is in the fuzzy whitelist.
        whitelisted_fuzzy = False
        for entry in LOGIN_EXEMPT_FUZZY_WHITELIST:
            if path and path.startswith(entry):
                whitelisted_fuzzy = True

        # Return if either whitelisted directly or via fuzzy logic
        return whitelisted_directly or whitelisted_fuzzy

    def is_permission_whitelisted(self, view_data):
        """Determines if view is permission-whitelisted. Used for strict mode."""

        # Fetch out path and url names and default to blank string.
        path = view_data.get("path", "")
        url_name = view_data.get("current_url_name", "")
        full_url_name = view_data.get("fully_qualified_url_name", "")

        # In "standard" exemption list.
        # Verify whether each path var is not an empty string and is in the whitelist.
        whitelisted_directly = (
            (path and path in STRICT_POLICY_WHITELIST)
            or (url_name and url_name in STRICT_POLICY_WHITELIST)
            or (full_url_name and full_url_name in STRICT_POLICY_WHITELIST)
        )

        # In "app-wide" exemption list.
        # Verify whether path var is not an empty string and is in the fuzzy whitelist.
        whitelisted_fuzzy = False
        for entry in STRICT_POLICY_FUZZY_WHITELIST:
            if path and path.startswith(entry):
                whitelisted_fuzzy = True

        # Return if either whitelisted directly or via fuzzy logic
        return whitelisted_directly or whitelisted_fuzzy

    def login_required_hook(self, request):
        """Hook that can be overridden in subclasses to add additional ways
        to pass the login required criteria. Should return either True or False."""
        return False

    def permission_required_hook(self, request):
        """Hook that can be overridden in subclasses to add additional ways
        to pass the login required criteria. Should return either True or False."""
        return False

    def is_special_route(self, view_data):
        """Check if the path is a special route that should forego checks"""

        path = view_data["path"]

        return (
            # If url is for favicon
            self.verify_favicon_route(path)
            # If url is for static, as defined in settings.
            or self.verify_static_route(path)
            # If url is for media, as defined in settings.
            or self.verify_media_route(path)
            # If url is for websockets, as defined in settings.
            or self.verify_websocket_route(path)
        )

    def verify_favicon_route(self, path):
        """Verify that the path of the request is not a favicon request."""
        return path == "/favicon.ico"

    def verify_static_route(self, path):
        """Verify that the path of the request is not a STATIC URL"""
        return_val = False
        if STATIC_ROUTE and STATIC_ROUTE != "/":
            return_val = path.startswith(STATIC_ROUTE)
        return return_val

    def verify_media_route(self, path):
        """Verify that the path of the request is not a MEDIA URL"""
        return_val = False
        if MEDIA_ROUTE and MEDIA_ROUTE != "/":
            return_val = path.startswith(MEDIA_ROUTE)
        return return_val

    def verify_websocket_route(self, path):
        """Verify that the path of the request is not a WEBSOCKET URL"""
        return_val = False
        if WEBSOCKET_ROUTE and WEBSOCKET_ROUTE != "/":
            return_val = path.startswith(WEBSOCKET_ROUTE)
        return return_val

    def verify_redirect_route(self, view_class):
        """Verify that the view class is a RedirectView"""
        return view_class is not None and view_class == RedirectView
