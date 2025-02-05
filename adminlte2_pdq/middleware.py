"""Django-AdminLTE2-PDQ Middleware"""

# System Imports.
import logging
import warnings

# Third-Party Imports.
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import resolve
from django.views.generic.base import RedirectView

# Internal Imports.
from .constants import (
    LOGIN_REQUIRED,
    LOGIN_EXEMPT_WHITELIST,
    LOGIN_EXEMPT_FUZZY_WHITELIST,
    RESPONSE_403_DEBUG_MESSAGE,
    RESPONSE_403_PRODUCTION_MESSAGE,
    RESPONSE_404_DEBUG_MESSAGE,
    RESPONSE_404_PRODUCTION_MESSAGE,
    STRICT_POLICY,
    STRICT_POLICY_WHITELIST,
    STRICT_POLICY_FUZZY_WHITELIST,
    LOGIN_URL,
    HOME_ROUTE,
    MEDIA_ROUTE,
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

        # Ensure user object is accessible for Authentication checks.
        if not hasattr(request, "user"):
            # Django SessionMiddleware is required to use Django AuthenticationMiddleware.
            # Django AuthenticationMiddleware is what gives us access to user object in request.
            # Django MessageMiddleware is required to display messages to user on middleware failure for a view.
            raise ImportError(
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
        self.check_error_states(request, view_data)

        # Handle if view requires user login to proceed.
        # Determined by combination of the ADMINLTE2_USE_LOGIN_REQUIRED and ADMINLTE2_LOGIN_EXEMPT_WHITELIST settings.
        if (LOGIN_REQUIRED or view_data["login_required"]) and not self.verify_logged_in(request, view_data):
            # User not logged in and view requires login to access.

            # Redirect to login page.
            return redirect(LOGIN_URL + f"?next={request.path}")

        self.check_for_should_display_redirect_message(request, view_data)

        # Handle if view requires specific user permissions to proceed.
        # Determined by combination of the ADMINLTE2_USE_STRICT_POLICY and ADMINLTE2_STRICT_POLICY_WHITELIST settings.
        if (
            # Is STRICT mode.
            STRICT_POLICY
            # Is not a decorator allowing lowered permission checks.
            and view_data["decorator_name"] not in ["allow_anonymous_access", "allow_without_permissions"]
            # Fails general checks for everything else.
            and not self.verify_strict_mode_permission_set(request, view_data)
        ):

            # Redirect to home route.
            return redirect(HOME_ROUTE)

        # User passed all tests, return requested response.
        response = self.get_response(request)
        if view_data["decorator_name"]:
            response.admin_pdq_data = view_data

        return response

    def check_error_states(self, request, view_data):
        """Check for various conflicting decorator/mixin states, raise error upon finding any."""

        # Check if view is in any whitelists.
        is_login_whitelisted = self.is_login_whitelisted(view_data)
        is_perm_whitelisted = self.is_permission_whitelisted(view_data)
        view_requires_permissions = bool(view_data["one_of_permissions"]) or bool(view_data["full_permissions"])

        # Handle if using login_required decorator within STRICT mode or Login Required mode.
        if (STRICT_POLICY or LOGIN_REQUIRED) and view_data["decorator_name"] == "login_required":

            # Determine some error message values based on mode.
            if STRICT_POLICY:
                mode_type = "STRICT"
                mode_text = "login and permissions are"
                if view_data["view_perm_type"] == "decorator":
                    decorator_name = "login_required"
                    similar_decorators = "'allow_anonymous_access' or 'allow_without_permissions'"
                else:
                    decorator_name = "LoginRequired"
                    similar_decorators = "'AllowAnonymousAccess' or 'AllowWithoutPermissions'"
                pluralize = "s"
            else:
                mode_type = "LOGIN REQUIRED"
                mode_text = "login is"
                if view_data["view_perm_type"] == "decorator":
                    decorator_name = "login_required"
                    similar_decorators = "'allow_anonymous_access'"
                else:
                    decorator_name = "LoginRequired"
                    similar_decorators = "'AllowAnonymousAccess'"
                pluralize = ""

            # Display error message.
            error_message = (
                "AdminLtePdq Error: The '{decorator_name}' {view_perm_type} is not supported in AdminLtePdq "
                "{mode_type} mode. Having {mode_type} mode on implicitly assumes {mode_text} required "
                "for all views that are not in a whitelist setting."
                "\n\n"
                "Also consider the {similar_decorators} {view_perm_type}{pluralize}."
            ).format(
                decorator_name=decorator_name,
                mode_type=mode_type,
                mode_text=mode_text,
                similar_decorators=similar_decorators,
                view_perm_type=view_data["view_perm_type"],
                pluralize=pluralize,
            )
            raise ImproperlyConfigured(error_message)

        # Handle if using allow_anonymous_access or allow_without_permissions decorator in mode that doesn't make sense.
        if (
            # Using allow_anonymous or allow_without_permissions in Loose mode.
            (
                (not STRICT_POLICY and not LOGIN_REQUIRED)
                and view_data["decorator_name"] in ["allow_anonymous_access", "allow_without_permissions"]
            )
            # Or using allow_without_permissions outside of strict mode.
            or (not STRICT_POLICY and view_data["decorator_name"] == "allow_without_permissions")
        ):
            # Determine some error message values based on mode.
            if not STRICT_POLICY and not LOGIN_REQUIRED:
                mode_type = "LOOSE"
            else:
                mode_type = "LOGIN REQUIRED"

            if view_data["view_perm_type"] == "decorator":
                decorator_name = view_data["decorator_name"]
            else:
                decorator_name = view_data["decorator_name"].replace("_", " ").title().replace(" ", "")

            # Display error message.
            error_message = (
                "AdminLtePdq Error: The '{decorator_name}' {view_perm_type} is not supported in AdminLtePdq "
                "{mode_type} mode. This {view_perm_type} only exists for clarity of permission access in STRICT mode."
            ).format(
                decorator_name=decorator_name,
                view_perm_type=view_data["view_perm_type"],
                mode_type=mode_type,
            )
            raise ImproperlyConfigured(error_message)

        # Handle if view is strict-mode whitelisted but using a decorator/mixin state that doesn't make sense.
        if is_perm_whitelisted:
            # Whitelisted, yet using a decorator that requires permissions. Raise error.
            if view_data["decorator_name"] == "permission_required":
                raise ImproperlyConfigured(
                    (
                        "AdminLtePdq Error: The {view_type} view '{view_name}' has a permission {view_perm_type}, "
                        "but is in the ADMINLTE2_STRICT_POLICY_WHITELIST setting. Please remove one."
                    ).format(
                        view_type=view_data["view_type"],
                        view_name=view_data["view_name"],
                        view_perm_type=view_data["view_perm_type"],
                    )
                )

            # Whitelisted, and using a decorator that also removes permissions. Raise warning.
            if view_data["decorator_name"] == "allow_without_permissions":

                if view_data["view_perm_type"] == "decorator":
                    decorator_name = "allow_without_permissions"
                else:
                    decorator_name = "AllowWithoutPermissions"

                warning_message = (
                    "AdminLtePdq Warning: The {view_type} view '{view_name}' has an '{decorator_name}' "
                    "{view_perm_type}, but is also in the ADMINLTE2_STRICT_POLICY_WHITELIST. These two effectively "
                    "achieve the same functionality."
                ).format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                    view_perm_type=view_data["view_perm_type"],
                    decorator_name=decorator_name,
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

        # Handle if view is login whitelisted but using a decorator/mixin state that doesn't make sense.
        if is_login_whitelisted:
            # Whitelisted, yet using a decorator that requires login. Raise error.
            if view_data["decorator_name"] == "login_required":

                if view_data["view_perm_type"] == "decorator":
                    decorator_name = "login_required"
                else:
                    decorator_name = "LoginRequired"

                raise ImproperlyConfigured(
                    (
                        "AdminLtePdq Error: The {view_type} view '{view_name}' has a '{decorator_name}' "
                        "{view_perm_type}, but is in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST setting. Please remove one."
                    ).format(
                        view_type=view_data["view_type"],
                        view_name=view_data["view_name"],
                        view_perm_type=view_data["view_perm_type"],
                        decorator_name=decorator_name,
                    )
                )

            # Whitelisted, and using a decorator that also removes permissions. Raise warning.
            if view_data["decorator_name"] == "allow_anonymous_access":

                if view_data["view_perm_type"] == "decorator":
                    decorator_name = "allow_anonymous_access"
                else:
                    decorator_name = "AllowAnonymousAccess"

                warning_message = (
                    "AdminLtePdq Warning: The {view_type} view '{view_name}' has an '{decorator_name}' "
                    "{view_perm_type}, but is also in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST. These two effectively "
                    "achieve the same functionality."
                ).format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                    view_perm_type=view_data["view_perm_type"],
                    decorator_name=decorator_name,
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

            # Handle if whitelists don't make sense.
            # Specifically if view is login whitelisted, but permissions are still required in some way.
            # In such a case, the user still requires login for permissions, so the login whitelist does nothing.
            if (
                # Not in a state that would invalidate this.
                not (is_perm_whitelisted or view_data["decorator_name"] == "allow_without_permissions")
                # and IS on one of the states that we're looking for.
                and (
                    # Is strict policy
                    STRICT_POLICY
                    # Or using a permission decorator.
                    or view_data["decorator_name"] == "permission_required"
                )
            ):
                if view_data["view_perm_type"] == "decorator":
                    decorator_name = "allow_without_permissions"
                else:
                    decorator_name = "AllowWithoutPermissions"

                warning_message = (
                    "AdminLtePdq Warning: The {view_type} view '{view_name}' is login whitelisted, but the view "
                    "still requires permissions. A user must login to have permissions, so the login whitelist is "
                    "redundant and probably not achieving the desired effect. Correct this by adding the view to "
                    "the permission whitelist setting (ADMINLTE2_STRICT_POLICY_WHITELIST), or by adding the "
                    "'{decorator_name}' {view_perm_type}."
                ).format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                    view_perm_type=view_data["view_perm_type"],
                    decorator_name=decorator_name,
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

        # Handle if view is a permission view but does NOT have permission requirements defined.
        if (
            # Is a permission view.
            view_data["decorator_name"] == "permission_required"
            # And no permission values defined.
            and not view_requires_permissions
        ):
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    "AdminLtePdq Warning: The {view_type} view '{view_name}' has permission "
                    "requirements, but does not have any permissions set. "
                    "This means that this view is inaccessible until permissions "
                    "are set for the view.\n"
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                ).format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
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
            view_data["decorator_name"] == "allow_without_permissions"
            # But permission values are defined.
            and view_requires_permissions
        ):
            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = (
                    "AdminLtePdq Warning: The {view_type} view '{view_name}' is permission exempt, "
                    "but has some permission requirements set. "
                    "This means that this view is accessible to anyone authenticated, and the "
                    "permissions are ineffective.\n"
                    "\n\n"
                    "For further information, please see the docs: "
                    "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
                ).format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)

    def parse_request_data(self, request):
        """Parses request data and generates dict of calculated values."""

        # Initialize default data structure.
        # This is our fallback if view is not using AdminLtePdq logic.
        data_dict = {
            "path": request.path,
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
                # Is class-based view. Get class data dict.
                pdq_data = getattr(view_class, "admin_pdq_data", {})
            else:
                # Is function-based view. Get function data dict.
                pdq_data = getattr(resolver.func, "admin_pdq_data", {})

            # Process data.
            if view_class:
                # Get class attributes.
                data_dict["view_name"] = view_class.__qualname__
                data_dict["view_type"] = "class-based"
                data_dict["view_perm_type"] = "mixin"

                # Handle for AdminLtePdq-specific attributes.
                if pdq_data:
                    data_dict["decorator_name"] = pdq_data.get("decorator_name", "")
                    data_dict["allow_anonymous_access"] = pdq_data.get("allow_anonymous_access", False)
                    data_dict["login_required"] = pdq_data.get("login_required", False)
                    data_dict["allow_without_permissions"] = pdq_data.get("allow_without_permissions", False)

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
                # Get function attributes.
                data_dict["view_name"] = resolver.func.__qualname__
                data_dict["view_type"] = "function-based"
                data_dict["view_perm_type"] = "decorator"

                # Handle for AdminLtePdq-specific attributes.
                if pdq_data:
                    data_dict["decorator_name"] = pdq_data.get("decorator_name", "")
                    data_dict["allow_anonymous_access"] = pdq_data.get("allow_anonymous_access", False)
                    data_dict["login_required"] = pdq_data.get("login_required", False)
                    data_dict["allow_without_permissions"] = pdq_data.get("allow_without_permissions", False)
                    data_dict["one_of_permissions"] = pdq_data.get("one_of_permissions", None)
                    data_dict["full_permissions"] = pdq_data.get("full_permissions", None)

        except Http404:
            data_dict.update({"resolver": None})

        # Return parsed data.
        return data_dict

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
            # If path exists in whitelist.
            or view_data["path"] in LOGIN_EXEMPT_WHITELIST
            # If passes requirements for custom login hook (defined on a per-project basis).
            or self.login_required_hook(request)
            # If url is for media, as defined in settings.
            or self.verify_media_route(view_data["path"])
            # If url is for websockets, as defined in settings.
            or self.verify_websocket_route(view_data["path"])
        )

    def verify_has_perms(self, request, view_data):
        """Checks to verify User has required permissions, for views that require it."""

        # Default to failing.
        passed_one_of_perms_check = False
        passed_full_perms_check = False

        if view_data["one_of_permissions"]:
            # Partial set exists. Must have at least one of any.
            if any(request.user.has_perm(perm) for perm in view_data["one_of_permissions"]):
                passed_one_of_perms_check = True
        else:
            # No partial set to pass. Default to true.
            passed_one_of_perms_check = True

        if view_data["full_permissions"]:
            # Full set exists. Must have all.
            if all(request.user.has_perm(perm) for perm in view_data["full_permissions"]):
                passed_full_perms_check = True
        else:
            # No full set to pass. Default to true.
            passed_full_perms_check = True

        # Return true if passes both checks.
        return passed_one_of_perms_check and passed_full_perms_check

    def verify_strict_mode_permission_set(self, request, view_data):
        """Verify view access based on permission/login requirements on the view object.

        :return: False if user cannot access view as per Strict Mode policy | True otherwise.
        """
        exempt = False

        # Proceed if is a proper view (not a "404 not found").
        if view_data["resolver"]:

            # Determine if request url is exempt. Is the case for the following:
            if (
                # If url name exists in whitelist.
                self.is_permission_whitelisted(view_data)
                # If path exists in whitelist.
                or view_data["path"] in STRICT_POLICY_WHITELIST
                # If is the equivalent of the "Django Admin" app.
                or view_data["app_name"] == "admin"
                # If url is for media, as defined in settings.
                or self.verify_media_route(view_data["path"])
                # If url is for websockets, as defined in settings.
                or self.verify_websocket_route(view_data["path"])
                # If url is for redirecting, as defined in settings.
                or self.verify_redirect_route(view_data["view_class"])
            ):
                # One or more conditions passed for url being exempt from checks.
                exempt = True

            # Allow request if any of the checks passed.
            if (
                # View is exempt from requirements.
                exempt
                # OR view didn't require permissions due to decorators.
                or view_data["decorator_name"] in ["allow_anonymous_access", "allow_without_permissions"]
                # OR user had the correct permissions.
                # For now, this check technically only works because we don't set these values
                # on the redirect-to-login requests. So they're populated if the user passes
                # decorator/mixin checks, and unpopulated otherwise.
                #
                # If we ever start populating these values on all requests, then
                # this logic will no longer work.
                or view_data["login_required"]
                or view_data["one_of_permissions"]
                or view_data["full_permissions"]
            ):
                return True

            # Decorator/Mixin failed checks, or Login Required not set.
            # Add messages, warnings, and return False.
            # TODO: Upon closer examination, this looks like older logic (likely from before any major reworks)
            #   which was never moved. This section effectively provides warning messages/redirects, if in
            #   strict mode and the view doesn't have proper permissions set.
            #
            #   This logic no longer really makes sense here, as this function looks to be more about
            #   validating the user permissions in strict mode, rather than checking that the view itself
            #   is correctly defined.
            #
            #   Long-term, this should probably be moved to the `check_error_states()` function,
            #   but for now tests somehow seem to pass and time is limited, so leaving here for now.
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
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                    view_perm_type=view_data["view_perm_type"],
                )
                # Create console warning message.
                warnings.warn(warning_message, RuntimeWarning)
                # Create Django Messages warning.
                messages.warning(request, warning_message)
            else:
                # Error if in production mode.
                # Create Django Messages warning.
                messages.warning(request, RESPONSE_404_PRODUCTION_MESSAGE)

        # If we made it this far, then failed all checks, return False.
        return False

    def check_for_should_display_redirect_message(self, request, view_data):
        """When redirecting to home (due to failure on permission checks), we want a helper message in debug mode.

        This logic checks for that.
        Note that STRICT MODE is handled elsewhere, so this does not have to handle for that.
        """

        # Check if state where user failed permissions check.
        if (
            # If url name does not exist in whitelist.
            not self.is_permission_whitelisted(view_data)
            # If path does not exist in whitelist.
            and not view_data["path"] in STRICT_POLICY_WHITELIST
            # If user fails perm checks.
            and not self.verify_has_perms(request, view_data)
        ):

            if settings.DEBUG:
                # Warning if in development mode.
                warning_message = RESPONSE_403_DEBUG_MESSAGE.format(
                    view_type=view_data["view_type"],
                    view_name=view_data["view_name"],
                )
                # Create Django Messages warning.
                messages.warning(request, warning_message)

            else:
                warning_message = RESPONSE_403_PRODUCTION_MESSAGE
                # Create Django Messages warning.
                messages.warning(request, warning_message)

    def is_login_whitelisted(self, view_data):
        """Determines if view is login-whitelisted. Used for login_required mode or strict mode."""

        try:
            return bool(
                # In "app-wide" exemption list.
                view_data["path"].startswith(LOGIN_EXEMPT_FUZZY_WHITELIST)
                # In "standard" exemption list.
                or view_data["current_url_name"] in LOGIN_EXEMPT_WHITELIST
                or view_data["fully_qualified_url_name"] in LOGIN_EXEMPT_WHITELIST
            )
        except KeyError:
            return False

    def is_permission_whitelisted(self, view_data):
        """Determines if view is permission-whitelisted. Used for strict mode."""

        try:
            return bool(
                # In "app-wide" exemption list.
                view_data["path"].startswith(STRICT_POLICY_FUZZY_WHITELIST)
                # In "standard" exemption list.
                or view_data["current_url_name"] in STRICT_POLICY_WHITELIST
                or view_data["fully_qualified_url_name"] in STRICT_POLICY_WHITELIST
            )
        except KeyError:
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
        return view_class and view_class == RedirectView
