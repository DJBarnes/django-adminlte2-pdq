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
