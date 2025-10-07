"""Imports to make this folder behave like a single file."""

# Constants related to general package settings.
from .general_constants import (
    DATETIME_WIDGET,
    DATE_WIDGET,
    TIME_WIDGET,
    BOLD_REQUIRED_FIELDS,
    ASTERISK_REQUIRED_FIELDS,
    # 403 / 404 handling.
    REDIRECT_TO_HOME_ON_403,
    REDIRECT_TO_HOME_ON_404,
    # Message settings.
    RESPONSE_403_DEBUG_MESSAGE,
    RESPONSE_403_PRODUCTION_MESSAGE,
    RESPONSE_404_DEBUG_MESSAGE,
    RESPONSE_404_PRODUCTION_MESSAGE,
)


# Constants related to package routes.
from .route_and_policy_constants import (
    LOGIN_URL,
    LOGOUT_URL,
    PWD_RESET_ROUTE,
    PWD_RESET_DONE_ROUTE,
    PWD_RESET_CONFIRM_ROUTE,
    PWD_RESET_COMPLETE_ROUTE,
    REGISTER_ROUTE,
    MEDIA_ROUTE,
    STATIC_ROUTE,
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
    STRICT_POLICY_SERVE_404_FUZZY_WHITELIST,
)
