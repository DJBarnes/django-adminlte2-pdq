"""Django AdminLTE2 default Constants."""
from django.conf import settings

# Known routes that should never require being logged in.
LOGIN_URL = getattr(settings, 'LOGIN_URL', '/accounts/login')
LOGOUT_ROUTE = getattr(settings, 'LOGOUT_ROUTE', 'logout')
PWD_RESET_ROUTE = getattr(settings, 'PWD_RESET_ROUTE', 'password_reset')
PWD_RESET_DONE_ROUTE = getattr(settings, 'PWD_RESET_DONE_ROUTE', 'password_reset_done')
PWD_RESET_CONFIRM_ROUTE = getattr(settings, 'PWD_RESET_CONFIRM_ROUTE', 'password_reset_confirm')
PWD_RESET_COMPLETE_ROUTE = getattr(settings, 'PWD_RESET_COMPLETE_ROUTE', 'password_reset_complete')
REGISTER_ROUTE = getattr(settings, 'REGISTER_ROUTE', 'adminlte2_pdq:register')
MEDIA_ROUTE = getattr(settings, 'MEDIA_URL', '/media/')

# Known routes that should never have a permission check done.
HOME_ROUTE = getattr(settings, 'ADMINLTE2_HOME_ROUTE', 'adminlte2_pdq:home')

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
] + LOGIN_EXEMPT_WHITELIST

# Add any user defined list of exempt urls to the constant.
LOGIN_EXEMPT_WHITELIST += getattr(settings, 'ADMINLTE2_LOGIN_EXEMPT_WHITELIST', [])
STRICT_POLICY_WHITELIST += getattr(settings, 'ADMINLTE2_STRICT_POLICY_WHITELIST', [])

# Get whether or not we are using LoginRequired and PermissionRequired
LOGIN_REQUIRED = getattr(settings, 'ADMINLTE2_USE_LOGIN_REQUIRED', False)
STRICT_POLICY = getattr(settings, 'ADMINLTE2_USE_STRICT_POLICY', False)

# Date Time Picker Widgets to use. Valid values are 'native', 'jquery', 'bootstrap'
DATETIME_WIDGET = getattr(settings, 'ADMINLTE2_DATETIME_WIDGET', 'native')
DATE_WIDGET = getattr(settings, 'ADMINLTE2_DATE_WIDGET', 'native')
TIME_WIDGET = getattr(settings, 'ADMINLTE2_TIME_WIDGET', 'native')
