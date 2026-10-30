"""
Tests for nodes without their own permissions, which fall back to the permissions of the view they link to.

Each table lists, for one policy setup, whether a node is shown (Y) or hidden (N) for each kind of view and each kind
of user. Every row is checked twice: for a function view (decorators) and for a class view (mixins). A failure names
the policy setup (the test), the view, and the user.
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission

# Internal Imports.
from adminlte2_pdq.templatetags import sidebar_menu
from tests.django_adminlte2_pdq.tests.core.menu.base_test_case import SidebarMenuBaseTestCase


# Module Variables.
UserModel = get_user_model()

# Each kind of view, and its route. "{view_type}" is "function" or "class".
# "none" is the package's demo-css view, which has no decorator or mixin.
# The "(string)" views define a single permission as a string: auth.add_foo.
VIEW_ROUTES = {
    "none": "adminlte2_pdq:demo-css",
    "allow_anonymous_access": "adminlte2_pdq_tests:{view_type}-allow-anonymous-access",
    "login_required": "adminlte2_pdq_tests:{view_type}-login-required",
    "allow_without_permissions": "adminlte2_pdq_tests:{view_type}-allow-without-permissions",
    "one_permission_required": "adminlte2_pdq_tests:{view_type}-one-permission-required",
    "one_permission_required (string)": "adminlte2_pdq_tests:{view_type}-one-permission-required-as-string",
    "full_permissions_required": "adminlte2_pdq_tests:{view_type}-full-permissions-required",
    "full_permissions_required (string)": "adminlte2_pdq_tests:{view_type}-full-permissions-required-as-string",
}
VIEW_TYPES = ("function", "class")

# Every route above, for the whitelist tests.
VIEW_WHITELIST = sorted(
    {route.format(view_type=view_type) for route in VIEW_ROUTES.values() for view_type in VIEW_TYPES}
)

# The views that require permissions use auth.add_foo and auth.change_foo: "one" views need either, "full" views need
# both, and the "(string)" views need auth.add_foo. Wrong permissions and groups are ones the views don't use.
PERMISSION_SETS = {
    "no permissions": {},
    "wrong permissions": {"permissions": ["view_foo", "delete_foo"]},
    "partial permissions": {"permissions": ["add_foo"]},
    "full permissions": {"permissions": ["add_foo", "change_foo"]},
    "wrong groups": {"groups": ["view_bar", "delete_bar"]},
    "partial groups": {"groups": ["add_bar"]},
    "full groups": {"groups": ["add_bar", "change_bar"]},
}

# The table columns, in order: an = anonymous; for a user and a staff user: no = no permissions,
# wp/pp/fp = wrong/partial/full permissions, wg/pg/fg = wrong/partial/full groups; su = superuser.
USERS = (
    ["anonymous"]
    + [f"user with {name}" for name in PERMISSION_SETS]
    + [f"staff user with {name}" for name in PERMISSION_SETS]
    + ["superuser"]
)

Y = True  # The node is shown.
N = False  # The node is hidden.

# fmt: off
LOOSE_MODE = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":           (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_permission_required (string)":    (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "full_permissions_required":           (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "full_permissions_required (string)":  (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
}

LOGIN_REQUIRED_MODE = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":           (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_permission_required (string)":    (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "full_permissions_required":           (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "full_permissions_required (string)":  (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
}

LOGIN_REQUIRED_MODE__LOGIN_WHITELIST = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":           (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_permission_required (string)":    (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "full_permissions_required":           (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "full_permissions_required (string)":  (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
}

STRICT_MODE = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_without_permissions":           (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_permission_required (string)":    (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "full_permissions_required":           (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "full_permissions_required (string)":  (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
}

STRICT_MODE__LOGIN_WHITELIST = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (N,   N, N, N, N, N, N, N,   N, N, N, N, N, N, N,   Y),
    "allow_without_permissions":           (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "one_permission_required (string)":    (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
    "full_permissions_required":           (N,   N, N, N, Y, N, N, Y,   N, N, N, Y, N, N, Y,   Y),
    "full_permissions_required (string)":  (N,   N, N, Y, Y, N, Y, Y,   N, N, Y, Y, N, Y, Y,   Y),
}

STRICT_MODE__PERMISSION_WHITELIST = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":           (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required (string)":    (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "full_permissions_required":           (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "full_permissions_required (string)":  (N,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
}

STRICT_MODE__BOTH_WHITELISTS = {
    #                                            user                   staff
    #                                       an   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                                (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":              (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                      (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":           (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":             (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required (string)":    (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "full_permissions_required":           (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "full_permissions_required (string)":  (Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
}
# fmt: on


class NodeViewFallbackTestCase(SidebarMenuBaseTestCase):
    """Tests for nodes without permissions, which use the permissions of the view they link to."""

    def _create_user(self, name):
        """Create the user for a table column."""
        if name == "anonymous":
            return AnonymousUser()
        if name == "superuser":
            return UserModel.objects.create(username="superuser", is_superuser=True)
        is_staff = name.startswith("staff user with ")
        permission_set = PERMISSION_SETS[name.split(" with ", 1)[1]]
        user = UserModel.objects.create(username=name.replace(" ", "_"), is_staff=is_staff)
        user.user_permissions.set(Permission.objects.filter(codename__in=permission_set.get("permissions", [])))
        user.groups.set(Group.objects.filter(name__in=permission_set.get("groups", [])))
        return user

    def assert_visibility(self, table):
        """Check every view and user in a table, for function views and class views."""
        self.assertEqual(list(table), list(VIEW_ROUTES), "The table must have a row for every kind of view.")
        users = {name: self._create_user(name) for name in USERS}
        for view_type in VIEW_TYPES:
            for kind, row in table.items():
                self.assertEqual(len(row), len(USERS), f"The {kind} row must have a column for every user.")
                node = {
                    "route": VIEW_ROUTES[kind].format(view_type=view_type),
                    "text": "Test Node",
                    "icon": "fa fa-file",
                }
                for (user_name, user), expected in zip(users.items(), row):
                    with self.subTest(view=f"{view_type} view, {kind}", user=user_name):
                        self.assertEqual(
                            sidebar_menu.is_allowed_node(user, node),
                            expected,
                            f"Expected the node to be {'shown' if expected else 'hidden'}.",
                        )

    def test__group_and_permission_names_exist(self):
        """Every permission and group the users get exists, so no user silently has fewer than intended."""
        for permission_set in PERMISSION_SETS.values():
            for codename in permission_set.get("permissions", []):
                self.assertTrue(Permission.objects.filter(codename=codename).exists(), codename)
            for group in permission_set.get("groups", []):
                self.assertTrue(Group.objects.filter(name=group).exists(), group)

    def test__loose_mode(self):
        """Loose mode."""
        self.assert_visibility(LOOSE_MODE)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode(self):
        """Login-required mode, no whitelists."""
        self.assert_visibility(LOGIN_REQUIRED_MODE)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", VIEW_WHITELIST)
    def test__login_required_mode__login_whitelist(self):
        """Login-required mode, every view in the login whitelist."""
        self.assert_visibility(LOGIN_REQUIRED_MODE__LOGIN_WHITELIST)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode(self):
        """Strict mode, no whitelists."""
        self.assert_visibility(STRICT_MODE)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", VIEW_WHITELIST)
    def test__strict_mode__login_whitelist(self):
        """Strict mode, every view in the login whitelist."""
        self.assert_visibility(STRICT_MODE__LOGIN_WHITELIST)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", VIEW_WHITELIST)
    def test__strict_mode__permission_whitelist(self):
        """Strict mode, every view in the permission whitelist."""
        self.assert_visibility(STRICT_MODE__PERMISSION_WHITELIST)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", VIEW_WHITELIST)
    def test__strict_mode__both_whitelists(self):
        """Strict mode, every view in both whitelists."""
        self.assert_visibility(STRICT_MODE__BOTH_WHITELISTS)
