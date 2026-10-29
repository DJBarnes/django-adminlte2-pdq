"""Django AdminLTE2 Admin Header"""

import django
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("admin/partials/_main_header_control_sidebar_button.html")
def show_control_sidebar_button():
    """Show control sidebar button"""

    default_dict = {
        "SHOW_RECENT_ACTIVITY_TAB": True,
    }

    control_sidebar_tabs = {
        **default_dict,
        **getattr(settings, "ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS", {}),
    }

    number_of_tabs = sum(control_sidebar_tabs.values())

    show_button = number_of_tabs > 0

    return {"show_control_sidebar_button": show_button}


@register.simple_tag()
def django_admin_follows_browser_dark_mode():
    """Whether Django admin's base.css switches to dark colors when the browser prefers dark (Django < 4.2)."""
    return django.VERSION < (4, 2)
