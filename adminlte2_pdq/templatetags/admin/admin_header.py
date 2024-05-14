"""Django AdminLTE2 Admin Header"""

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
