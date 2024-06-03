"""
Django AdminLTE2 Sidebar Template Tags

Template tags and logic for rendering sidebar menu
"""

# Third-Party Imports.
from django import template
from django.conf import settings
from django.http import Http404
from django.urls import resolve, reverse, NoReverseMatch
from django.utils.module_loading import import_string

# Internal Imports.
from adminlte2_pdq.constants import (
    LOGIN_REQUIRED,
    LOGIN_EXEMPT_WHITELIST,
    STRICT_POLICY,
    STRICT_POLICY_WHITELIST,
)
from adminlte2_pdq.menu import MENU
from adminlte2_pdq.templatetags.admin.admin_menu import AdminMenu


# Template tag registration.
register = template.Library()


NODE_KEY_ERROR_MESSAGE = (
    "The route key must be provided for the node."
    " If you do not have a valid route yet you can use '#' as a placeholder."
    " If you have Whitelisting turned on, be sure to"
    " add an entry for '#' to the whitelist."
    " Missing key was: {key_error}"
)
NODE_REVERSE_ERROR_MESSAGE = (
    "The node with the route '{route}' is not a valid route."
    " If you do not have a valid route yet you can use '#' as a placeholder."
    " If you have Whitelisting turned on, be sure to"
    " add an entry for '#' to the whitelist."
    " Exception Message: {reverse_error}"
)


def strip_hash_bookmark_from_url(url):
    """Strip the hash bookmark from a string url"""
    return (url or "").split("#")[0]


def get_view_from_node(node):
    """Get the view from the node"""

    view = None
    try:
        route = node["route"]
        route_args = node.get("route_args", [])
        route_kwargs = node.get("route_kwargs", {})
        url_with_hash = node.get("url", None)
        url = url_with_hash.split("#")[0] if url_with_hash else None

        try:
            if route != "#":
                view = resolve(reverse(route, args=route_args, kwargs=route_kwargs))
            elif url and url != "":
                view = resolve(url)
        except Http404:
            view = None

    except KeyError as key_error:
        error_message = NODE_KEY_ERROR_MESSAGE.format(key_error=key_error)
        raise KeyError(error_message) from key_error
    except NoReverseMatch as reverse_error:
        error_message = NODE_REVERSE_ERROR_MESSAGE.format(
            route=route,
            reverse_error=reverse_error,
        )
        raise NoReverseMatch(error_message) from reverse_error

    return view


def get_permissions_from_view(view):
    """Get the permissions and login_required from a view"""

    view_data = {}
    view_class = getattr(view.func, "view_class", None)
    if view_class:
        pdq_data = getattr(view_class, "admin_pdq_data", {})
    else:
        pdq_data = getattr(view.func, "admin_pdq_data", {})

    view_data["decorator_name"] = pdq_data.get("decorator_name", "")
    view_data["allow_anonymous"] = pdq_data.get("allow_anonymous", None)
    view_data["login_required"] = pdq_data.get("login_required", None)
    view_data["allow_without_permissions"] = pdq_data.get("allow_without_permissions", None)
    view_data["one_of_permissions"] = pdq_data.get("one_of_permissions", [])
    view_data["full_permissions"] = pdq_data.get("full_permissions", [])

    return view_data


def get_permissions_from_node(node):
    """
    Gets the permissions required from the node

    by using either the 'route' or 'url' key on the node to determine the
    associated view for the route/url. Then checks the view to see if it
    contains properties for the required permissions and returns them if found.
    """

    # Get permissions and login_required defined directly on the node.
    node_allow_anonymous = node.get("allow_anonymous", None)
    node_login_required = node.get("login_required", None)
    node_allow_without_permissions = node.get("allow_without_permissions", None)
    node_one_of_permissions = node.get("one_of_permissions", None)
    node_full_permissions = node.get("permissions", None)

    # Skip checking if all values are set.
    # Required as a work-around for default Django behavior, when rendering
    # an admin page link. If additional permission values are added, they MUST
    # also be added here and then defined on the default node in admin_menu.py.
    if (
        node_allow_anonymous is not None
        and node_login_required is not None
        and node_allow_without_permissions is not None
        and node_one_of_permissions is not None
        and node_full_permissions is not None
    ):
        return (
            node_allow_anonymous,
            node_login_required,
            node_allow_without_permissions,
            node_one_of_permissions,
            node_full_permissions,
        )

    # Default our values to None.
    view_allow_anonymous = None
    view_login_required = None
    view_allow_without_permissions = None
    view_one_of_permissions = None
    view_full_permissions = None

    # Get the view from the node.
    view = get_view_from_node(node)

    # If there is a view, use it to get the view permissions and login_required.
    if view:
        view_data = get_permissions_from_view(view)

        view_allow_anonymous = view_data["allow_anonymous"]
        view_login_required = view_data["login_required"]
        view_allow_without_permissions = view_data["allow_without_permissions"]
        view_one_of_permissions = view_data["one_of_permissions"]
        view_full_permissions = view_data["full_permissions"]

    # NOTE: Order matters for below values.
    # For all of them, a node value takes precedence, if provided.
    # If no node value is provided, the view value is used.
    # Fall back to global default/setting value, if neither of those are set.

    # Check if node allows anonymous.
    allow_anonymous = node_allow_anonymous
    if allow_anonymous is None:
        # Fall back to view value.
        allow_anonymous = view_allow_anonymous

    # Check if node requires login.
    login_required = node_login_required
    if login_required is None:
        # Use decorator/mixin login_required.
        login_required = view_login_required
    if login_required is None:
        # Fall back to settings values.
        login_required = STRICT_POLICY or LOGIN_REQUIRED

    # Check if node allows without permissions.
    allow_without_permissions = node_allow_without_permissions
    if allow_without_permissions is None:
        # Fall back to view value.
        allow_without_permissions = view_allow_without_permissions

    # Check if node requires one of permissions.
    one_of_permissions = node_one_of_permissions
    if one_of_permissions is None:
        # Use view value or empty list.
        one_of_permissions = view_one_of_permissions or []

    # Check if node requires full permissions.
    full_permissions = node_full_permissions
    if full_permissions is None:
        # Use view value or empty list.
        full_permissions = view_full_permissions or []

    # Return calculated values.
    return (
        allow_anonymous,
        login_required,
        allow_without_permissions,
        one_of_permissions,
        full_permissions,
    )


def ensure_node_has_url_property(node):
    """Ensure that a node has a url property"""
    if "url" not in node:
        try:
            route = node["route"]
            route_args = node.get("route_args", [])
            route_kwargs = node.get("route_kwargs", {})
            if route != "#":
                url = reverse(route, args=route_args, kwargs=route_kwargs)
            else:
                url = "#"
        except KeyError as key_error:
            error_message = NODE_KEY_ERROR_MESSAGE.format(key_error=key_error)
            raise KeyError(error_message) from key_error
        except NoReverseMatch as reverse_error:
            error_message = NODE_REVERSE_ERROR_MESSAGE.format(
                route=route,
                reverse_error=reverse_error,
            )
            raise NoReverseMatch(error_message) from reverse_error

        node["url"] = url


def check_for_login_whitelisted_node(node):
    """Check to see if the route property on the node is in the login whitelist"""
    return node.get("route") in LOGIN_EXEMPT_WHITELIST


def check_for_strict_whitelisted_node(node):
    """Check to see if the route property on the node is in the whitelist"""
    return node.get("route") in STRICT_POLICY_WHITELIST


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

    # Get the permissions, one_of_perms, and login_required from the node or node's view.
    return_data = get_permissions_from_node(node)
    allow_anonymous = return_data[0]
    login_required = return_data[1]
    allow_without_permissions = return_data[2]
    one_of_permissions = return_data[3]
    full_permissions = return_data[4]

    # Get whether node has at least one property set
    has_property = login_required or bool(one_of_permissions) or bool(full_permissions)

    # Start allowed as the opposite of the strict policy.
    # If we are in strict mode, allowed should start as false.
    # If we are NOT in strict mode, allowed should start as true.
    allowed = not STRICT_POLICY

    # If the node requires being logged in, or the login required middleware is active.
    if login_required or LOGIN_REQUIRED:
        # If login_required, verify user is authenticated or the route for the
        # node is whitelisted in the login exempt whitelist.
        allowed = user.is_authenticated or check_for_login_whitelisted_node(node)

    # If the node requires permissions, it will also require being logged in
    # without explicitly setting that. But, by checking after the login required
    # check, we can catch both scenarios where they define both.
    if one_of_permissions or full_permissions:

        # Determine if the node is accessible by permissions alone.
        # This will include the need to be logged in even if they didn't specify that.
        allowed = check_for_one_permission(user, one_of_permissions) or check_for_all_permissions(
            user, full_permissions
        )

    # Check whitelist when in strict mode assuming no properties have been set on the node.
    if not has_property and STRICT_POLICY and (check_for_strict_whitelisted_node(node) or user.is_superuser):
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
            child_nodes = node.get("nodes")
            if child_nodes:
                child_allowed = check_for_one_permission_in_node_list(user, child_nodes)
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
            child_nodes = node.get("nodes")
            if child_nodes:
                child_match = check_for_node_that_matches_request_path(request, child_nodes)
                if child_match:
                    match = True
            else:
                ensure_node_has_url_property(node)
                stripped_request = strip_hash_bookmark_from_url(request.path)
                stripped_node_url = strip_hash_bookmark_from_url(node["url"])
                if stripped_request.startswith(stripped_node_url):
                    match = True

    return match


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu.html", takes_context=True)
def render_menu(context):
    """Render out the sidebar menu"""

    use_menu_group_separator = getattr(
        settings,
        "ADMINLTE2_USE_MENU_GROUP_SEPARATOR",
        True,
    )

    include_admin_nav = getattr(
        settings,
        "ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES",
        False,
    )

    separator = {
        "text": "",
        "nodes": [],
        "separator": True,
    }

    default_menu = MENU if _default_routes_are_registered() else []

    menu_first = context.get("ADMINLTE2_MENU_FIRST", [])
    menu_main = context.get(
        "ADMINLTE2_MENU",
        getattr(
            settings,
            "ADMINLTE2_MENU",
            default_menu,
        ),
    )
    menu_admin = AdminMenu.create_menu(context) if include_admin_nav else []
    menu_last = context.get("ADMINLTE2_MENU_LAST", [])

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
        "section_list": section_list,
        "user": context["user"],  # render_section needs this
        "request": context["request"],  # render_tree needs this
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_section.html", takes_context=True)
def render_section(context, section):
    """Render out an entire sidebar section"""
    nodes = section.get("nodes")
    allowed = check_for_one_permission_in_node_list(context["user"], nodes)

    return {
        "section": section,
        "allowed": allowed,
        "user": context["user"],  # render_tree needs this
        "request": context["request"],  # render_tree needs this
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_nodes.html", takes_context=True)
def render_nodes(context, nodes):
    """Render out a list of nodes"""
    return {
        "nodes": nodes,
        "user": context["user"],  # render_tree needs this
        "request": context["request"],  # render_tree needs this
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_tree.html", takes_context=True)
def render_tree(context, node):
    """Render out a menu tree"""
    nodes = node.get("nodes")
    allowed = check_for_one_permission_in_node_list(context["user"], nodes)
    add_display_block = check_for_node_that_matches_request_path(context["request"], nodes)

    if not node.get("icon"):
        node["icon"] = "not-found"

    return {
        "node": node,
        "allowed": allowed,
        "add_display_block": add_display_block,
        "user": context["user"],
        "request": context["request"],
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_link.html", takes_context=True)
def render_link(context, node):
    """Render out a menu link"""
    default = {
        "class": "",
        "attributes": {},
    }

    print("\n\n\n\n")
    print("render_link():")
    print("    context: {0}".format(context))
    print("    node: {0}".format(node))
    print("    default: {0}".format(default))

    default.update(node)
    node = default

    print("")
    print("    updated_node: {0}".format(node))

    ensure_node_has_url_property(node)

    allowed = is_allowed_node(context["user"], node)

    text = node.get("text") or ""
    title = text
    hook = node.get("hook")  # 'path.to.function' that will return text
    if hook:
        # NOTE: hook should return 'text' or a tuple ('text', 'title text')
        hook_args = node.get("hook_args", [])
        hook_kwargs = node.get("hook_kwargs", {})
        text_func = import_string(hook)
        text = title = text_func(*hook_args, context=context, **hook_kwargs)
        try:
            text, title = text
        except ValueError:
            pass  # A tuple wasn't returned, assume just text

    node["text"] = text
    node["title"] = title

    if not node.get("icon"):
        node["icon"] = ""

    return {
        "node": node,
        "allowed": allowed,
        "request": context["request"],
    }


@register.filter
def url_starts_with(search_string, sub_string):
    """Determine if a url starts with a sub string"""
    stripped_search_string = strip_hash_bookmark_from_url(search_string)
    stripped_sub_string = strip_hash_bookmark_from_url(sub_string)
    return stripped_search_string.startswith(stripped_sub_string)


def _default_routes_are_registered():
    """Determine if the default routes provided by the package are registered for use"""
    try:
        _ = reverse("password_change")
        _ = reverse("adminlte2_pdq:home")
        _ = reverse("adminlte2_pdq:demo-css")
        _ = reverse("adminlte2_pdq:register")
        _ = reverse("adminlte2_pdq:sample_form")
        _ = reverse("adminlte2_pdq:sample1")
        _ = reverse("adminlte2_pdq:sample2")
    except NoReverseMatch:
        return False
    return True
