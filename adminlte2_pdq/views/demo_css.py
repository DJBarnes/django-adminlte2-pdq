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


def demo_css(request):
    """Show examples of extra-features.css"""

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
        "adminlte2_demo_css/old/home.html",
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
        "adminlte2_demo_css/old/alerts.html",
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


def demo_css_buttons(request):
    """Show example button elements."""

    return render(
        request,
        "adminlte2_demo_css/old/buttons.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_labels(request):
    """Show example label elements."""

    return render(
        request,
        "adminlte2_demo_css/old/labels.html",
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
        "adminlte2_demo_css/old/tables.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


# endregion Demo CSS
