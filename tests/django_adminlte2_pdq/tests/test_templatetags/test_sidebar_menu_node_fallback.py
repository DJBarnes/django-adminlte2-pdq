"""
Tests for Template Tags
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.
from django.contrib.auth import get_user_model

# Internal Imports.
from .test_sidebar_menu import TemplateTagSidebarMenuBaseTestCase
from adminlte2_pdq.templatetags import sidebar_menu


# Module Variables.
UserModel = get_user_model()


class TemplateTagSidebarMenu__ViewFallbackWhenNodeUndefined__Decorators(TemplateTagSidebarMenuBaseTestCase):
    """Tests the logic for when a node does not have permissions defined,
    so logic has to fall back to values defined on a function-based (aka decorator) view.
    """

    FULL_VIEW_WHITELIST = [
        "adminlte2_pdq:demo-css",
        "adminlte2_pdq_tests:function-allow-anonymous-access",
        "adminlte2_pdq_tests:function-login-required",
        "adminlte2_pdq_tests:function-allow-without-permissions",
        "adminlte2_pdq_tests:function-one-permission-required",
        "adminlte2_pdq_tests:function-one-permission-required-as-string",
        "adminlte2_pdq_tests:function-full-permissions-required",
        "adminlte2_pdq_tests:function-full-permissions-required-as-string",
    ]

    # region Loose Mode

    def test__loose_mode__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Loose Mode

    # region LoginRequired Mode, No Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion LoginRequired Mode, No Whitelist

    # region LoginRequired Mode, Login Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

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
    def test__strict_mode__no_whitelists__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

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
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Login Whitelist

    # region Strict Mode, Permission Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

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
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_no_decorator(self):
        """Tests for a view with no decorator defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_anonymous_access_decorator(self):
        """Tests for a view with a AllowAnonymous decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_login_required_decorator(self):
        """Tests for a node deferring to a view with a LoginRequired decorator."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_allow_without_permissions_decorator(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_one_permission_required_decorator(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_one_permission_required_decorator_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_permission_required_decorator(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_permission_required_decorator__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired decorator."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:function-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Both Whitelists


class TemplateTagSidebarMenu__ViewFallbackWhenNodeUndefined__Classes(TemplateTagSidebarMenuBaseTestCase):
    """Tests the logic for when a node does not have permissions defined,
    so logic has to fall back to values defined on a class-based (aka mixin) view.
    """

    FULL_VIEW_WHITELIST = [
        "adminlte2_pdq:demo-css",
        "adminlte2_pdq_tests:class-allow-anonymous-access",
        "adminlte2_pdq_tests:class-login-required",
        "adminlte2_pdq_tests:class-allow-without-permissions",
        "adminlte2_pdq_tests:class-one-permission-required",
        "adminlte2_pdq_tests:class-one-permission-required-as-string",
        "adminlte2_pdq_tests:class-full-permissions-required",
        "adminlte2_pdq_tests:class-full-permissions-required-as-string",
    ]

    # region Loose Mode

    def test__loose_mode__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__loose_mode__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Loose Mode

    # region LoginRequired Mode, No Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required_mode__no_whitelists__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion LoginRequired Mode, No Whitelist

    # region LoginRequired Mode, Login Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__login_required_mode__with_login_whitelist__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

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
    def test__strict_mode__no_whitelists__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict_mode__no_whitelists__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

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
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_login_whitelist__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Login Whitelist

    # region Strict Mode, Permission Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__with_permission_whitelist__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

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
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_no_mixin(self):
        """Tests for a view with no mixin defined."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_anonymous_access_mixin(self):
        """Tests for a view with a AllowAnonymous mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-anonymous-access",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_login_required_mixin(self):
        """Tests for a node deferring to a view with a LoginRequired mixin."""

        # Note: LoginRequired is not valid for STRICT mode.
        # Behavior is currently undefined, so here we verify behavior is more strict rather than less.

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-login-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_allow_without_permissions_mixin(self):
        """Tests for a node deferring to a view with a AllowWithoutPermission mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-allow-without-permissions",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_one_permission_required_mixin(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_one_permission_required_mixin_as_string(self):
        """Tests for a node deferring to a view with a OnePermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-one-permission-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_permission_required_mixin(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

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

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar", "change_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", FULL_VIEW_WHITELIST)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", FULL_VIEW_WHITELIST)
    def test__strict_mode__both_whitelists__view_with_permission_required_mixin__as_str(self):
        """Tests for a node deferring to a view with a PermissionRequired mixin."""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq_tests:class-full-permissions-required-as-string",
            "text": "Test Node",
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

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permission groups"):
            # Get user to run subtest on.
            self._setup_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with wrong permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["view_foo", "delete_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(permissions=["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with wrong permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["view_bar", "delete_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permission groups"):
            # Get user to run subtest on.
            self._setup_staff_user(groups=["add_bar"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Both Whitelists
