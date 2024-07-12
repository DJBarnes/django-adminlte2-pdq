"""Django AdminLTE2 Admin Control Sidebar"""
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('admin/partials/_control_sidebar/_tabs.html')
def show_control_sidebar_tabs():
    """Show the control sidebar tabs"""

    # Default the show recent activity tab to true
    default_dict = {
        'SHOW_RECENT_ACTIVITY_TAB': True,
    }

    # Pull the settings for the control sidebar from settings.
    # It is possible that the show recent activity will be
    # overridden by the settings
    control_sidebar_tabs = {
        **default_dict,
        **getattr(
            settings,
            'ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS',
            {}
        ),
    }

    # Get the number of tabs that should be shown. This sums up the values
    # of the dictionary representing the control sidebar. Each value is a
    # boolean. Despite the fact that they values are booleans, the sum operation
    # will work since False = 0 and True = 1. Therefore, one setting set to
    # true will yield True, and 3 settings set to try will yield 3.
    number_of_tabs = sum(control_sidebar_tabs.values())

    # If the number of tabs is greater than 1, we will turn the control sidebar
    # into tabs. If it is 0 or 1 tab, it will not render the tabs part.
    show_tabs = number_of_tabs > 1

    return {
        'show_csb_tabs': show_tabs,
        'show_csb_recent_tab': control_sidebar_tabs.get(
            'SHOW_RECENT_ACTIVITY_TAB', False
        ),
        'show_csb_settings_tab': control_sidebar_tabs.get(
            'SHOW_SETTINGS_TAB', False
        ),
        'show_csb_extra_tab': control_sidebar_tabs.get(
            'SHOW_EXTRA_TABS', False
        ),
    }


@register.inclusion_tag(
    'admin/partials/_control_sidebar/_recent_activity_tab_pane.html',
    takes_context=True
)
def show_control_sidebar_recent_activity_tab_pane(context):
    """Show the control sidebar recent activity tab pane"""

    control_sidebar_tabs = getattr(
        settings,
        'ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS',
        {}
    )

    show_tab_pane = control_sidebar_tabs.get('SHOW_RECENT_ACTIVITY_TAB', True)

    new_context = context.flatten()
    new_context.update({
        'show_csb_recent_activity_tab_pane': show_tab_pane,
    })

    return new_context


@register.inclusion_tag('admin/partials/_control_sidebar/_settings_tab_pane.html')
def show_control_sidebar_settings_tab_pane():
    """Show control sidebar settings tab pane"""

    control_sidebar_tabs = getattr(
        settings,
        'ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS',
        {}
    )

    show_tab_pane = control_sidebar_tabs.get('SHOW_SETTINGS_TAB', False)
    tab_pane_active = not control_sidebar_tabs.get(
        'SHOW_RECENT_ACTIVITY_TAB',
        True
    )

    return {
        'show_csb_settings_tab_pane': show_tab_pane,
        'activate_csb_settings_tab_pane': tab_pane_active,
    }


@register.inclusion_tag('admin/partials/_control_sidebar/_extra_tab_panes.html')
def show_control_sidebar_extra_tab_panes():
    """Show control sidebar extra tab panes"""

    control_sidebar_tabs = getattr(
        settings,
        'ADMINLTE2_ADMIN_CONTROL_SIDEBAR_TABS',
        {}
    )

    show_tab_pane = control_sidebar_tabs.get('SHOW_EXTRA_TABS', False)
    tab_pane_active = not (
        control_sidebar_tabs.get('SHOW_RECENT_ACTIVITY_TAB', True) or
        control_sidebar_tabs.get('SHOW_SETTINGS_TAB', False)
    )

    return {
        'show_csb_extra_tab_panes': show_tab_pane,
        'activate_csb_extra_tab_panes': tab_pane_active,
    }
