"""
View access in loose mode (the default).

See base_test_case.py for the views, the users, and how each cell is checked.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.test import override_settings

# Internal Imports.
from .base_test_case import AccessTestCase, E, H, L, VIEW_TYPES, Y


# Module Variables.

# Cells:
#   Y = page loads
#   L = redirect to login
#   H = redirect home with the "permission requirements were not met" message
#   E = ImproperlyConfigured
#
# Columns (the "user" and "staff" groups each have the no to fg columns):
#   an = anonymous
#   in = inactive user (can't log in)
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
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "login_required":                     (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_without_permissions":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required":            (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "one_permission_required (string)":   (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "full_permissions_required":          (L, L,   H, H, H, Y, H, H, Y,   H, H, H, Y, H, H, Y,   Y),
    "full_permissions_required (string)": (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
}
# fmt: on


@override_settings(DEBUG=True)
class LooseModeAccessTestCase(AccessTestCase):
    """View access in loose mode."""

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", False)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", False)
    def test__loose_mode(self):
        """Loose mode."""
        self.assert_access(
            LOOSE_MODE,
            errors={
                "allow_anonymous_access": "loose_mode__allow_anonymous_access_not_supported",
                "allow_without_permissions": "loose_mode__allow_without_permissions_not_supported",
            },
        )

    def test__project_settings_are_loose(self):
        """The test project runs in loose mode, so the loose mode tests don't depend on their patches."""
        # pylint: disable=import-outside-toplevel
        from django.conf import settings

        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_STRICT_POLICY", False))
        self.assertEqual([], getattr(settings, "ADMINLTE2_LOGIN_EXEMPT_WHITELIST", []))
        self.assertEqual([], getattr(settings, "ADMINLTE2_STRICT_POLICY_WHITELIST", []))

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", False)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", False)
    @patch(
        "adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST",
        ["adminlte2_pdq_tests:function-login-required", "adminlte2_pdq_tests:class-login-required"],
    )
    def test__loose_mode__login_required_view_in_login_whitelist(self):
        """A login_required view can't also be in the login whitelist."""
        for view_type in VIEW_TYPES:
            for user_name, user in self._create_table_users().items():
                with self.subTest(view=f"{view_type} view, login_required", user=user_name):
                    self.assert_outcome(view_type, "login_required", user, E, [], "login_required_and_login_whitelist")
