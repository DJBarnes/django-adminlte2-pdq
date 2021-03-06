"""Django AdminLTE2 Admin Index"""
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('admin/partials/_index_app_display.html', takes_context=True)
def index_app_display(context):
    """Index app display"""

    use_app_list = getattr(
        settings,
        'ADMINLTE2_ADMIN_INDEX_USE_APP_LIST',
        False
    )

    if use_app_list:
        partial = "admin/partials/_index_list.html"
    else:
        partial = "admin/partials/_index_box.html"

    return {
        'admin_index_partial': partial,
        'app': context.get('app'),
        'model': context.get('model'),
    }
