"""Django AdminLTE2 Admin Menu"""
from django import template
from django.conf import settings

from adminlte2_pdq.menu import MENU
from adminlte2_pdq.admin_menu import AdminMenu


register = template.Library()


@register.inclusion_tag('adminlte2/partials/_main_sidebar/_menu.html', takes_context=True)
def render_admin_menu(context):
    """Render out the admin menu"""

    use_menu_group_separator = getattr(
        settings, 'ADMINLTE2_USE_MENU_GROUP_SEPARATOR', True)

    include_main_nav = getattr(
        settings, 'ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES',
        False
    )

    separator = {
        'text': '',
        'nodes': [],
        'separator': True,
    }

    menu_first = context.get('ADMINLTE2_MENU_FIRST', [])
    menu_main = context.get(
        'ADMINLTE2_MENU',
        getattr(
            settings,
            'ADMINLTE2_MENU',
            MENU
        )
    ) if include_main_nav else []
    menu_admin = AdminMenu.create_menu(context)
    menu_last = context.get('ADMINLTE2_MENU_LAST', [])

    section_list = menu_first
    if use_menu_group_separator and menu_first and (menu_main or menu_admin or menu_last):
        section_list += [separator]

    section_list += menu_main
    if use_menu_group_separator and menu_main and (menu_admin or menu_last):
        section_list += [separator]

    section_list += menu_admin
    if use_menu_group_separator and menu_admin and menu_last:
        section_list += [separator]

    section_list += menu_last

    return {
        'section_list': section_list,
        'user': context['user'],  # render_section needs this
        'request': context['request'],  # render_tree needs this
    }


@register.simple_tag()
def render_admin_tree_icon():
    """Render the admin tree icon"""
    return AdminMenu.get_admin_icon()


@register.simple_tag(takes_context=True)
def render_app_icon(context):
    """Render app icon"""
    return AdminMenu.get_app_icon(context['app']['name'])


@register.simple_tag(takes_context=True)
def render_model_icon(context):
    """Render model icon"""
    return AdminMenu.get_model_icon(context['model']['object_name'])
