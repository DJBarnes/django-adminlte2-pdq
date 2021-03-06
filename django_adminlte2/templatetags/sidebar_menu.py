"""
Django AdminLTE2 Sidebar Template Tags

Template tags and logic for rendering sidebar menu
"""
from django import template
from django.conf import settings
from django.urls import resolve, reverse, NoReverseMatch
from django.utils.module_loading import import_string

from django_adminlte2.menu import MENU, WHITELIST
from django_adminlte2.templatetags.admin.admin_menu import AdminMenu

register = template.Library()


def strip_hash_bookmark_from_url(url):
    """Strip the hash bookmark from a string url"""
    return (url or '').split('#')[0]


def get_permissions_from_node(node):
    """
    Gets the permissions required from the node

    by using either the 'route' or 'url' key on the node to determine the
    associated view for the route/url. Then checks the view to see if it
    contains properties for the required permissions and returns them if found.
    """
    permissions = node.get('permissions', None)
    one_of_permissions = node.get('one_of_permissions', None)

    if permissions is not None or one_of_permissions is not None:
        return permissions or [], one_of_permissions or []

    view = None
    try:
        route = node['route']
        url_with_hash = node.get('url', None)
        url = url_with_hash.split('#')[0] if url_with_hash else None

        if route != '#':
            view = resolve(reverse(route))
        elif url and url != '':
            view = resolve(url)

    except KeyError as key_error:
        error_message = (
            "The route key must be provided for the node."
            " If you do not have a valid route yet you can use '#' as a placeholder."
            " If you have Whitelisting turned on, be sure to add an entry for '#' to the whitelist."
            " Missing key was: {0}"
        ).format(key_error)
        raise KeyError(error_message) from key_error
    except NoReverseMatch as reverse_error:
        error_message = (
            "The node with the route '{0}' is not a valid route."
            " If you do not have a valid route yet you can use '#' as a placeholder."
            " If you have Whitelisting turned on, be sure to add an entry for '#' to the whitelist."
            " Exception Message: {1}"
        ).format(route, reverse_error)
        raise NoReverseMatch(error_message) from reverse_error

    if view:
        view_class = getattr(view.func, 'view_class', None)
        if view_class:
            permissions = getattr(view_class, 'permission_required', [])
            one_of_permissions = getattr(
                view_class,
                'permission_required_one',
                []
            )
        else:
            permissions = getattr(view.func, 'permissions', [])
            one_of_permissions = getattr(view.func, 'one_of_permissions', [])

    return permissions or [], one_of_permissions or []


def ensure_node_has_url_property(node):
    """Ensure that a node has a url property"""
    if 'url' not in node:
        try:
            route = node['route']
            if route != '#':
                url = reverse(route)
            else:
                url = '#'
        except KeyError as key_error:
            error_message = (
                "The route key must be provided for the node."
                " If you do not have a valid route yet you can use '#' as a placeholder."
                " If you have Whitelisting turned on, be sure to"
                " add an entry for '#' to the whitelist."
                " Missing key was: {0}"
            ).format(key_error)
            raise KeyError(error_message) from key_error
        except NoReverseMatch as reverse_error:
            error_message = (
                "The node with the route '{0}' is not a valid route."
                " If you do not have a valid route yet you can use '#' as a placeholder."
                " If you have Whitelisting turned on, be sure to"
                " add an entry for '#' to the whitelist."
                " Exception Message: {1}"
            ).format(route, reverse_error)
            raise NoReverseMatch(error_message) from reverse_error

        node['url'] = url


def check_for_whitelisted_node(node):
    """Check to see if the route property on the node is in the whitelist"""
    return node.get('route') in getattr(
        settings,
        'ADMINLTE2_MENU_PERMISSION_FREE_WHITELIST',
        WHITELIST
    )


def check_for_all_permissions(user, permissions):
    """
    Check to see if the passed user has all of the permissions

    that are listed in the passed permissions.
    If the user does not have all of them, false is returned.
    If the passed permission list is empty, the method returns false.
    Even though empty permission lists return false here, they are checked
    with the whitelist methods in the is_allowed_node method.
    Unless you know what you are doing, consider using is_allowed_node
    for true permission checking on a node.
    """

    # Superusers get all permissions
    if user.is_superuser:
        return True

    allowed = True

    # Compare the user's perms against the passed in permissions
    # ensuring the user has all of them
    if permissions:
        if not user.has_perms(permissions):
            allowed = False
    else:
        allowed = False

    return allowed


def check_for_one_permission(user, permissions):
    """
    Check to see if the passed user has at least one of the permissions

    that are listed in the passed permissions.
    If the user does not have one of them, false is returned.
    If the passed permission list is empty, the method returns false.
    Even though empty permission lists return false here, they are checked
    with the whitelist methods in the is_allowed_node method.
    Unless you know what you are doing, consider using is_allowed_node
    for true permission checking on a node.
    """

    # Superusers get all permissions
    if user.is_superuser:
        return True

    allowed = False

    # Compare the user's perms against the passed in permissions
    # ensuring the user has all of them
    if permissions:
        for permission in permissions:
            if user.has_perm(permission):
                allowed = True
                break

    return allowed


def is_allowed_node(user, node):
    """
    Checks to ensure a node is valid for rendering.

    An all encompassing method that checks all permissions, one of permissions
    and the whitelist settings to know whether or not a given node is valid
    for rendering to the user.
    Any new code that needs to check permissions should use this method.
    """

    permissions, one_of_permissions = get_permissions_from_node(node)

    # Determine if the node is accessible by permissions alone.
    # This will be false for empty node permission lists
    allowed_by_perms = check_for_all_permissions(user, permissions) or \
        check_for_one_permission(user, one_of_permissions)

    # Get whether to do whitelist checking
    do_whitelist_check = getattr(
        settings,
        'ADMINLTE2_USE_WHITELIST_FOR_UNDEFINED_PERMISSIONS',
        False
    )

    # If we are whitelist checking
    if do_whitelist_check:
        # Allowed will be true if the node is allowed by perms, or in the whitelist
        allowed = allowed_by_perms or check_for_whitelisted_node(node)
    else:
        # Else, if the permission lists are not empty, use those
        if permissions or one_of_permissions:
            allowed = allowed_by_perms
        else:
            # Else, there is no white list checking, and there are no defined
            # permissions, so return true to make the node allowed
            allowed = True

    return allowed


def check_for_one_permission_in_node_list(user, nodes):
    """Check user has one permission in the entire node list"""
    # Superusers get all permissions
    if user.is_superuser:
        return True

    allowed = False

    if nodes:
        for node in nodes:
            child_nodes = node.get('nodes')
            if child_nodes:
                child_allowed = check_for_one_permission_in_node_list(
                    user,
                    child_nodes
                )
                if child_allowed:
                    allowed = True
            else:
                check_result = is_allowed_node(user, node)

                if check_result:
                    allowed = True
                    break

    return allowed


def check_for_node_that_matches_request_path(request, nodes):
    """Check for a node that matches the request path"""

    match = False

    if nodes:
        for node in nodes:
            child_nodes = node.get('nodes')
            if child_nodes:
                child_match = check_for_node_that_matches_request_path(
                    request,
                    child_nodes
                )
                if child_match:
                    match = True
            else:
                ensure_node_has_url_property(node)
                stripped_request = strip_hash_bookmark_from_url(request.path)
                stripped_node_url = strip_hash_bookmark_from_url(node['url'])
                if stripped_request.startswith(stripped_node_url):
                    match = True

    return match


@register.inclusion_tag('adminlte2/partials/_main_sidebar/_menu.html', takes_context=True)
def render_menu(context):
    """Render out the sidebar menu"""

    use_menu_group_separator = getattr(
        settings,
        'ADMINLTE2_USE_MENU_GROUP_SEPARATOR',
        True,
    )

    include_admin_nav = getattr(
        settings,
        'ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES',
        False,
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
    )
    menu_admin = AdminMenu.create_menu(context) if include_admin_nav else []
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


@register.inclusion_tag('adminlte2/partials/_main_sidebar/_menu_section.html', takes_context=True)
def render_section(context, section):
    """Render out an entire sidebar section"""
    nodes = section.get('nodes')
    allowed = check_for_one_permission_in_node_list(context['user'], nodes)

    return {
        'section': section,
        'allowed': allowed,
        'user': context['user'],  # render_tree needs this
        'request': context['request'],  # render_tree needs this
    }


@register.inclusion_tag('adminlte2/partials/_main_sidebar/_menu_nodes.html', takes_context=True)
def render_nodes(context, nodes):
    """Render out a list of nodes"""
    return {
        'nodes': nodes,
        'user': context['user'],  # render_tree needs this
        'request': context['request'],  # render_tree needs this
    }


@register.inclusion_tag('adminlte2/partials/_main_sidebar/_menu_tree.html', takes_context=True)
def render_tree(context, node):
    """Render out a menu tree"""
    nodes = node.get('nodes')
    allowed = check_for_one_permission_in_node_list(context['user'], nodes)
    add_display_block = check_for_node_that_matches_request_path(
        context['request'],
        nodes
    )

    if not node.get('icon'):
        node['icon'] = 'not-found'

    return {
        'node': node,
        'allowed': allowed,
        'add_display_block': add_display_block,
        'user': context['user'],
        'request': context['request'],
    }


@register.inclusion_tag('adminlte2/partials/_main_sidebar/_menu_link.html', takes_context=True)
def render_link(context, node):
    """Render out a menu link"""
    default = {
        'class': '',
        'attributes': {},
    }

    default.update(node)
    node = default

    ensure_node_has_url_property(node)

    allowed = is_allowed_node(context['user'], node)

    text = node.get('text') or ''
    title = text
    hook = node.get('hook')  # 'path.to.function' that will return text
    if hook:
        # NOTE: hook should return 'text' or a tuple ('text', 'title text')
        hook_args = node.get('hook_args', [])
        hook_kwargs = node.get('hook_kwargs', {})
        text_func = import_string(hook)
        text = title = text_func(*hook_args, context=context, **hook_kwargs)
        try:
            text, title = text
        except ValueError:
            pass  # A tuple wasn't returned, assume just text

    node['text'] = text
    node['title'] = title

    if not node.get('icon'):
        node['icon'] = ''

    return {
        'node': node,
        'allowed': allowed,
        'request': context['request'],
    }


@register.filter
def url_starts_with(search_string, sub_string):
    """Determine if a url starts with a sub string"""
    stripped_search_string = strip_hash_bookmark_from_url(search_string)
    stripped_sub_string = strip_hash_bookmark_from_url(sub_string)
    return stripped_search_string.startswith(stripped_sub_string)
