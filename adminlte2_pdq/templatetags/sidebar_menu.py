"""
Django AdminLTE2 Sidebar Template Tags

Template tags and logic for rendering sidebar menu
"""

# Third-Party Imports.
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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


# region Render Functions


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu.html", takes_context=True)
def render_menu(context):
    """Render out the sidebar menu.

    A menu is the entire menu on the sidebar.
    """

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
    """Render out an entire sidebar section.

    A section is a grouping of items within the menu.
    """
    nodes = section.get("nodes")
    allowed = check_for_one_permission_in_node_list(context["user"], nodes)

    return {
        "section": section,
        "allowed": allowed,
        "user": context["user"],  # render_tree needs this
        "request": context["request"],  # render_tree needs this
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_tree.html", takes_context=True)
def render_tree(context, node):
    """Render out a menu tree.

    A tree is an optional, expandable item with nodes within it.
    """
    ensure_node_has_url_property(node, required=False)
    nodes = node.get("nodes")
    allowed = check_for_one_permission_in_node_list(context["user"], nodes)
    add_display_block = check_for_node_that_matches_request_path(context["request"], nodes)

    if not node.get("icon"):
        node["icon"] = "not-found"

    active = False
    if _determine_node_active_status(node, context["request"]):
        active = True
    for inner_node in node["nodes"]:
        if _determine_node_active_status(inner_node, context["request"]):
            active = True
    node["active"] = active

    return {
        "node": node,
        "allowed": allowed,
        "add_display_block": add_display_block,
        "user": context["user"],
        "request": context["request"],
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_nodes.html", takes_context=True)
def render_nodes(context, nodes):
    """Render out a list of nodes.

    A node is an individual clickable item within the menu.
    """
    return {
        "nodes": nodes,
        "user": context["user"],  # render_tree needs this
        "request": context["request"],  # render_tree needs this
    }


@register.inclusion_tag("adminlte2/partials/_main_sidebar/_menu_link.html", takes_context=True)
def render_link(context, node):
    """Render out a menu link.

    A menu link is the clickable link within a given node.
    """
    default = {
        "class": "",
        "attributes": {},
    }

    default.update(node)
    node = default

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

    node["active"] = _determine_node_active_status(node, context["request"])

    return {
        "node": node,
        "allowed": allowed,
        "request": context["request"],
    }


# endregion Render Functions


# region Permission Handling Functions


def get_permissions_from_view(view):
    """Get the permission/access data from a view."""

    view_data = {}
    view_class = getattr(view.func, "view_class", None)

    # Get extra AdminLtePdq data, if available.
    if view_class:
        # Is class-based view.

        # Get AdminLte class data dict.
        admin_pdq_data = getattr(view_class, "admin_pdq_data", {})

        permission_required_one_value = getattr(view_class, "permission_required_one", None)
        permission_required_value = getattr(view_class, "permission_required", None)

    else:
        # Is function-based view. Get AdminLte function data dict.
        admin_pdq_data = getattr(view.func, "admin_pdq_data", {})

        permission_required_one_value = getattr(view.func, "permission_required_one", None)
        permission_required_value = getattr(view.func, "permission_required", None)

    view_data["decorator_name"] = admin_pdq_data.get("decorator_name", "")
    view_data["allow_anonymous_access"] = admin_pdq_data.get("allow_anonymous_access", None)
    view_data["login_required"] = admin_pdq_data.get("login_required", None)
    view_data["allow_without_permissions"] = admin_pdq_data.get("allow_without_permissions", None)
    view_data["one_of_permissions"] = permission_required_one_value
    view_data["full_permissions"] = permission_required_value

    return view_data


def get_permissions_from_node(node):
    """Gets the permission/access data for provided node.

    If values are defined on the node itself, then those values take priority over all else.

    If node is missing one or more values, then logic falls back to the view, if the values are
    defined there as per the associated decorators/mixins.

    If the view also is missing one or more values, then logic falls back to expected default
    behavior as per project settings. Mostly those defined by STRICT mode and LOGIN_REQUIRED mode.
    """

    err_str__anonymous_and_login_required = "Cannot allow_anonymous_access and have login_required at the same time."
    err_str__without_perms_and_perms_required = (
        "Cannot allow_without_perms and have permissions required at the same time."
    )
    err_str__anonymous_permissions = (
        "Cannot allow_anonymous_access while having permission requirements at the same time."
    )

    # Get permissions and login_required defined directly on the node.
    node_allow_anonymous_access = node.get("allow_anonymous_access", None)
    node_login_required = node.get("login_required", None)
    node_allow_without_permissions = node.get("allow_without_permissions", None)
    node_one_of_permissions = node.get("one_of_permissions", None)
    node_full_permissions = node.get("permissions", None)

    # If any of these are strings, set as iterables.
    if isinstance(node_one_of_permissions, str):
        node_one_of_permissions = (node_one_of_permissions,)
    if isinstance(node_full_permissions, str):
        node_full_permissions = (node_full_permissions,)

    # Raise errors for configurations that don't make sense for node level.
    # Note: one_of_permission and full_permissions can be set at the same time.
    #   In which case they overlap. So requires all of one permission set, plus at least one of a second set.
    if node_allow_anonymous_access and node_login_required:
        # Setting conflicting login_required states.
        raise ImproperlyConfigured(err_str__anonymous_and_login_required)
    if (
        # So black doesn't one-line this.
        node_allow_without_permissions
        and (node_one_of_permissions or node_full_permissions)
    ):
        # Setting conflicting permission states.
        raise ImproperlyConfigured(err_str__without_perms_and_perms_required)
    if (
        # So black doesn't one-line this.
        node_allow_anonymous_access
        and (node_one_of_permissions or node_full_permissions)
    ):
        # Can't have anonymous and permission requirements.
        raise ImproperlyConfigured(err_str__anonymous_permissions)

    # Skip checking if all values are set.
    # Required as a work-around for default Django behavior, when rendering
    # an admin page link. If additional permission values are added, they MUST
    # also be added here and then defined on the default node in admin_menu.py.
    if (
        node_allow_anonymous_access is not None
        and node_login_required is not None
        and node_allow_without_permissions is not None
        and node_one_of_permissions is not None
        and node_full_permissions is not None
    ):
        return {
            "allow_anonymous_access": node_allow_anonymous_access,
            "login_required": node_login_required,
            "allow_without_permissions": node_allow_without_permissions,
            "one_of_permissions": node_one_of_permissions,
            "full_permissions": node_full_permissions,
            # Special case for handling a view in STRICT POLICY WHITELIST but the node says permission is required.
            "node_requires_permissions": (bool(node_one_of_permissions) or bool(node_full_permissions)),
        }

    # Default our values to None.
    view_allow_anonymous_access = None
    view_login_required = None
    view_allow_without_permissions = None
    view_one_of_permissions = None
    view_full_permissions = None

    # Get the view from the node.
    view = get_view_from_node(node)

    # If there is a view, use it to get the view permissions and login_required.
    if view:
        view_data = get_permissions_from_view(view)
        view_allow_anonymous_access = view_data["allow_anonymous_access"]
        view_login_required = view_data["login_required"]
        view_allow_without_permissions = view_data["allow_without_permissions"]
        view_one_of_permissions = view_data["one_of_permissions"]
        view_full_permissions = view_data["full_permissions"]

        # If any of these are strings, set as iterables.
        if isinstance(view_one_of_permissions, str):
            view_one_of_permissions = (view_one_of_permissions,)
        if isinstance(view_full_permissions, str):
            view_full_permissions = (view_full_permissions,)

    # Raise errors for configurations that don't make sense for view level.
    # Should handle effectively the same as above node error checks. Just at the view level.
    if view_allow_anonymous_access and view_login_required:
        # Setting conflicting login_required states.
        raise ImproperlyConfigured(err_str__anonymous_and_login_required)
    if (
        # So black doesn't one-line this.
        view_allow_without_permissions
        and (view_one_of_permissions or view_full_permissions)
    ):
        # Setting conflicting permission states.
        raise ImproperlyConfigured(err_str__without_perms_and_perms_required)
    if (
        # So black doesn't one-line this.
        view_allow_anonymous_access
        and (view_one_of_permissions or view_full_permissions)
    ):
        # Can't have anonymous and permission requirements.
        raise ImproperlyConfigured(err_str__anonymous_permissions)

    # NOTE 1: Order matters for below values.
    #   For all of them, a node value takes precedence, if provided.
    #   If no node value is provided, the view value is used.
    #   Fall back to global default/setting value, if neither of those are set.
    #
    # Note 2: If we made it this far, then it should be impossible for node or
    #   view values to overlap in ways that conflict.
    #   Aka, below logic should be able to pretty comfortably make some
    #   assumptions to help guide permission logic.

    # Check if node allows anonymous.
    allow_anonymous_access = node_allow_anonymous_access
    if allow_anonymous_access is None and not bool(node_login_required):
        # Fall back to view value, as long as node login_required is not also set.
        allow_anonymous_access = view_allow_anonymous_access

    # Check if node requires login.
    login_required = node_login_required
    if login_required is None and not bool(node_allow_anonymous_access):
        # Fall back to view value, as long as node allow_anonymous_access is not also set.
        login_required = view_login_required
    if login_required is None and not bool(node_allow_anonymous_access):
        # Fall back to settings values, as long as node allow_anonymous_access is not also set.
        # If either of these are set, then login should be required.
        login_required = STRICT_POLICY or LOGIN_REQUIRED

    # Check if node allows without permissions.
    allow_without_permissions = node_allow_without_permissions
    if allow_without_permissions is None and not (bool(node_one_of_permissions) or bool(node_full_permissions)):
        # Fall back to view value, as long as node permissions are not set.
        allow_without_permissions = view_allow_without_permissions

    # Check if node requires one of permissions.
    one_of_permissions = node_one_of_permissions
    if one_of_permissions is None and not bool(node_allow_without_permissions):
        # Fall back to view value, as long as node allow_without_permissions is not set.
        one_of_permissions = view_one_of_permissions or []

    # Check if node requires full permissions.
    full_permissions = node_full_permissions
    if full_permissions is None and not bool(node_allow_without_permissions):
        # Fall back to view value, as long as node allow_without_permissions is not set.
        full_permissions = view_full_permissions or []

    # Return calculated values.
    return {
        "allow_anonymous_access": allow_anonymous_access,
        "login_required": login_required,
        "allow_without_permissions": allow_without_permissions,
        "one_of_permissions": one_of_permissions,
        "full_permissions": full_permissions,
        # Special case for handling a view in STRICT POLICY WHITELIST but the node says permission is required.
        "node_requires_permissions": (bool(node_one_of_permissions) or bool(node_full_permissions)),
    }


def is_allowed_node(user, node):
    """Checks if a node is valid for rendering to current user.

    A node is valid for rendering if the user has permissions needed as specified by the
    node, view, or general project settings.

    Values to check against are generally determined by the get_permissions_from_node function.
    If conflicting values are provided, the most strict interpretation is used.
    """

    # Always allow superuser.
    if user.is_superuser:
        return True

    # Start allowed as the opposite of the authentication policy.
    # If we are in LOGIN REQUIRED, should start as failing login checks.
    # If we are in STRICT, should start as failing permission checks.
    passes_login_check = not LOGIN_REQUIRED
    passes_permission_check = not STRICT_POLICY

    # Get the permission/access values from the node or node's view.
    return_data = get_permissions_from_node(node)

    allow_anonymous_access = return_data["allow_anonymous_access"]
    login_required = return_data["login_required"]
    allow_without_permissions = return_data["allow_without_permissions"]
    one_of_permissions = return_data["one_of_permissions"]
    full_permissions = return_data["full_permissions"]
    # Special case for handling a view in STRICT POLICY WHITELIST but the node says permission is required.
    node_requires_permissions = return_data["node_requires_permissions"]

    # If node allows anonymous, then anyone can access, regardless of any other settings.
    if allow_anonymous_access:
        passes_login_check = True
        passes_permission_check = True

    # If the node requires being logged in, or the login required middleware is active.
    elif login_required or LOGIN_REQUIRED:
        # Some iteration of login is required.
        # Verify user is authenticated or the route for the node is whitelisted in the login exempt whitelist.
        passes_login_check = user.is_authenticated or check_for_login_whitelisted_node(node)

    # If node allows without permissions, then all users pass permission checks.
    if allow_without_permissions:
        passes_permission_check = True

    # Check if view is in permission whitelist, so long as node doesn't specify permissions required.
    elif not node_requires_permissions and check_for_strict_whitelisted_node(node):
        passes_permission_check = True

    # Otherwise if any permission values exist, user needs to pass a permission check.
    elif one_of_permissions or full_permissions:

        # TODO: I'm so tired, I suspect I messed this logic up?
        #   Verify permission-access node tests when more rested.
        #   The goal of this is to allow views that either need one_permission or full_permissions.
        #   In such a case, the user should be able to pass the single check without worrying about the other.
        #   .
        #   But also needs to allow stacking requirements so that a node/view can define and require both values.
        #   In the case of using both, the user needs to have all of the perms in full_permissions AND at least one
        #   perm in one_of_permissions.
        #   .
        #   Tests seemed fine when going through them, but now looking at this final logic I have here, I
        #   suspect it's possibly too relaxed.
        #   Specifically, in cases where one_permission or full_permissions are defined, but no values are passed in,
        #   does this fail? I don't know if we have any tests for that on the node level.

        # Default to passing checks.
        passes_one_check = True
        passes_all_check = True

        # Check if one permission required.
        if one_of_permissions:
            passes_one_check = check_for_one_permission(user, one_of_permissions)

        # Check if all permissions required.
        if full_permissions:
            passes_all_check = check_for_all_permissions(user, full_permissions)

        # Final result is the combination of these two.
        passes_permission_check = passes_one_check and passes_all_check

    # Return true if passes both types of checks. False otherwise.
    return passes_login_check and passes_permission_check


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

    # Compare the user's perms against the passed in permissions, ensuring the user at least one of them.
    # We only run this check if any permissions were passed at all.
    if permissions:
        for permission in permissions:
            if user.has_perm(permission):
                allowed = True
                break

    return allowed


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

    allowed = False

    # Compare the user's perms against the passed in permissions, ensuring the user has all of them.
    # We only run this check if any permissions were passed at all.
    if permissions:
        allowed = True
        if not user.has_perms(permissions):
            allowed = False

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


def check_for_login_whitelisted_node(node):
    """Check to see if the route property on the node is in the login whitelist"""
    return node.get("route") in LOGIN_EXEMPT_WHITELIST


def check_for_strict_whitelisted_node(node):
    """Check to see if the route property on the node is in the whitelist"""
    return node.get("route") in STRICT_POLICY_WHITELIST


# endregion Permission Handling Functions


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


def ensure_node_has_url_property(node, required=True):
    """Ensure that a node has a url property"""
    if "url" not in node:
        try:
            route = node["route"] if required else node.get("route", "#")
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


def strip_hash_bookmark_from_url(url):
    """Strip the hash bookmark from a string url"""
    return (url or "").split("#")[0]


def _url_starts_with(search_string, sub_string):
    """Determine if a url starts with a sub string"""
    stripped_search_string = strip_hash_bookmark_from_url(search_string)
    stripped_sub_string = strip_hash_bookmark_from_url(sub_string)
    return stripped_search_string.startswith(stripped_sub_string)


def _determine_node_active_status(node, request):
    """Determine if a node should be active"""
    active = False
    if node.get("active_requires_exact_url_match", False):
        if request.path == node["url"]:
            active = True
    else:
        if _url_starts_with(request.path, node["url"]):
            active = True
    return active


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
