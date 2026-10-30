"""
View access in strict mode (ADMINLTE2_USE_STRICT_POLICY).

See base_test_case.py for the views, the users, and how each cell is checked.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.test import override_settings

# Internal Imports.
from .base_test_case import AccessTestCase, E, H, L, Notice, Y


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
STRICT_MODE = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (L, L,   H, H, H, H, H, H, H,   H, H, H, H, H, H, H,   H),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":            (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "one_permission_required (string)":   (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "full_permissions_required":          (L, L,   H, H, H, Y, H, H, Y,   H, H, H, Y, H, H, Y,   Y),
    "full_permissions_required (string)": (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
}

STRICT_MODE__LOGIN_WHITELIST = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (L, L,   H, H, H, H, H, H, H,   H, H, H, H, H, H, H,   H),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":            (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "one_permission_required (string)":   (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "full_permissions_required":          (L, L,   H, H, H, Y, H, H, Y,   H, H, H, Y, H, H, Y,   Y),
    "full_permissions_required (string)": (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
}

STRICT_MODE__PERMISSION_WHITELIST = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":            (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required (string)":   (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required (string)": (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
}

STRICT_MODE__BOTH_WHITELISTS = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "one_permission_required":            (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required (string)":   (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required (string)": (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
}
# fmt: on


@override_settings(DEBUG=True)
class StrictModeAccessTestCase(AccessTestCase):
    """View access in strict mode."""

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict_mode(self):
        """Strict mode, no whitelists."""
        self.assert_access(
            STRICT_MODE,
            notices={
                "none": [
                    Notice("strict_mode__no_decorators", "function", logged_in_only=True),
                    Notice("missing_permissions", "class"),
                ],
            },
            errors={
                "login_required": "strict_mode__login_required_not_supported",
            },
        )

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict_mode__login_whitelist(self):
        """Strict mode, every view in the login whitelist."""
        self.assert_access(
            STRICT_MODE__LOGIN_WHITELIST,
            whitelists=["login"],
            notices={
                "none": [
                    Notice("ineffective_login_whitelist"),
                    Notice("strict_mode__no_decorators", "function"),
                    Notice("missing_permissions", "class"),
                ],
                "allow_anonymous_access": [
                    Notice("allow_anonymous_access_and_login_whitelist"),
                    Notice("ineffective_login_whitelist"),
                ],
                "one_permission_required": [Notice("ineffective_login_whitelist")],
                "one_permission_required (string)": [Notice("ineffective_login_whitelist")],
                "full_permissions_required": [Notice("ineffective_login_whitelist")],
                "full_permissions_required (string)": [Notice("ineffective_login_whitelist")],
            },
            errors={
                "login_required": "strict_mode__login_required_not_supported",
            },
        )

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict_mode__permission_whitelist(self):
        """Strict mode, every view in the permission whitelist."""
        self.assert_access(
            STRICT_MODE__PERMISSION_WHITELIST,
            whitelists=["permission"],
            notices={
                "allow_without_permissions": [Notice("allow_without_permissions_and_permission_whitelist")],
            },
            errors={
                "login_required": "strict_mode__login_required_not_supported",
                "one_permission_required": "permissions_and_permission_whitelist",
                "one_permission_required (string)": "permissions_and_permission_whitelist",
                "full_permissions_required": "permissions_and_permission_whitelist",
                "full_permissions_required (string)": "permissions_and_permission_whitelist",
            },
        )

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict_mode__both_whitelists(self):
        """Strict mode, every view in both whitelists."""
        self.assert_access(
            STRICT_MODE__BOTH_WHITELISTS,
            whitelists=["login", "permission"],
            notices={
                "allow_anonymous_access": [Notice("allow_anonymous_access_and_login_whitelist")],
                "allow_without_permissions": [Notice("allow_without_permissions_and_permission_whitelist")],
            },
            errors={
                "login_required": "strict_mode__login_required_not_supported",
                "one_permission_required": "permissions_and_permission_whitelist",
                "one_permission_required (string)": "permissions_and_permission_whitelist",
                "full_permissions_required": "permissions_and_permission_whitelist",
                "full_permissions_required (string)": "permissions_and_permission_whitelist",
            },
        )
