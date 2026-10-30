"""
View access in login-required mode (ADMINLTE2_USE_LOGIN_REQUIRED).

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
LOGIN_REQUIRED_MODE = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required":            (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "one_permission_required (string)":   (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "full_permissions_required":          (L, L,   H, H, H, Y, H, H, Y,   H, H, H, Y, H, H, Y,   Y),
    "full_permissions_required (string)": (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
}

LOGIN_REQUIRED_MODE__LOGIN_WHITELIST = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required":            (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "one_permission_required (string)":   (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
    "full_permissions_required":          (L, L,   H, H, H, Y, H, H, Y,   H, H, H, Y, H, H, Y,   Y),
    "full_permissions_required (string)": (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
}

LOGIN_REQUIRED_MODE__PERMISSION_WHITELIST = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (L, L,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required":            (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required (string)":   (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required (string)": (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
}

LOGIN_REQUIRED_MODE__BOTH_WHITELISTS = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "allow_anonymous_access":             (Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y, Y, Y, Y, Y, Y, Y,   Y),
    "login_required":                     (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "allow_without_permissions":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required":            (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "one_permission_required (string)":   (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required":          (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
    "full_permissions_required (string)": (E, E,   E, E, E, E, E, E, E,   E, E, E, E, E, E, E,   E),
}
# fmt: on


@override_settings(DEBUG=True)
class LoginRequiredModeAccessTestCase(AccessTestCase):
    """View access in login-required mode."""

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test__login_required_mode(self):
        """Login-required mode, no whitelists."""
        self.assert_access(
            LOGIN_REQUIRED_MODE,
            errors={
                "login_required": "login_required_mode__login_required_not_supported",
                "allow_without_permissions": "login_required_mode__allow_without_permissions_not_supported",
            },
        )

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test__login_required_mode__login_whitelist(self):
        """Login-required mode, every view in the login whitelist."""
        self.assert_access(
            LOGIN_REQUIRED_MODE__LOGIN_WHITELIST,
            whitelists=["login"],
            notices={
                "allow_anonymous_access": [Notice("allow_anonymous_access_and_login_whitelist")],
                "one_permission_required": [Notice("ineffective_login_whitelist")],
                "one_permission_required (string)": [Notice("ineffective_login_whitelist")],
                "full_permissions_required": [Notice("ineffective_login_whitelist")],
                "full_permissions_required (string)": [Notice("ineffective_login_whitelist")],
            },
            errors={
                "login_required": "login_required_mode__login_required_not_supported",
                "allow_without_permissions": "login_required_mode__allow_without_permissions_not_supported",
            },
        )

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test__login_required_mode__permission_whitelist(self):
        """Login-required mode, every view in the fuzzy permission whitelist. The exact permission whitelist can't be
        set outside strict mode (the settings check rejects it), but the fuzzy one can."""
        self.assert_access(
            LOGIN_REQUIRED_MODE__PERMISSION_WHITELIST,
            whitelists=["permission"],
            forms=["fuzzy"],
            errors={
                "login_required": "login_required_mode__login_required_not_supported",
                "allow_without_permissions": "login_required_mode__allow_without_permissions_not_supported",
                "one_permission_required": "permissions_and_permission_whitelist",
                "one_permission_required (string)": "permissions_and_permission_whitelist",
                "full_permissions_required": "permissions_and_permission_whitelist",
                "full_permissions_required (string)": "permissions_and_permission_whitelist",
            },
        )

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test__login_required_mode__both_whitelists(self):
        """Login-required mode, every view in the login whitelist and the fuzzy permission whitelist."""
        self.assert_access(
            LOGIN_REQUIRED_MODE__BOTH_WHITELISTS,
            whitelists=["login", "permission"],
            forms=["fuzzy"],
            notices={
                "allow_anonymous_access": [Notice("allow_anonymous_access_and_login_whitelist")],
            },
            errors={
                "login_required": "login_required_mode__login_required_not_supported",
                "allow_without_permissions": "login_required_mode__allow_without_permissions_not_supported",
                "one_permission_required": "permissions_and_permission_whitelist",
                "one_permission_required (string)": "permissions_and_permission_whitelist",
                "full_permissions_required": "permissions_and_permission_whitelist",
                "full_permissions_required (string)": "permissions_and_permission_whitelist",
            },
        )
