"""
Tests for Constants
"""

# Third-Party Imports.
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

# First-Party Imports
from adminlte2_pdq.constants.route_and_policy_constants import get_strict_policy, get_login_required_policy


class ConfigurationMiddlewareTestCase(TestCase):
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

    @override_settings(ADMINLTE2_USE_STRICT_POLICY=False, ADMINLTE2_STRICT_POLICY_WHITELIST=["foobar"])
    def test_improperly_configured_error_is_raised_when_strict_whitelist_set_and_not_in_strict_mode(self):
        """Test that an ImproperlyConfigured error is raised when there is a setting for the strict
        whitelist and the strict policy is set to False."""

        with self.assertRaises(ImproperlyConfigured) as cm:
            # pylint:disable=unused-import
            # from adminlte2_pdq.constants import LOGIN_REQUIRED, STRICT_POLICY
            get_strict_policy()

        error_message = "Can't use ADMINLTE2_STRICT_POLICY_WHITELIST outside of STRICT_POLICY = True."
        self.assertEqual(str(cm.exception), error_message)

    @override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=False, ADMINLTE2_LOGIN_EXEMPT_WHITELIST=["foobar"])
    def test_improperly_configured_error_is_raised_when_login_whitelist_set_and_not_in_login_required_mode(self):
        """Test that an ImproperlyConfigured error is raised when there is a setting for the login
        whitelist and the login required policy is set to False."""

        with self.assertRaises(ImproperlyConfigured) as cm:
            # pylint:disable=unused-import
            # from adminlte2_pdq.constants import LOGIN_REQUIRED, STRICT_POLICY
            get_login_required_policy(False)

        error_message = "Can't use ADMINLTE2_LOGIN_EXEMPT_WHITELIST outside of LOGIN_REQUIRED = True."
        self.assertEqual(str(cm.exception), error_message)
