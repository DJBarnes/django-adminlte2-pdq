"""
Tests for nodes that define their own access settings, which is_allowed_node() uses instead of the view's.

Each table lists, for one policy setup, whether a node is shown (Y) or hidden (N) for each node setting and each kind
of user. The node links to the package's demo-css view, which has no decorator or mixin. A failure names the policy
setup (the test), the node setting, and the user.
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.

# Internal Imports.
from tests.django_adminlte2_pdq.tests.core.menu.base_test_case import N, SidebarMenuBaseTestCase, Y


# Module Variables.
ROUTE = "adminlte2_pdq:demo-css"

# Each row's node setting. "none" is a node with only a route, text, and icon. The "(two)" row needs either of two
# permissions, so a user with only one of them shows the difference between one_of_permissions and permissions.
# A node with both settings needs to pass both. Users with full permissions pass both (add_foo, and change_foo but not
# view_foo); users with partial permissions pass only permissions, and users with wrong permissions only one_of.
NODE_SETTINGS = {
    "none": {},
    "allow_anonymous_access": {"allow_anonymous_access": True},
    "login_required": {"login_required": True},
    "allow_without_permissions": {"allow_without_permissions": True},
    "one_of_permissions": {"one_of_permissions": ["auth.add_foo"]},
    "one_of_permissions (two)": {"one_of_permissions": ["auth.add_foo", "auth.change_foo"]},
    "permissions": {"permissions": ["auth.add_foo", "auth.change_foo"]},
    "one_of_permissions + permissions": {
        "one_of_permissions": ["auth.change_foo", "auth.view_foo"],
        "permissions": ["auth.add_foo"],
    },
}

# Cells:
#   Y = shown
#   N = hidden
#
# Columns (the "user" and "staff" groups each have the no to fg columns):
#   an = anonymous
#   no = no permissions
#   wp = wrong permissions
#   pp = partial permissions
#   fp = full permissions
#   wg = wrong groups
#   pg = partial groups
#   fg = full groups
#   su = superuser
# fmt: off
LOOSE_MODE = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":         (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}

LOGIN_REQUIRED_MODE = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":         (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}

LOGIN_REQUIRED_MODE__LOGIN_WHITELIST = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":         (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}

STRICT_MODE = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_without_permissions":         (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}

STRICT_MODE__LOGIN_WHITELIST = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_without_permissions":         (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}

STRICT_MODE__PERMISSION_WHITELIST = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":         (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}

STRICT_MODE__BOTH_WHITELISTS = {
    #                                         user                   staff
    #                                    an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":            (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                    (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":         (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_of_permissions":                (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_of_permissions (two)":          (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "permissions":                       (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "one_of_permissions + permissions":  (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
}
# fmt: on


class NodeVisibilityTestCase(SidebarMenuBaseTestCase):
    """Tests for nodes with their own access settings."""

    def assert_visibility(self, table):
        """Check every node setting and user in a table."""
        self.assertEqual(list(table), list(NODE_SETTINGS), "The table must have a row for every node setting.")
        users = self._create_table_users()
        for setting, row in table.items():
            node = {"route": ROUTE, "text": "Test Node", "icon": "fa fa-file", **NODE_SETTINGS[setting]}
            self.assert_node_visibility(users, node, row, node_setting=setting)

    def test__loose_mode(self):
        """Loose mode."""
        self.assert_visibility(LOOSE_MODE)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode(self):
        """Login-required mode, no whitelists."""
        self.assert_visibility(LOGIN_REQUIRED_MODE)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", [ROUTE])
    def test__login_required_mode__login_whitelist(self):
        """Login-required mode, the route in the login whitelist."""
        self.assert_visibility(LOGIN_REQUIRED_MODE__LOGIN_WHITELIST)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode(self):
        """Strict mode, no whitelists."""
        self.assert_visibility(STRICT_MODE)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", [ROUTE])
    def test__strict_mode__login_whitelist(self):
        """Strict mode, the route in the login whitelist.

        The login whitelist only lets anonymous users pass the login check. Permissions are still required.
        """
        self.assert_visibility(STRICT_MODE__LOGIN_WHITELIST)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", [ROUTE])
    def test__strict_mode__permission_whitelist(self):
        """Strict mode, the route in the permission whitelist."""
        self.assert_visibility(STRICT_MODE__PERMISSION_WHITELIST)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", [ROUTE])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", [ROUTE])
    def test__strict_mode__both_whitelists(self):
        """Strict mode, the route in both whitelists."""
        self.assert_visibility(STRICT_MODE__BOTH_WHITELISTS)
