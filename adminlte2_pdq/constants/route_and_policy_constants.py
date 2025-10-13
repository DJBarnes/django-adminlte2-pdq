"""
Constants related to package whitelisting.
"""

# Third-Party Imports.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy


# Known routes that should never require being logged in.
LOGIN_URL = getattr(settings, "LOGIN_URL", reverse_lazy("login"))
LOGOUT_URL = getattr(settings, "LOGOUT_URL", reverse_lazy("logout"))
PWD_RESET_ROUTE = getattr(settings, "PWD_RESET_ROUTE", "password_reset")
PWD_RESET_DONE_ROUTE = getattr(settings, "PWD_RESET_DONE_ROUTE", "password_reset_done")
PWD_RESET_CONFIRM_ROUTE = getattr(settings, "PWD_RESET_CONFIRM_ROUTE", "password_reset_confirm")
PWD_RESET_COMPLETE_ROUTE = getattr(settings, "PWD_RESET_COMPLETE_ROUTE", "password_reset_complete")
REGISTER_ROUTE = getattr(settings, "REGISTER_ROUTE", "adminlte2_pdq:register")
MEDIA_ROUTE = getattr(settings, "MEDIA_URL", "/media/")
STATIC_ROUTE = getattr(settings, "STATIC_URL", "/static/")
WEBSOCKET_ROUTE = getattr(settings, "WEBSOCKET_URL", "/ws/")


# Known routes that should never require a permission check.
HOME_ROUTE = getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home")
PWD_CHANGE = getattr(settings, "PWD_CHANGE", "password_change")
PWD_CHANGE_DONE = getattr(settings, "PWD_CHANGE_DONE", "password_change_done")


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

# Project-wide serve 404 whitelist.
# These take either a exact url or url base of urls that should serve a 404
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
    if not strict_policy and getattr(settings, "ADMINLTE2_STRICT_POLICY_WHITELIST", []) != []:
        # Permission whitelisted, but outside of STRICT mode.
        raise ImproperlyConfigured("Can't use ADMINLTE2_STRICT_POLICY_WHITELIST outside of STRICT_POLICY = True.")
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
    if not login_policy and getattr(settings, "ADMINLTE2_LOGIN_EXEMPT_WHITELIST", []) != []:
        # Login whitelisted, but outside of LOGIN_REQUIRED mode.
        raise ImproperlyConfigured("Can't use ADMINLTE2_LOGIN_EXEMPT_WHITELIST outside of LOGIN_REQUIRED = True.")
    # Return the strict policy
    return login_policy


# Get whether or not we are using STRICT_POLICY and LOGIN_REQUIRED.
STRICT_POLICY = get_strict_policy()
LOGIN_REQUIRED = get_login_required_policy(STRICT_POLICY)
