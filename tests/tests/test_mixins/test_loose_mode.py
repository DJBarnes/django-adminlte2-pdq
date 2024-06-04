"""
Tests for Mixin login in project "loose" authentication mode.
"""

# System Imports.
import warnings

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings

# Internal Imports.
from .base_test_case import BaseMixinTextCase


# Module Variables.
UserModel = get_user_model()


@override_settings(DEBUG=True)
class TestLooseAuthenticationMixins(BaseMixinTextCase):
    """
    Test project authentication mixins, under project "Loose" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertFalse(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from constants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        # Test for expected setting values.
        self.assertFalse(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Loose" mode. For sanity checking."""

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.inactive_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.none_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.none_staff_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_staff_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_staff_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.super_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As an inactive user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.inactive_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As staff user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.none_staff_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As staff user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_perm_staff_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As staff user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_perm_staff_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As a superuser"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.super_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.inactive_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.none_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.none_staff_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.partial_perm_staff_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.full_perm_staff_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.super_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As an inactive user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.inactive_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As staff user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_staff_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As staff user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_staff_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As staff user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_staff_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As a superuser"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.super_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.inactive_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_staff_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

            # with self.subTest('As user with one permission'):
            #     # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_staff_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_perm_staff_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.super_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.inactive_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_staff_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_staff_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_perm_staff_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.super_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )


@override_settings(DEBUG=True)
class TestLooseAuthenticationMixinOverlap(BaseMixinTextCase):
    """Tests to make sure mixin logic doesn't bleed into each other.

    By "bleeding", we refer to instances when the user overlaps values for one
    Mixin with another. Or forgets expected values of a Mixin. Or combinations thereof.

    For example, a LoginRequired Mixin should always behave the same as the login_required
    decorator, even if the user accidentally defines permissions on the view as well.

    Due to how Mixins and our project middleware works, these are not as cleanly separated
    as they are with the decorators, and so additional tests are required.

    NOTE: I'm not sure if it's possible to get updated values for response attributes?
          Seems to only return the values defined at literal class value.
          So sometimes the passed attributes seem "wrong" but as long as the actual view
          directs as expected, then it's probably fine? Not sure if there's a better way...
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertFalse(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from constants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        # Test for expected setting values.
        self.assertFalse(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__bleeding_anonymous_with_permissions(self):
        """Bleeding tests for allow_anonymous_access mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

    def test__bleeding_login_with_permissions(self):
        """Bleeding tests for login_required mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.none_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full permissions"):
            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full groups"):
            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

    def test__bleeding_conflicting_permissions(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

    def test__bleeding_one_permission_missing_permissions(self):
        """Bleeding tests for permission_required_one mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.anonymous_user,
                    expected_status=200,
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.none_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.partial_perm_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.full_perm_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.incorrect_group_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.partial_group_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.full_group_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__bleeding_full_permission_missing_permissions(self):
        """Bleeding tests for permission_required_one mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.anonymous_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.none_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.partial_perm_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.full_perm_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.incorrect_group_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page..
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.partial_group_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.full_group_user,
                    expected_status=200,
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))
