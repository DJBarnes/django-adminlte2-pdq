"""
Tests for which sidebar menu nodes a user can see (is_allowed_node), in each policy mode.
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.

# Internal Imports.
from adminlte2_pdq.templatetags import sidebar_menu
from tests.django_adminlte2_pdq.tests.core.menu.base_test_case import SidebarMenuBaseTestCase


# Module Variables.


class NodeVisibilityTestCase(SidebarMenuBaseTestCase):
    """Tests for is_allowed_node() function in sidebar logic."""

    # region Loose Mode, Standard Settings

    def test__standard__node_minimal(self):
        """Tests for node with no auth requirements defined on a basic no-auth view.
        Aka, the "standard" case.
        """

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__standard__node_allow_anonymous_access(self):
        """Test standard node allow anonymous access"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_anonymous_access": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__standard__node_login_required(self):
        """Test standard node login required"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__standard__node_allow_without_permissions(self):
        """
        Note: Technically this state doesn't make sense, and would not be achievable under normal
            middleware handling. Without login_required, this will always return True.
        # Todo: Should at least raise a warning anytime logic occurs that has no effect, such as this.
        """

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_without_permissions": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__standard__node_one_permission_required(self):
        """Test standard node one permission required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__standard__node_full_permissions_required(self):
        """Test standard node full permission required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Loose Mode, Standard Settings

    # region LoginRequired Mode, No Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_minimal(self):
        """Test login required no whitelists node minimal"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_allow_anonymous_access(self):
        """Test login required no whitelist node allow anonymous access"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_anonymous_access": True,
        }

        with self.subTest("As anonymous user"):
            # Note: See above note for allow_anonymous_access test with anonymous user.

            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_login_required(self):
        """Test login required no whitelists node login required"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_allow_without_permissions(self):
        """Test login required no whitelists node allow without permissions"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_without_permissions": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_one_permission_required(self):
        """Test login required no whitelists node one permission required"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_full_permissions_required(self):
        """Test login required no whitelists node full permissions required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion LoginRequired Mode, No Whitelist

    # region LoginRequired Mode, Login Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_minimal(self):
        """Test login required with login whitelist node minimal."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_allow_anonymous_access(self):
        """Test login required with login whitelist node allow anonymous access."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_anonymous_access": True,
        }

        with self.subTest("As anonymous user"):
            # Note: See above note for allow_anonymous_access test with anonymous user.

            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_login_required(self):
        """Test login required with login whitelist node login required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_allow_without_permissions(self):
        """Test login required with login whitelist node allow without permissions."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_without_permissions": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_one_permission_required(self):
        """Test login required with login whitelist node one permission required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_full_permissions_required(self):
        """Test login required with login whitelist node full permissions required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion LoginRequired Mode, Login Whitelist

    # region Strict Mode, No Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_minimal(self):
        """Test strict no whitelists node minimal."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_allow_anonymous_access(self):
        """Test strict no whitelists node allow anonymous access."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_anonymous_access": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_login_required(self):
        """Test strict no whitelists node login required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_allow_without_permissions(self):
        """Test strict no whitelists node allow without permissions."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_without_permissions": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_one_permission_required(self):
        """Test strict no whitelists node one permission required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_full_permissions_required(self):
        """Test strict no whitelists node full permissions required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, No Whitelist

    # region Strict Mode, Login Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_login_whitelist__node_minimal(self):
        """
        NOTE: The LOGIN_EXEMPT_WHITELIST is only for login access.
            If the view is not also put into the PERMISSION_EXEMPT_WHITELIST, then the login
            whitelist effectively does nothing. This is because permissions are still required,
            and to have permissions, a user needs to be logged in.

        # TODO: In fact, this should probably provide a warning when put into this state.
        """

        # # Node used for all subtests.
        # node = {
        #     "route": "adminlte2_pdq:demo-css",
        #     "text": "Demo CSS",
        #     "icon": "fa fa-file",
        # }
        #
        # with self.subTest("As anonymous user"):
        #     # Get user to run subtest on.
        #     self._setup_anonymous_user()
        #
        #     # Test sidebar logic.
        #     allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
        #     self.assertFalse(allowed)

    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)
    #
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_allow_anonymous_access(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous_access": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)
    #
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_login_required(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "login_required": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)
    #
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)
    #
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_one_permission_required(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "one_of_permissions": ["auth.add_foo"],
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)
    #
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_full_permissions_required(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "permissions": ["auth.add_foo", "auth.change_foo"],
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(permissions=["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    # endregion Strict Mode, Login Whitelist

    # region Strict Mode, Permission Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_minimal(self):
        """Test strict with permission whitelist node minimal."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_allow_anonymous_access(self):
        """Test strict with permission whitelist node allow anonymous access."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_anonymous_access": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_login_required(self):
        """Test strict with permission whitelist node login required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_allow_without_permissions(self):
        """Test strict with permission whitelist node allow without permissions."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_without_permissions": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_one_permission_required(self):
        """Test strict with permission whitelist node one permission required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_full_permissions_required(self):
        """Test strict with permission whitelist node full permissions required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Permission Whitelist

    # region Strict Mode, Both Whitelists

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_minimal(self):
        """Test strict with both whitelists node minimal."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_allow_anonymous_access(self):
        """Test strict with both whitelists node allow anonymous access."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_anonymous_access": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_login_required(self):
        """Test strict with both whitelists node login required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_allow_without_permissions(self):
        """Test strict with both whitelists node allow without permissions."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "allow_without_permissions": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_one_permission_required(self):
        """Test strict with both whitelists node one permission required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_full_permissions_required(self):
        """Test strict with both whitelists node full permissions required."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Both Whitelists
