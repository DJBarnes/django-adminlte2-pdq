"""Imports to make this folder behave like a single file."""

# Constants related to general package settings.
from .general_constants import (
    DATETIME_WIDGET,
    DATE_WIDGET,
    TIME_WIDGET,
    BOLD_REQUIRED_FIELDS,
    ASTERISK_REQUIRED_FIELDS,
    # Message settings.
    RESPONSE_403_DEBUG_MESSAGE,
    RESPONSE_403_PRODUCTION_MESSAGE,
    RESPONSE_404_DEBUG_MESSAGE,
    RESPONSE_404_PRODUCTION_MESSAGE,
    # Debug text settings.
    TEXT_BLUE,
    TEXT_CYAN,
    TEXT_GREEN,
    TEXT_PURPLE,
    TEXT_RED,
    TEXT_RESET,
    TEXT_YELLOW,
    # Debug print
    SHOW_DEBUG_PRINT,
)


# Constants related to package routes.
from .route_and_policy_constants import (
    LOGIN_URL,
    LOGOUT_ROUTE,
    PWD_RESET_ROUTE,
    PWD_RESET_DONE_ROUTE,
    PWD_RESET_CONFIRM_ROUTE,
    PWD_RESET_COMPLETE_ROUTE,
    REGISTER_ROUTE,
    MEDIA_ROUTE,
    WEBSOCKET_ROUTE,
    HOME_ROUTE,
    PWD_CHANGE,
    PWD_CHANGE_DONE,
)


# Constants related to package policy.
from .route_and_policy_constants import (
    LOGIN_EXEMPT_WHITELIST,
    STRICT_POLICY_WHITELIST,
    LOGIN_EXEMPT_FUZZY_WHITELIST,
    STRICT_POLICY_FUZZY_WHITELIST,
    LOGIN_REQUIRED,
    STRICT_POLICY,
)
