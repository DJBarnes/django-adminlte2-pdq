"""
Tests for Mixin login in project "login required" authentication mode.
"""

# System Imports.
import warnings
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import override_settings

# Internal Imports.
from .base_test_case import BaseMixinTextCase, LOGIN_WHITELIST_VIEWS


# Module Variables.
UserModel = get_user_model()


class LoginModeMixin:
    """Test project authentication mixins, under project "Login Required" mode.

    This class is a parent class that should not run by itself.
    It needs to be imported into other classes to execute.
    """

    def test__no_mixins(self):
        """Test for view with no mixins, in project "LOGIN REQUIRED" mode.
        Everything should act like "login required" mixin by default.
        """

        with self.subTest("As anonymous user"):
            # Should redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.anonymous_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.inactive_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.super_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Login Required" mode."""

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.anonymous_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As an inactive user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.inactive_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.full_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.super_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Login Required" mode.
        In Login Required mode, this mixin should NOT work, and instead raise errors.
        """

        with self.subTest("As anonymous user"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As an inactive user"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.inactive_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As staff user with no permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As staff user with one permission"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As staff user with full permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

        with self.subTest("As a superuser"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Login Required" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As an inactive user"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.inactive_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As staff user with no permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As staff user with one permission"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As staff user with full permissions"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As a superuser"):
            # Invalid mixin used for Login Required mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_login__allow_without_permissions_mixin_message, str(err.exception))

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Login Required" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.anonymous_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.inactive_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.super_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
        """Test for permission_required mixin, in project "Login Required" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.anonymous_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.inactive_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As staff user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
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

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.super_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class TestLoginRequiredAuthenticationMixins(BaseMixinTextCase, LoginModeMixin):
    """Runtime test execution of mixins under "Login Required" mode."""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
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

        self.assertTrue(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_LOGIN_EXEMPT_WHITELIST=LOGIN_WHITELIST_VIEWS)
@override_settings(LOGIN_EXEMPT_WHITELIST=LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
class TestLoginRequiredAuthenticationMixinsWithLoginWhitelist(BaseMixinTextCase, LoginModeMixin):
    """Runtime test execution of mixins under "Login Required" mode, with whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    In this case, the login_required and allow_without_permission mixins don't make sense,
    and aren't allowed in this mode.

    Modified States are:
    * "no_decorator" - The "anonymous" and "inactive" users can now access the page.
    * "allow_anonymous_access" - Raises a "whitelist overlap" warning.
    * "one_of_perms"/"full_perms" - Raises an "ineffective whitelist" warning.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertFalse(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(13, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from constants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(13, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixins, in project "LOGIN REQUIRED" mode, with login whitelist.

        The "anonymous" and "inactive" users can now access the page.
        """

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.anonymous_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.inactive_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
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
                # View setup.
                "adminlte2_pdq_tests:class-standard",
                user=self.super_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Login Required" mode, with login whitelist.

        Raises a "whitelist overlap" warning.
        """

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As an inactive user"):
            # Shouldn't really be possible.
            # But testing anyway since package does a lot of background magic with auth logic.
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.inactive_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-1].message))

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Login Required" mode, with login whitelist.

        Raises an "ineffective whitelist" warning.
        """

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.inactive_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="One Permission Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | One Permission Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__one_of_perms,
                str(warning[-1].message),
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
        """Test for permission_required mixin, in project "Login Required" mode, with login whitelist.

        Raises an "ineffective whitelist" warning.
        """

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.inactive_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
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
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
            )

            # Verify we get the expected warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(
                self.pdq_strict__ineffective_login_whitelist_message__full_perms,
                str(warning[-1].message),
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
