"""
Tests for the sidebar menu's node helpers: permissions, urls, whitelists, and active state.
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.test import override_settings, RequestFactory
from django.urls import NoReverseMatch

# Internal Imports.
from adminlte2_pdq.templatetags import sidebar_menu
from tests.django_adminlte2_pdq.tests.core.menu.base_test_case import SidebarMenuBaseTestCase


# Module Variables.
HOME = "adminlte2_pdq:home"
DEMO_CSS = "adminlte2_pdq:demo-css"
EXTERNAL_URL = "https://github.com"

# The sample views' permissions: sample1 requires all of them, sample2 one of them. Both also require login.
SAMPLE1_PERMISSIONS = ["auth.add_group", "auth.change_group", "auth.delete_group"]
SAMPLE2_PERMISSIONS = ["auth.add_permission", "auth.change_permission", "auth.delete_permission"]

# What get_permissions_from_node() returns for a node without any settings, or that links to a view without any.
NO_PERMISSIONS = {
    "allow_anonymous_access": False,
    "login_required": False,
    "allow_without_permissions": False,
    "one_of_permissions": [],
    "full_permissions": [],
    "node_requires_permissions": False,
}

# Each node's settings (besides its text and icon), and how its result differs from NO_PERMISSIONS. A setting on the
# node is used instead of the view's. node_requires_permissions is True when the node itself sets permissions.
PERMISSIONS_FROM_NODE = {
    "hash route": ({"route": "#"}, {}),
    "view without settings": ({"route": HOME}, {}),
    "external url": ({"route": "#", "url": EXTERNAL_URL}, {}),
    # login_required.
    "login_required on the node": ({"route": DEMO_CSS, "login_required": True}, {"login_required": True}),
    "login_required from the view": ({"route": "adminlte2_pdq:sample_form"}, {"login_required": True}),
    "login_required from the view, by url": ({"route": "#", "url": "/sample_form/"}, {"login_required": True}),
    "login_required on the node and the view": (
        {"route": "adminlte2_pdq:sample_form", "login_required": False},
        {},
    ),
    "login_required on a node with an external url": (
        {"route": "#", "url": EXTERNAL_URL, "login_required": True},
        {"login_required": True},
    ),
    # one_of_permissions.
    "one_of_permissions on the node": (
        {"route": DEMO_CSS, "one_of_permissions": ["add_sample2", "update_sample2"]},
        {"one_of_permissions": ["add_sample2", "update_sample2"], "node_requires_permissions": True},
    ),
    "one_of_permissions on the node, as a string": (
        {"route": DEMO_CSS, "one_of_permissions": "add_sample2"},
        {"one_of_permissions": ["add_sample2"], "node_requires_permissions": True},
    ),
    "one_of_permissions from the view": (
        {"route": "adminlte2_pdq:sample2"},
        {"login_required": True, "one_of_permissions": SAMPLE2_PERMISSIONS},
    ),
    "one_of_permissions from the view, by url": (
        {"route": "#", "url": "/sample2/"},
        {"login_required": True, "one_of_permissions": SAMPLE2_PERMISSIONS},
    ),
    "one_of_permissions on the node and the view": (
        {"route": "adminlte2_pdq:sample2", "one_of_permissions": []},
        {"login_required": True},
    ),
    "one_of_permissions on a node with an external url": (
        {"route": "#", "url": EXTERNAL_URL, "one_of_permissions": ["add_sample2", "update_sample2"]},
        {"one_of_permissions": ["add_sample2", "update_sample2"], "node_requires_permissions": True},
    ),
    # permissions.
    "permissions on the node": (
        {"route": DEMO_CSS, "permissions": ["add_sample1", "update_sample1"]},
        {"full_permissions": ["add_sample1", "update_sample1"], "node_requires_permissions": True},
    ),
    "permissions on the node, as a string": (
        {"route": DEMO_CSS, "permissions": "add_sample1"},
        {"full_permissions": ["add_sample1"], "node_requires_permissions": True},
    ),
    "permissions from the view": (
        {"route": "adminlte2_pdq:sample1"},
        {"login_required": True, "full_permissions": SAMPLE1_PERMISSIONS},
    ),
    "permissions from the view, by url": (
        {"route": "#", "url": "/sample1/"},
        {"login_required": True, "full_permissions": SAMPLE1_PERMISSIONS},
    ),
    "permissions on the node and the view": (
        {"route": "adminlte2_pdq:sample1", "permissions": []},
        {"login_required": True},
    ),
    "permissions from stacked view decorators": (
        {"route": "adminlte2_pdq_tests:function-stacked-permissions-required"},
        {
            "login_required": True,
            "one_of_permissions": ["auth.view_foo", "auth.delete_foo"],
            "full_permissions": ["auth.add_foo", "auth.change_foo"],
        },
    ),
    "permissions on a node with an external url": (
        {"route": "#", "url": EXTERNAL_URL, "permissions": ["add_sample1", "update_sample1"]},
        {"full_permissions": ["add_sample1", "update_sample1"], "node_requires_permissions": True},
    ),
}

# Node settings that conflict. Each raises ImproperlyConfigured, whether set on the node or on the linked view.
CONFLICTING_SETTINGS = {
    "allow_anonymous_access and login_required": {"allow_anonymous_access": True, "login_required": True},
    "allow_without_permissions and permissions": {"allow_without_permissions": True, "permissions": ["foobar"]},
    "allow_anonymous_access and permissions": {"allow_anonymous_access": True, "permissions": ["foobar"]},
}

# Each node's settings, the exact and fuzzy whitelists, and whether the node is whitelisted.
WHITELISTED_NODES = {
    "route in the whitelist": ({"route": "adminlte2_pdq:sample2"}, ["adminlte2_pdq:sample2"], (), True),
    "route not in the whitelist": ({"route": "adminlte2_pdq:sample2"}, ["adminlte2_pdq:sample1"], (), False),
    "path in the whitelist": ({"route": "adminlte2_pdq:sample2"}, ["/sample2/"], (), True),
    "url name in the whitelist": ({"route": "adminlte2_pdq:sample2"}, ["sample2"], (), True),
    "url set on the node": ({"route": "#", "url": "/sample2/"}, ["adminlte2_pdq:sample2"], (), True),
    "path starts with a fuzzy entry": ({"route": "adminlte2_pdq:sample2"}, [], ("/sample2",), True),
    "path doesn't start with a fuzzy entry": ({"route": "adminlte2_pdq:sample2"}, [], ("/sample1",), False),
    "hash route in the whitelist": ({"route": "#"}, ["#"], (), True),
    "hash route": ({"route": "#"}, [], ("/",), False),
    "external url": ({"route": "#", "url": EXTERNAL_URL}, [EXTERNAL_URL], ("https://",), False),
    "url that doesn't resolve": ({"route": "#", "url": "/no-such-page/"}, [], ("/no-such",), True),
    "route that doesn't exist": ({"route": "foobar"}, [], ("/",), False),
}

# Each staff user's permissions and the permissions checked, and whether check_for_one_permission() and
# check_for_all_permissions() pass. "superuser" is a superuser without permissions.
PERMISSION_CHECKS = {
    "missing permission": ([], ["user_does_not_have_this_one"], False, False),
    "one of two permissions": (["add_group"], ["auth.add_group", "auth.update_group"], True, False),
    "all permissions": (["add_group"], ["auth.add_group"], True, True),
    "no permissions to check": (["add_group"], [], False, False),
    "superuser": ("superuser", ["does_not_matter_since_superuser"], True, True),
}

# Each request path, whether the node needs an exact url match, and whether a node for /home/ is active.
ACTIVE_STATUS = {
    "exact match": ("/home/", False, True),
    "starts with": ("/home/some/sub/url/", False, True),
    "no match": ("/homey_da_clown/", False, False),
    "exact match, exact required": ("/home/", True, True),
    "starts with, exact required": ("/home/some/sub/url/", True, False),
}


def nest(node, depth):
    """Put the node in a menu tree, at the given depth (1 = top level). Returns the top-level node list."""
    nodes = [node]
    for level in range(depth - 1, 0, -1):
        nodes = [{"text": f"Tree level {level}", "icon": "fa fa-leaf", "nodes": nodes}]
    return nodes


def sample2_node():
    """A node for the sample2 view, which requires one of the add, change, or delete permission permissions."""
    return {"route": "adminlte2_pdq:sample2", "text": "Sample2", "icon": "fa fa-building"}


class SidebarMenuHelpersTestCase(SidebarMenuBaseTestCase):
    """
    Tests basic logic for sidebar Template Tags and Helper functions used in those template tags.
    """

    def _superuser(self):
        """The superuser, created on first use."""
        if not self.super_user:
            self._setup_super_user()
        return self.super_user

    # region Demo Url

    def test__default_routes_are_registered_function__works_when_routes_are_registered(self):
        """Test default routes are registered function works when routes are registered"""
        # pylint:disable=protected-access
        self.assertTrue(sidebar_menu._default_routes_are_registered())

    @override_settings(ROOT_URLCONF="tests.django_adminlte2_pdq.django_test_project.urls_empty")
    def test__default_routes_are_registered_function__fails_when_routes_are_not_registered(self):
        """Test default routes are registered function fails when routes are not registered"""
        # pylint:disable=protected-access
        self.assertFalse(sidebar_menu._default_routes_are_registered())

    # endregion Demo Url

    # region get_permissions_from_node() Function

    def test__get_permissions_from_node(self):
        """The permission settings come from the node, or else from the view it links to."""
        for name, (settings, differences) in PERMISSIONS_FROM_NODE.items():
            with self.subTest(node=name):
                node = {"text": "Sample", "icon": "fa fa-file", **settings}

                result = sidebar_menu.get_permissions_from_node(node)

                # The allow_* settings may be None or False when unset, and the permissions a list or tuple.
                actual = {
                    key: list(result[key]) if key in ("one_of_permissions", "full_permissions") else bool(result[key])
                    for key in NO_PERMISSIONS
                }
                self.assertEqual({**NO_PERMISSIONS, **differences}, actual)

    def test__get_permissions_from_node__missing_route(self):
        """A node without a route raises KeyError."""
        with self.assertRaises(KeyError) as err:
            sidebar_menu.get_permissions_from_node({"text": "Sample1", "icon": "fa fa-group"})
        self.assertEqual(self.node_error__key_error_message, str(err.exception))

    def test__get_permissions_from_node__invalid_route(self):
        """A node with a route that doesn't exist raises NoReverseMatch."""
        with self.assertRaises(NoReverseMatch) as err:
            sidebar_menu.get_permissions_from_node({"route": "foobar", "text": "Sample1", "icon": "fa fa-group"})
        self.assertEqual(self.node_error__invalid_route_message, str(err.exception))

    def test__get_permissions_from_node__conflicting_node_settings(self):
        """A node with conflicting settings raises ImproperlyConfigured."""
        for name, settings in CONFLICTING_SETTINGS.items():
            with self.subTest(settings=name):
                node = {"route": "foobar", "text": "Sample1", "icon": "fa fa-group", **settings}

                with self.assertRaises(ImproperlyConfigured):
                    sidebar_menu.get_permissions_from_node(node)

    def test__get_permissions_from_node__conflicting_view_settings(self):
        """A node that links to a view with conflicting settings raises ImproperlyConfigured."""
        for name, settings in CONFLICTING_SETTINGS.items():
            with self.subTest(settings=name):
                node = {"route": HOME, "text": "Sample1", "icon": "fa fa-group"}
                view_data = {
                    "allow_anonymous_access": settings.get("allow_anonymous_access", False),
                    "login_required": settings.get("login_required", False),
                    "allow_without_permissions": settings.get("allow_without_permissions", False),
                    "one_of_permissions": settings.get("permissions"),
                    "full_permissions": None,
                }

                with patch("adminlte2_pdq.templatetags.sidebar_menu.get_permissions_from_view") as view_permissions:
                    view_permissions.return_value = view_data
                    with self.assertRaises(ImproperlyConfigured):
                        sidebar_menu.get_permissions_from_node(node)

    # endregion get_permissions_from_node() Function

    # region ensure_node_has_url_property() Function

    def test__ensure_node_has_url_property(self):
        """The node's url is kept if set, otherwise built from its route."""
        urls = {
            "url already set": ({"route": "adminlte2_pdq:sample2", "url": "/foobar/"}, "/foobar/"),
            "url from the route": ({"route": "adminlte2_pdq:sample2"}, "/sample2/"),
            "hash route": ({"route": "#"}, "#"),
        }
        for name, (settings, expected_url) in urls.items():
            with self.subTest(node=name):
                node = {"text": "Sample2", "icon": "fa fa-building", **settings}

                sidebar_menu.ensure_node_has_url_property(node)

                self.assertEqual(expected_url, node["url"])

    def test__ensure_node_has_url_property__missing_route(self):
        """A node without a route raises KeyError."""
        with self.assertRaises(KeyError) as err:
            sidebar_menu.ensure_node_has_url_property({"text": "Sample2", "icon": "fa fa-building"})
        self.assertEqual(self.node_error__key_error_message, str(err.exception))

    def test__ensure_node_has_url_property__invalid_route(self):
        """A node with a route that doesn't exist raises NoReverseMatch."""
        with self.assertRaises(NoReverseMatch) as err:
            sidebar_menu.ensure_node_has_url_property({"route": "foobar", "text": "Sample2", "icon": "fa fa-building"})
        self.assertEqual(self.node_error__invalid_route_message, str(err.exception))

    # endregion ensure_node_has_url_property() Function

    # region Whitelist Functions

    def test__whitelisted_node(self):
        """A node is whitelisted the same way the middleware whitelists a request."""
        checks = {
            "login": ("check_for_login_whitelisted_node", "LOGIN_EXEMPT_WHITELIST", "LOGIN_EXEMPT_FUZZY_WHITELIST"),
            "permission": (
                "check_for_strict_whitelisted_node",
                "STRICT_POLICY_WHITELIST",
                "STRICT_POLICY_FUZZY_WHITELIST",
            ),
        }
        for whitelist, (function, exact_setting, fuzzy_setting) in checks.items():
            for name, (settings, exact, fuzzy, expected) in WHITELISTED_NODES.items():
                with self.subTest(whitelist=whitelist, node=name):
                    node = {"text": "Sample2", "icon": "fa fa-building", **settings}

                    with patch(f"adminlte2_pdq.templatetags.sidebar_menu.{exact_setting}", exact), patch(
                        f"adminlte2_pdq.templatetags.sidebar_menu.{fuzzy_setting}", fuzzy
                    ):
                        self.assertEqual(expected, getattr(sidebar_menu, function)(node))

    # endregion Whitelist Functions

    # region Permission Check Functions

    def test__check_for_permissions(self):
        """check_for_one_permission() needs one of the permissions, check_for_all_permissions() all of them."""
        for name, (user_permissions, permissions, one_allowed, all_allowed) in PERMISSION_CHECKS.items():
            with self.subTest(user=name):
                if user_permissions == "superuser":
                    user = self._superuser()
                else:
                    self._setup_staff_user(user_permissions)
                    user = self.staff_user

                self.assertEqual(one_allowed, sidebar_menu.check_for_one_permission(user, permissions))
                self.assertEqual(all_allowed, sidebar_menu.check_for_all_permissions(user, permissions))

    def test__check_for_one_permission_in_node_list(self):
        """A user passes if they can open one node in the list, at any depth of the menu tree."""
        users = {"superuser": True, "user with the permission": True, "user without the permission": False}
        for depth in (1, 2, 3):
            for user_name, expected in users.items():
                with self.subTest(depth=depth, user=user_name):
                    if user_name == "superuser":
                        user = self._superuser()
                    else:
                        self._setup_staff_user("add_permission" if expected else "add_group")
                        user = self.staff_user

                    nodes = nest(sample2_node(), depth)

                    self.assertEqual(expected, sidebar_menu.check_for_one_permission_in_node_list(user, nodes))

    # endregion Permission Check Functions

    # region Active Node Functions

    def test__check_for_node_that_matches_request_path__no_nodes(self):
        """An empty node list has no match."""
        request = RequestFactory().get("/sample2/")

        self.assertFalse(sidebar_menu.check_for_node_that_matches_request_path(request, []))

    def test__check_for_node_that_matches_request_path(self):
        """A node at any depth of the menu tree matches the request path of its url."""
        for depth in (1, 2, 3):
            for path, expected in (("/sample2/", True), ("/sample1/", False)):
                with self.subTest(depth=depth, path=path):
                    request = RequestFactory().get(path)
                    nodes = nest(sample2_node(), depth)

                    self.assertEqual(expected, sidebar_menu.check_for_node_that_matches_request_path(request, nodes))

    def test__determine_node_active_status(self):
        """A node is active when the request path starts with its url, or matches it exactly if required."""
        # pylint:disable=protected-access
        for name, (path, exact_required, expected) in ACTIVE_STATUS.items():
            with self.subTest(path=name):
                node = {"url": "/home/", "text": "Sample1", "icon": "fa fa-group"}
                if exact_required:
                    node["active_requires_exact_url_match"] = True
                request = HttpRequest()
                request.path = path

                self.assertEqual(expected, sidebar_menu._determine_node_active_status(node, request))

    # endregion Active Node Functions
