"""Django AdminLTE2 Views"""

# System Imports.
import logging

# Third-Party Imports.
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

# Internal Imports.
from adminlte2_pdq.menu import CSS_MENU


# Initialize logger.
logger = logging.getLogger(__name__)


# Module level variables.
BOOTSTRAP_TYPES = [
    "default",
    "primary",
    "info",
    "success",
    "warning",
    "danger",
    "navy",
    "blue",
    "teal",
    "olive",
    "lime",
    "orange",
    "fuchsia",
    "indigo",
    "purple",
    "maroon",
    "gray",
    "black",
]
CSS_COLOR_HEX_KEYS = {
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
}


def demo_css(request):
    """Home page for CSS demo. Primarily links to various pages that show how to use package CSS stylings.
    Can also be used as verification to make sure package HTML/CSS functions as expected.
    """

    return render(
        request,
        "adminlte2_demo_css/home.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_alerts(request):
    """Show example alert elements."""

    # Add messages to demo them.
    messages.set_level(request, messages.DEBUG)
    messages.debug(request, "This is a debug message via the messages framework.")
    messages.info(request, "This is a info message via the messages framework.")
    messages.success(request, "This is a success message via the messages framework.")
    messages.warning(request, "This is a warning message via the messages framework.")
    messages.error(request, "This is a error message via the messages framework.")
    messages.add_message(request, 50, "This is an unknown level message via the messages framework.")

    return render(
        request,
        "adminlte2_demo_css/alerts.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_boxes(request):
    """Show example box elements."""

    return render(
        request,
        "adminlte2_demo_css/old/boxes.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_buttons_basic(request):
    """Show example basic button elements."""

    return render(
        request,
        "adminlte2_demo_css/buttons_basic.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_buttons_specialized(request):
    """Show example specialized button elements."""

    return render(
        request,
        "adminlte2_demo_css/buttons_specialized.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_buttons_boxes(request):
    """Show example box elements."""

    return render(
        request,
        "adminlte2_demo_css/boxes.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_labels(request):
    """Show example label elements."""

    return render(
        request,
        "adminlte2_demo_css/labels.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_modals(request):
    """Show example modal elements."""

    return render(
        request,
        "adminlte2_demo_css/old/modals.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_tables(request):
    """Show example table elements."""

    return render(
        request,
        "adminlte2_demo_css/tables.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_ui_general(request):
    """Show example general ui elements."""

    return render(
        request,
        "adminlte2_demo_css/ui_general.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "css_color_hex_keys": CSS_COLOR_HEX_KEYS,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_widgets(request):
    """Show example widget elements."""

    return render(
        request,
        "adminlte2_demo_css/widgets.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


# endregion Demo CSS
