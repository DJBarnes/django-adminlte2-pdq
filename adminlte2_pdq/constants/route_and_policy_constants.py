"""
Constants related to package whitelisting.
"""

# Third-Party Imports.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# Known routes that should never require being logged in.
LOGIN_URL = getattr(settings, "LOGIN_URL", "/accounts/login")
LOGOUT_ROUTE = getattr(settings, "LOGOUT_ROUTE", "logout")
PWD_RESET_ROUTE = getattr(settings, "PWD_RESET_ROUTE", "password_reset")
PWD_RESET_DONE_ROUTE = getattr(settings, "PWD_RESET_DONE_ROUTE", "password_reset_done")
PWD_RESET_CONFIRM_ROUTE = getattr(settings, "PWD_RESET_CONFIRM_ROUTE", "password_reset_confirm")
PWD_RESET_COMPLETE_ROUTE = getattr(settings, "PWD_RESET_COMPLETE_ROUTE", "password_reset_complete")
REGISTER_ROUTE = getattr(settings, "REGISTER_ROUTE", "adminlte2_pdq:register")
MEDIA_ROUTE = getattr(settings, "MEDIA_URL", "/media/")
WEBSOCKET_ROUTE = getattr(settings, "WEBSOCKET_URL", "/ws/")


# Known routes that should never require a permission check.
HOME_ROUTE = getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home")
PWD_CHANGE = getattr(settings, "PWD_CHANGE", "password_change")
PWD_CHANGE_DONE = getattr(settings, "PWD_CHANGE_DONE", "password_change_done")


# List of known routes that should never require being logged in.
LOGIN_EXEMPT_WHITELIST = [
    LOGIN_URL,
    LOGOUT_ROUTE,
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


# Get whether or not we are using LoginRequired and PermissionRequired.
# NOTE: By nature of what STRICT_POLICY is, it implicitly means login is required.
STRICT_POLICY = getattr(settings, "ADMINLTE2_USE_STRICT_POLICY", False)
if STRICT_POLICY:
    LOGIN_REQUIRED = True
else:
    LOGIN_REQUIRED = getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False)


# Verify state of whitelist values against chosen policy.
if not STRICT_POLICY and getattr(settings, "ADMINLTE2_STRICT_POLICY_WHITELIST", []) != []:
    # Permission whitelisted, but outside of STRICT mode.
    raise ImproperlyConfigured("Can't use ADMINLTE2_STRICT_POLICY_WHITELIST outside of STRICT_POLICY = True.")
if not LOGIN_REQUIRED and getattr(settings, "ADMINLTE2_LOGIN_EXEMPT_WHITELIST", []) != []:
    # Login whitelisted, but outside of LOGIN_REQUIRED mode.
    raise ImproperlyConfigured("Can't use ADMINLTE2_LOGIN_EXEMPT_WHITELIST outside of LOGIN_REQUIRED = True.")
