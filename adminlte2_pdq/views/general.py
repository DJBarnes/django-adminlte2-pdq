"""Django AdminLTE2 Views"""

# System Imports.
import logging

# Third-Party Imports.
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

# Internal Imports.
from adminlte2_pdq.constants import (
    RESPONSE_404_DEBUG_MESSAGE,
    RESPONSE_404_PRODUCTION_MESSAGE,
)
from adminlte2_pdq.decorators import (
    login_required,
    permission_required,
    permission_required_one,
)
from adminlte2_pdq.forms import SampleForm, SampleFormset
from adminlte2_pdq.menu import CSS_MENU


# Initialize logger.
logger = logging.getLogger(__name__)


def home(request):
    """Show default home page"""
    return render(request, "adminlte2/home.html", {})


def register(request):
    """Show default register page"""
    dummy_form = {
        "errors": None,
        "non_field_errors": None,
    }
    return render(
        request,
        "registration/register.html",
        {
            "form": dummy_form,
        },
    )


@login_required()
def sample_form(request):
    """Show sample form page"""
    form = SampleForm()
    form["sample_phone"].phone_info = {
        "pattern": r"\([0-9]{3}\) [0-9]{3}-[0-9]{4}",
        "inputmask": "(999) 999-9999",
    }
    form["sample_range"].range_min_max = {
        "min": 5,
        "max": 10,
    }
    form["sample_color"].is_color = True
    form["sample_datalist"].datalist = {
        "name": "my_awesome_datalist",
        "data": ("foo", "bar"),
    }

    formset = SampleFormset()

    return render(
        request,
        "adminlte2/sample_form.html",
        {"form": form, "formset": formset},
    )


@permission_required(["auth.add_group", "auth.change_group", "auth.delete_group"])
def sample1(request):
    """Show default sample1 page"""
    return render(request, "adminlte2/sample1.html", {})


@permission_required_one(["auth.add_permission", "auth.change_permission", "auth.delete_permission"])
def sample2(request):
    """Show default sample2 page"""
    return render(request, "adminlte2/sample2.html", {})


def view_404(request, exception):
    """On failure to locate a route, redirect to home page."""

    # Display warning.
    if settings.DEBUG:
        # Handle output when DEBUG = True.
        if len(RESPONSE_404_DEBUG_MESSAGE) > 0:
            messages.warning(request, RESPONSE_404_DEBUG_MESSAGE)
            logger.warning(RESPONSE_404_DEBUG_MESSAGE)
            messages.debug(request, str(exception))
            logger.warning(str(exception))
    else:
        # Handle output when DEBUG = False.
        if len(RESPONSE_404_PRODUCTION_MESSAGE) > 0:
            messages.warning(request, RESPONSE_404_PRODUCTION_MESSAGE)

    # Redirect to home.
    home_route = getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home")
    return redirect(home_route)
