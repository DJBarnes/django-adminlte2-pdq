"""
Constants related to package whitelisting.
"""

# System Imports.
import warnings

# Third-Party Imports.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy


def get_renamed_setting(name, old_name, default):
    """Get a setting that was renamed, falling back to its old name with a deprecation warning."""
    if hasattr(settings, name):
        return getattr(settings, name)
    if hasattr(settings, old_name):
        warnings.warn(
            f"The {old_name} setting is deprecated and will be removed in a future release. Rename it to {name}.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(settings, old_name)
    return default


# Known routes that should never require being logged in.
# LOGIN_URL, MEDIA_URL, and STATIC_URL are Django's own settings. The others are this package's.
LOGIN_URL = getattr(settings, "LOGIN_URL", reverse_lazy("login"))
LOGOUT_URL = get_renamed_setting("ADMINLTE2_LOGOUT_URL", "LOGOUT_URL", reverse_lazy("logout"))
PWD_RESET_ROUTE = get_renamed_setting("ADMINLTE2_PASSWORD_RESET_ROUTE", "PWD_RESET_ROUTE", "password_reset")
PWD_RESET_DONE_ROUTE = get_renamed_setting(
    "ADMINLTE2_PASSWORD_RESET_DONE_ROUTE", "PWD_RESET_DONE_ROUTE", "password_reset_done"
)
PWD_RESET_CONFIRM_ROUTE = get_renamed_setting(
    "ADMINLTE2_PASSWORD_RESET_CONFIRM_ROUTE", "PWD_RESET_CONFIRM_ROUTE", "password_reset_confirm"
)
PWD_RESET_COMPLETE_ROUTE = get_renamed_setting(
    "ADMINLTE2_PASSWORD_RESET_COMPLETE_ROUTE", "PWD_RESET_COMPLETE_ROUTE", "password_reset_complete"
)
REGISTER_ROUTE = get_renamed_setting("ADMINLTE2_REGISTER_ROUTE", "REGISTER_ROUTE", "adminlte2_pdq:register")
MEDIA_ROUTE = getattr(settings, "MEDIA_URL", "/media/")
STATIC_ROUTE = getattr(settings, "STATIC_URL", "/static/")
WEBSOCKET_ROUTE = get_renamed_setting("ADMINLTE2_WEBSOCKET_URL", "WEBSOCKET_URL", "/ws/")


# Known routes that should never require a permission check.
HOME_ROUTE = getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home")
PWD_CHANGE = get_renamed_setting("ADMINLTE2_PASSWORD_CHANGE_ROUTE", "PWD_CHANGE", "password_change")
PWD_CHANGE_DONE = get_renamed_setting("ADMINLTE2_PASSWORD_CHANGE_DONE_ROUTE", "PWD_CHANGE_DONE", "password_change_done")


# List of known routes that should never require being logged in.
LOGIN_EXEMPT_WHITELIST = [
    LOGIN_URL,
    LOGOUT_URL,
    PWD_RESET_ROUTE,
    PWD_RESET_DONE_ROUTE,
    PWD_RESET_CONFIRM_ROUTE,
    PWD_RESET_COMPLETE_ROUTE,
    REGISTER_ROUTE,
]
# List of known routes that should never require a permission check.
STRICT_POLICY_WHITELIST = [
    HOME_ROUTE,
    PWD_CHANGE,
    PWD_CHANGE_DONE,
] + LOGIN_EXEMPT_WHITELIST


# Add any user defined list of exempt urls to the constant.
LOGIN_EXEMPT_WHITELIST += getattr(settings, "ADMINLTE2_LOGIN_EXEMPT_WHITELIST", [])
STRICT_POLICY_WHITELIST += getattr(settings, "ADMINLTE2_STRICT_POLICY_WHITELIST", [])


# Project-wide whitelists.
# These take a url base, and whitelist any urls that stem from said base.
# For example, this is required to make the Django Debug Toolbar function.
LOGIN_EXEMPT_FUZZY_WHITELIST = tuple(
    getattr(
        settings,
        "ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST",
        [],
    )
)
STRICT_POLICY_FUZZY_WHITELIST = tuple(
    getattr(
        settings,
        "ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST",
        [],
    )
)

# Project-wide serve 403 whitelist.
# These take either an exact url or url base of urls that should serve a 403
# and not redirect to the home page when strict mode is enabled.
# Useful for specific url patterns that will handle authentication and authorization manually.

# EX: You may create an app for apis in your project and all of them are located
# at an endpoint such as "api/". In this case, when there is a 403, you do not want
# to do the default behavior of sending a redirect to the Home page of the site.
# You instead probably want to create some sort of JSON response that conveys the
# problem to the user. So, by adding "api/" to this list, all urls that start with "api/"
# will be handled by raising a PermissionDenied exception when a 403 occurs
# rather than redirecting to home. Which can be manually handled by code that you write.
STRICT_POLICY_SERVE_403_FUZZY_WHITELIST = tuple(
    getattr(
        settings,
        "ADMINLTE2_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST",
        [],
    )
)

# Project-wide serve 404 whitelist.
# These take either an exact url or url base of urls that should serve a 404
# and not redirect to the home page when strict mode is enabled.
# Useful for uncontrollable requests that come from a browser or an extension.

# EX: When using Chrome and the dev tools are open, there will be an automatic
# request to your Django app for ".well-known/appspecific/com.chrome.devtools.json"
# which may not exist. Redirecting to Home for that request seems wasteful.
# So, that value or similar ones can be added to this whitelist to make sure
# that they serve back a 404 instead of redirecting to Home.
STRICT_POLICY_SERVE_404_FUZZY_WHITELIST = tuple(
    getattr(
        settings,
        "ADMINLTE2_STRICT_POLICY_SERVE_404_FUZZY_WHITELIST",
        [],
    )
)

# NOTE: This below logic is in functions vs right at module level so that it can be properly tested.
# They are however called below at module level to ensure that they get run on import.


def get_strict_policy():
    """Get the STRICT_POLICY constant value"""

    strict_policy = getattr(settings, "ADMINLTE2_USE_STRICT_POLICY", False)

    # Verify state of whitelist values against chosen policy.
    for whitelist in ("ADMINLTE2_STRICT_POLICY_WHITELIST", "ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST"):
        if not strict_policy and getattr(settings, whitelist, None):
            # Permission whitelisted, but outside of STRICT mode.
            raise ImproperlyConfigured(f"Can't use {whitelist} outside of STRICT_POLICY = True.")

    # Return the strict policy
    return strict_policy


def get_login_required_policy(strict_policy):
    """Get the LOGIN_REQUIRED_POLICY constant value"""

    # Get the login policy from the settings.
    login_policy = getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False)

    # NOTE: By nature of what STRICT_POLICY is, it implicitly means login is required.
    if strict_policy:
        login_policy = True

    # Verify state of whitelist values against chosen policy.
    for whitelist in ("ADMINLTE2_LOGIN_EXEMPT_WHITELIST", "ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST"):
        if not login_policy and getattr(settings, whitelist, None):
            # Login whitelisted, but outside of LOGIN_REQUIRED mode.
            raise ImproperlyConfigured(f"Can't use {whitelist} outside of LOGIN_REQUIRED = True.")

    # Return the strict policy
    return login_policy


# Get whether or not we are using STRICT_POLICY and LOGIN_REQUIRED.
STRICT_POLICY = get_strict_policy()
LOGIN_REQUIRED = get_login_required_policy(STRICT_POLICY)
