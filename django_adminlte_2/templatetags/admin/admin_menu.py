"""Django AdminLTE2 Admin Menu"""
from django import template
from django.conf import settings
from django.contrib.admin.sites import site

from django_adminlte_2.menu import MENU

DEFAULT_ICON_ADMIN = 'fa fa-superpowers'
DEFAULT_ICON_APP = 'fa fa-circle'
DEFAULT_ICON_MODEL = 'fa fa-circle-o'


class _AdminMenu:
    """Admin Menu"""

    def __init__(self):
        self.admin_header_text = 'Administrator'
        self.admin_icon = DEFAULT_ICON_ADMIN
        self.model_icons = {}
        self.app_icons = {}

    def create_menu(self, context):
        """Create Menu"""

        app_list = []

        all_admin_perms = []

        request = context['request']

        if not context.get('available_apps'):
            context['available_apps'] = site.get_app_list(request)

        for app in context['available_apps']:

            model_nodes = []

            for model in app['models']:

                if context['user'].is_staff or context['user'].is_superuser:

                    # Initialize to none. If the user has a valid url endpoint they
                    # can access from permissions, the url will get a value.
                    url = None

                    if 'add_url' in model:
                        url = model['add_url']

                    if 'change_url' in model:
                        url = model['change_url']

                    if 'admin_url' in model:
                        url = model['admin_url']

                    # Only add node if user has a url to connect to.
                    if url:
                        model_perms = []

                        for perm, enabled in model['perms'].items():
                            if enabled:
                                lower_model_name = model['object_name'].lower()
                                current_permission = "%s_%s" % (
                                    perm,
                                    lower_model_name
                                )
                                new_entry = "%s.%s" % (
                                    app['app_label'],
                                    current_permission
                                )
                                model_perms.append(new_entry)
                                all_admin_perms.append(new_entry)

                        model_name = model['object_name']
                        model_icon = self.get_model_icon(model_name)

                        model_node = {
                            'url': url,
                            'text': model_name,
                            'icon': model_icon,
                            'permissions': [],
                            'one_of_permissions': model_perms,
                        }

                        model_nodes.append(model_node)

            if model_nodes:

                app_name = app['name']

                app_icon = self.get_app_icon(app_name)

                tree = {
                    'text': app_name,
                    'icon': app_icon,
                    'nodes': model_nodes,
                }

                app_list.append(tree)

        admin_index = [
            {
                'route': 'admin:index',
                'text': 'Admin Home',
                'icon': self.get_admin_icon(),
                'permissions': [],
                'one_of_permissions': all_admin_perms,
                'active_requires_exact_url_match': True,
            }
        ]

        put_entire_admin_in_tree = getattr(
            settings, 'ADMINLTE2_ADMIN_MENU_IN_TREE', False
        )

        show_admin_home_link = getattr(
            settings, 'ADMINLTE2_INCLUDE_ADMIN_HOME_LINK', False
        )

        if show_admin_home_link and app_list:
            full_list = admin_index + app_list
        else:
            full_list = app_list

        if put_entire_admin_in_tree:
            root_nodes = [
                {
                    'text': 'Admin',
                    'icon': self.admin_icon,
                    'nodes': full_list,
                },
            ]
        else:
            root_nodes = full_list

        menu = [
            {
                'text': self.admin_header_text,
                'nodes': root_nodes,
            }
        ]

        return menu

    def set_model_icon(self, model_name, icon):
        """Set model icon"""
        self.model_icons[model_name] = icon

    def get_model_icon(self, model_name):
        """Get model icon"""
        return self.model_icons.get(model_name, DEFAULT_ICON_MODEL)

    def set_app_icon(self, app_name, icon):
        """Set app icon"""
        self.app_icons[app_name] = icon

    def get_app_icon(self, app_name):
        """Get app icon"""
        return self.app_icons.get(app_name, DEFAULT_ICON_APP)

    def set_admin_icon(self, icon):
        """Set admin icon"""
        self.admin_icon = icon

    def get_admin_icon(self):
        """Get admin icon"""
        return self.admin_icon


register = template.Library()

AdminMenu = _AdminMenu()


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
    menu_main = getattr(
        settings, 'ADMINLTE2_MENU', MENU) if include_main_nav else []
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
