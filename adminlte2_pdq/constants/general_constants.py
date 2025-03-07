"""General package constants."""

# Third-Party Imports.
from django.conf import settings


# Date/Time picker widgets to use. Valid values are "native", "jquery", "bootstrap".
DATETIME_WIDGET = getattr(settings, "ADMINLTE2_DATETIME_WIDGET", "native")
DATE_WIDGET = getattr(settings, "ADMINLTE2_DATE_WIDGET", "native")
TIME_WIDGET = getattr(settings, "ADMINLTE2_TIME_WIDGET", "native")


# Boolean indicating if fields marked as "required" should be rendered in templates as bold.
BOLD_REQUIRED_FIELDS = getattr(settings, "ADMINLTE2_BOLD_REQUIRED_FIELDS", True)
# Boolean indicating if fields marked as "required" should be rendered in templates with an asterisk.
ASTERISK_REQUIRED_FIELDS = getattr(settings, "ADMINLTE2_ASTERISK_REQUIRED_FIELDS", True)


# Whether the system should use it's default functionality of redirecting users
# to the home page on a 403 error, or just raise a 403 error that should be
# handled manually by whatever means the user of the package has set up.
REDIRECT_TO_HOME_ON_403 = getattr(settings, "ADMINLTE2_REDIRECT_TO_HOME_ON_403", True)
# Whether the system should use it's default functionality of redirecting users
# to the home page on a 404 error, or just raise a 404 error that should be
# handled manually by whatever means the user of the package has set up.
REDIRECT_TO_HOME_ON_404 = getattr(settings, "ADMINLTE2_REDIRECT_TO_HOME_ON_404", True)

# The message to show upon a standard 403 "missing permissions" redirect.
# To skip showing messages, change either setting to a blank string.
# The `debug` message only shows if the above ADMINLTE_DEBUG = True. Otherwise the `production` message shows.
RESPONSE_403_DEBUG_MESSAGE = str(
    getattr(
        settings,
        "ADMINLTE2_RESPONSE_403_DEBUG_MESSAGE",
        (
            "AdminLtePdq Warning: Attempted to access {view_type} view '{view_name}' which "
            "requires permissions, and user permission requirements were not met. "
            "Redirected to project home instead. \n"
            "\n\n"
            "For further information, please see the docs: "
            "https://django-adminlte2-pdq.readthedocs.io/"
        ),
    )
).strip()
RESPONSE_403_PRODUCTION_MESSAGE = str(
    getattr(
        settings,
        "ADMINLTE2_RESPONSE_403_PRODUCTION_MESSAGE",
        "Unable to locate the requested page. If you believe this was an error, please contact the site administrator.",
    )
).strip()


# The message to show upon a standard 404 "page not found" redirect.
# To skip showing messages, change either setting to a blank string.
# The `debug` message only shows if the above ADMINLTE_DEBUG = True. Otherwise the `production` message shows.
RESPONSE_404_DEBUG_MESSAGE = str(
    getattr(
        settings,
        "ADMINLTE2_RESPONSE_404_DEBUG_MESSAGE",
        "AdminLtePdq Warning: The page you were looking for does not exist.",
    )
).strip()
RESPONSE_404_PRODUCTION_MESSAGE = str(
    getattr(
        settings,
        "ADMINLTE2_RESPONSE_404_PRODUCTION_MESSAGE",
        "Unable to locate the requested page. If you believe this was an error, please contact the site administrator.",
    )
).strip()


# Demo CSS Constant
# Override this to change what color values appear in all the demo css pages.
# Can be used to remove any unwanted colors, or add new custom colors if desired.
CSS_COLORS_DICT = dict(
    getattr(
        settings,
        "ADMINLTE2_CSS_COLORS_DICT",
        {
            "default": "#f4f4f4",
            "primary": "#3c8dbc",
            "info": "#00c0ef",
            "success": "#00a65a",
            "warning": "#f39c12",
            "danger": "#dd4b39",
            "navy": "#001f3f",
            "blue": "#0073b7",
            "teal": "#39cccc",
            "olive": "#3d9970",
            "lime": "#01ff70",
            "orange": "#ff851b",
            "fuchsia": "#f012be",
            "indigo": "#a35cd8",
            "purple": "#605ca8",
            "maroon": "#d81b60",
            "gray": "#d2d6de",
            "black": "#111111",
        },
    )
)
