"""Django AdminLTE2 Views"""

# System Imports.
import logging

# Third-Party Imports.
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

# Internal Imports.
from adminlte2_pdq.constants import CSS_COLORS_DICT
from adminlte2_pdq.menu import CSS_MENU


# Initialize logger.
logger = logging.getLogger(__name__)


BOOTSTRAP_TYPES = list(CSS_COLORS_DICT.keys())


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


def demo_css_boxes_solid(request):
    """Show example solid box elements."""

    return render(
        request,
        "adminlte2_demo_css/boxes_solid.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


def demo_css_boxes_standard(request):
    """Show example standard box elements."""

    return render(
        request,
        "adminlte2_demo_css/boxes_standard.html",
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


def demo_css_carousels(request):
    """Show example carousel elements."""

    return render(
        request,
        "adminlte2_demo_css/carousels.html",
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
        "adminlte2_demo_css/modals.html",
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
            "css_color_hex_keys": CSS_COLORS_DICT,
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


def demo_css_typography(request):
    """Show example typography elements."""

    return render(
        request,
        "adminlte2_demo_css/typography.html",
        {
            "bootstrap_types": BOOTSTRAP_TYPES,
            "ADMINLTE2_MENU": CSS_MENU,
        },
    )


# endregion Demo CSS
