"""
Tests for Constants
"""

# Third-Party Imports.
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

# First-Party Imports
from adminlte2_pdq.constants.route_and_policy_constants import (
    LOGIN_EXEMPT_WHITELIST,
    STRICT_POLICY_WHITELIST,
    get_login_required_policy,
    get_renamed_setting,
    get_strict_policy,
)


class PolicyConstantsTestCase(TestCase):
    """Test that settings / constants in the project is set up correctly to use PDQ
    NOTE: Even though we are testing methods that get the LOGIN_REQUIRED and STRICT_POLICY values
    and not the constants directly, the associated constants should have the same value because in
    the constants module are calls to these methods to set LOGIN_REQUIRED and STRICT_POLICY.
    We can't test the constants directly very easily due to them being figured out when testing
    starts up. We also can't mock because it would mean mocking the thing that we are trying to test
    which would result in tests that are verifying that mocking works correctly. Not that the logic
    associated with the mock works as intended. Thus we have functions to do all of the logic.
    Because we can easily test those.
    """

    # pylint:disable=import-outside-toplevel

    @override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=False, ADMINLTE2_USE_STRICT_POLICY=False)
    def test_login_required_and_strict_policy_constant_false_when_setting_false(self):
        """Test that the LOGIN_REQUIRED and STRICT_POLICY constant is set correctly from settings.py"""

        # from adminlte2_pdq.constants import LOGIN_REQUIRED, STRICT_POLICY

        self.assertFalse(get_strict_policy())
        self.assertFalse(get_login_required_policy(False))

    @override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True, ADMINLTE2_USE_STRICT_POLICY=False)
    def test_login_required_constant_true_when_setting_true(self):
        """Test that the LOGIN_REQUIRED constant is set correctly from settings.py"""

        # from adminlte2_pdq.constants import LOGIN_REQUIRED, STRICT_POLICY

        self.assertFalse(get_strict_policy())
        self.assertTrue(get_login_required_policy(False))

    @override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True, ADMINLTE2_USE_STRICT_POLICY=True)
    def test_strict_constant_true_when_setting_true(self):
        """Test that the STRICT_POLICY constant is set correctly from settings.py"""

        # from adminlte2_pdq.constants import LOGIN_REQUIRED, STRICT_POLICY

        self.assertTrue(get_strict_policy())
        self.assertTrue(get_login_required_policy(True))

    @override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=False, ADMINLTE2_USE_STRICT_POLICY=True)
    def test_setting_login_required_setting_to_false_has_no_effect_when_strict_setting_true(self):
        """Test that the LOGIN_REQUIRED constant remains True despite trying to set it to False when
        STRICT_POLICY setting / constant has been set to True settings.py"""

        # from adminlte2_pdq.constants import LOGIN_REQUIRED, STRICT_POLICY

        self.assertTrue(get_strict_policy())
        self.assertTrue(get_login_required_policy(True))

    def test_improperly_configured_error_is_raised_when_strict_whitelist_set_and_not_in_strict_mode(self):
        """The exact and fuzzy permission whitelists raise ImproperlyConfigured outside of strict mode."""
        for whitelist in ("ADMINLTE2_STRICT_POLICY_WHITELIST", "ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST"):
            with self.subTest(whitelist=whitelist):
                with override_settings(ADMINLTE2_USE_STRICT_POLICY=False, **{whitelist: ["/foobar/"]}):
                    with self.assertRaises(ImproperlyConfigured) as cm:
                        get_strict_policy()

                self.assertEqual(f"Can't use {whitelist} outside of STRICT_POLICY = True.", str(cm.exception))

    def test_improperly_configured_error_is_raised_when_login_whitelist_set_and_not_in_login_required_mode(self):
        """The exact and fuzzy login whitelists raise ImproperlyConfigured outside of login-required mode."""
        for whitelist in ("ADMINLTE2_LOGIN_EXEMPT_WHITELIST", "ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST"):
            with self.subTest(whitelist=whitelist):
                with override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=False, **{whitelist: ["/foobar/"]}):
                    with self.assertRaises(ImproperlyConfigured) as cm:
                        get_login_required_policy(False)

                self.assertEqual(f"Can't use {whitelist} outside of LOGIN_REQUIRED = True.", str(cm.exception))

    def test_whitelists_are_allowed_in_their_mode(self):
        """Each whitelist can be set in its own mode, and an empty whitelist in any mode."""
        cases = {
            "permission whitelists in strict mode": (
                {"ADMINLTE2_USE_STRICT_POLICY": True},
                {"ADMINLTE2_STRICT_POLICY_WHITELIST": ["/a/"], "ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST": ["/b/"]},
            ),
            "login whitelists in login-required mode": (
                {"ADMINLTE2_USE_LOGIN_REQUIRED": True},
                {"ADMINLTE2_LOGIN_EXEMPT_WHITELIST": ["/a/"], "ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST": ["/b/"]},
            ),
            "login whitelists in strict mode": (
                {"ADMINLTE2_USE_STRICT_POLICY": True},
                {"ADMINLTE2_LOGIN_EXEMPT_WHITELIST": ["/a/"], "ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST": ["/b/"]},
            ),
            "empty whitelists in loose mode": (
                {},
                {
                    "ADMINLTE2_STRICT_POLICY_WHITELIST": (),
                    "ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST": [],
                    "ADMINLTE2_LOGIN_EXEMPT_WHITELIST": (),
                    "ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST": [],
                },
            ),
        }
        for name, (policy, whitelists) in cases.items():
            with self.subTest(setup=name):
                with override_settings(**policy, **whitelists):
                    get_login_required_policy(get_strict_policy())


class RenamedSettingTestCase(TestCase):
    """Tests for settings that were renamed to have the ADMINLTE2_ prefix."""

    @override_settings(ADMINLTE2_NEW_NAME="new")
    def test__new_name(self):
        """The new name is used."""
        self.assertEqual("new", get_renamed_setting("ADMINLTE2_NEW_NAME", "OLD_NAME", "default"))

    @override_settings(OLD_NAME="old")
    def test__old_name_warns(self):
        """The old name still works, with a deprecation warning that names the new setting."""
        with self.assertWarns(DeprecationWarning) as warning:
            self.assertEqual("old", get_renamed_setting("ADMINLTE2_NEW_NAME", "OLD_NAME", "default"))
        self.assertIn("ADMINLTE2_NEW_NAME", str(warning.warning))

    @override_settings(ADMINLTE2_NEW_NAME="new", OLD_NAME="old")
    def test__new_name_wins(self):
        """When both are set, the new name is used."""
        self.assertEqual("new", get_renamed_setting("ADMINLTE2_NEW_NAME", "OLD_NAME", "default"))

    def test__default(self):
        """With neither set, the default is used."""
        self.assertEqual("default", get_renamed_setting("ADMINLTE2_NEW_NAME", "OLD_NAME", "default"))


class DefaultWhitelistsTestCase(TestCase):
    """The whitelists hold the package's own routes when the project adds none (as in the test project)."""

    def test__login_exempt_whitelist(self):
        """The login, logout, password reset, and register routes don't require login."""
        self.assertEqual(
            [
                "/accounts/login/",
                "/accounts/logout/",
                "password_reset",
                "password_reset_done",
                "password_reset_confirm",
                "password_reset_complete",
                "adminlte2_pdq:register",
            ],
            [str(route) for route in LOGIN_EXEMPT_WHITELIST],
        )

    def test__strict_policy_whitelist(self):
        """The home and password change routes, and every login-exempt route, don't require permissions."""
        self.assertEqual(
            ["adminlte2_pdq:home", "password_change", "password_change_done"]
            + [str(route) for route in LOGIN_EXEMPT_WHITELIST],
            [str(route) for route in STRICT_POLICY_WHITELIST],
        )
