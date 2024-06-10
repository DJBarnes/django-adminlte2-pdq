"""Django AdminLTE2 default Constants."""

# Third-Party Imports.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# Imports that may not be accessible, depending on local python environment setup.
try:
    from colorama import Back, Fore, Style

    COLORAMA_PRESENT = True
except ImportError:
    COLORAMA_PRESENT = False


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


# Known routes that should never have a permission check done.
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
# List of known routes that should never require permissions to access.
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


# Date Time Picker Widgets to use. Valid values are 'native', 'jquery', 'bootstrap'
DATETIME_WIDGET = getattr(settings, "ADMINLTE2_DATETIME_WIDGET", "native")
DATE_WIDGET = getattr(settings, "ADMINLTE2_DATE_WIDGET", "native")
TIME_WIDGET = getattr(settings, "ADMINLTE2_TIME_WIDGET", "native")


# What required field indicators should be used on a rendered form
BOLD_REQUIRED_FIELDS = getattr(settings, "ADMINLTE2_BOLD_REQUIRED_FIELDS", True)
ASTERISK_REQUIRED_FIELDS = getattr(settings, "ADMINLTE2_ASTERISK_REQUIRED_FIELDS", True)


# Debug output values. Use for internal project debugging.
TEXT_BLUE = "{0}{1}{2}".format(Fore.BLUE, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else ""
TEXT_CYAN = "{0}{1}{2}".format(Fore.CYAN, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else ""
TEXT_GREEN = "{0}{1}{2}".format(Fore.GREEN, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else ""
TEXT_PURPLE = "{0}{1}{2}".format(Fore.MAGENTA, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else ""
TEXT_RED = "{0}{1}{2}".format(Fore.RED, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else ""
TEXT_RESET = Style.RESET_ALL if COLORAMA_PRESENT else ""
TEXT_YELLOW = "{0}{1}{2}".format(Fore.YELLOW, Back.RESET, Style.NORMAL) if COLORAMA_PRESENT else ""

# Optionally display package-wide debug printing.
SHOW_DEBUG_PRINT = getattr(settings, "ADMINLTE2_SHOW_DEBUG_PRINT", False)
