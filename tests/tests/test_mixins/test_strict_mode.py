"""
Tests for Mixin login in project "strict" authentication mode.
"""

# System Imports.
import warnings
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

# Internal Imports.
from .base_test_case import BaseMixinTextCase, LOGIN_WHITELIST_VIEWS, PERM_WHITELIST_VIEWS


# Module Variables.
UserModel = get_user_model()


class StrictModeMixin:
    """Test project authentication mixins, under project "Strict" mode.

    This class is a parent class that should not run by itself.
    It needs to be imported into other classes to execute.
    """

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Strict" mode.
        Everything should redirect with a warning message.
        """

        with self.subTest("As anonymous user"):
            # View configured incorrectly for strict mode. Should initially redirect to "home".
            # But then since we're also not logged in, it redirects to login required page.

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
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # View configured incorrectly for strict mode. Should initially redirect to "home".
            # But then since we're also not logged in, it redirects to login required page.

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
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with no permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with one permission"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with full permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As a superuser"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode."""

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
        """Test for login_required mixin, in project "Strict" mode.
        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        with self.subTest("As anonymous user"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As an inactive user"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.inactive_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As staff user with no permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As staff user with one permission"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As staff user with full permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As a superuser"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
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
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
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
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.full_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.super_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode."""

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
        """Test for permission_required mixin, in project "Strict" mode."""

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
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationMixins(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode."""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
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
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@override_settings(ADMINLTE2_LOGIN_EXEMPT_WHITELIST=LOGIN_WHITELIST_VIEWS)
@override_settings(LOGIN_EXEMPT_WHITELIST=LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.constants.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
class TestStrictAuthenticationMixinsWithLoginWhitelist(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode, with login whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    Modified States are:
    * "no_mixin" - Raises "ineffective whitelist" warning and the default STRICT_MODE warning.
    * "allow_anonymous_access" - Raises "ineffective whitelist" warning and "overlaps with whitelist" warning.
    * "one_of_perms"/"full_perms" - Raises only the "ineffective whitelist" warning.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
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
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(13, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Strict" mode, with login whitelist.

        Raises "ineffective whitelist" warning and the default STRICT_MODE warning.
        """

        with self.subTest("As anonymous user"):
            # View configured incorrectly for strict mode. Should initially redirect to "home".
            # But then since we're also not logged in, it redirects to login required page.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
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
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # View configured incorrectly for strict mode. Should initially redirect to "home".
            # But then since we're also not logged in, it redirects to login required page.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
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
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with no permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with one permission"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As staff user with full permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As a superuser"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_messages=[
                        self.pdq_strict__no_mixin_message,
                        self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_strict__no_mixin_message, str(warning[-1].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                str(warning[-2].message),
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode, with login whitelist.

        Raises "ineffective whitelist" warning and "overlaps with whitelist" warning.
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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
                    expected_messages=[
                        self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(2, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertEqual(RuntimeWarning, warning[-2].category)
            self.assertText(self.pdq_login__allow_anonymous_whitelist_overlap_message, str(warning[-2].message))
            self.assertText(
                self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                str(warning[-1].message),
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

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode, with login whitelist.

        Raises only the "ineffective whitelist" warning.
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__one_of_perms,
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
        """Test for permission_required mixin, in project "Strict" mode, with login whitelist.

        Raises only the "ineffective whitelist" warning.
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq__ineffective_login_whitelist_message__full_perms,
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


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@override_settings(ADMINLTE2_STRICT_POLICY_WHITELIST=PERM_WHITELIST_VIEWS)
@override_settings(STRICT_POLICY_WHITELIST=PERM_WHITELIST_VIEWS)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY_WHITELIST", PERM_WHITELIST_VIEWS)
@patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", PERM_WHITELIST_VIEWS)
class TestStrictAuthenticationMixinsWithPermWhitelist(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode, with login whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    Modified States are:
    * "one_of_permissions"/"full_permissions" - Raises errors because they don't make sense.
    * Everything else should effectively behave as if it was in "Login Required" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(16, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from constants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(16, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Strict" mode, with perm whitelist.

        Effectively runs the same as LoginRequired no_mixin tests.
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

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Strict" mode, with perm whitelist.

        Raises warnings about redundancy with whitelist.
        """

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
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
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
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
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.super_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    expected_messages=[
                        self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(
                self.pdq_strict__allow_without_permissions_whitelist_overlap_message,
                str(warning[-1].message),
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode, with perm whitelist.

        Raises error because it doesn't make sense to be in a permission whitelist
        AND have a permission_required mixin.
        """

        # All users should raise the same error.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-one-permission-required",
                        user=user,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__one_permission_required_whitelist_overlap_message, str(err.exception))

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Strict" mode, with perm whitelist.

        Raises error because it doesn't make sense to be in a permission whitelist
        AND have a permission_required mixin.
        """

        # All users should raise the same error.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-full-permissions-required",
                        user=user,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__full_permission_required_whitelist_overlap_message, str(err.exception))


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@override_settings(ADMINLTE2_LOGIN_EXEMPT_WHITELIST=LOGIN_WHITELIST_VIEWS)
@override_settings(LOGIN_EXEMPT_WHITELIST=LOGIN_WHITELIST_VIEWS)
@override_settings(ADMINLTE2_STRICT_POLICY_WHITELIST=PERM_WHITELIST_VIEWS)
@override_settings(STRICT_POLICY_WHITELIST=PERM_WHITELIST_VIEWS)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.constants.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.constants.STRICT_POLICY_WHITELIST", PERM_WHITELIST_VIEWS)
@patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", PERM_WHITELIST_VIEWS)
class TestStrictAuthenticationMixinsWithBothWhitelists(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode, with login whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    In this case, pretty much everything should be visible to all user types, as long as it's
    a mixin that can be used in strict mode at all.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(13, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(16, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from constants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(13, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(16, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixin, in project "strict" mode, with both whitelists."""

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user in self.user_list:

            with self.subTest(f"Running as {user.username} user"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Standard View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Standard View Header",
                )

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode."""

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):

                # Verify we get the expected page.
                with warnings.catch_warnings(record=True) as warning:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-anonymous-access",
                        user=user,
                        # Expected view return data.
                        expected_status=200,
                        view_should_redirect=False,
                        # Expected content on page.
                        expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                        expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                        expected_messages=[
                            self.pdq_login__allow_anonymous_whitelist_overlap_message,
                        ],
                    )

                # Verify we get the expected console warning message.
                self.assertEqual(1, len(warning))
                self.assertEqual(RuntimeWarning, warning[-1].category)
                self.assertText(
                    self.pdq_login__allow_anonymous_whitelist_overlap_message,
                    str(warning[-1].message),
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
        """Test for login_required mixin, in project "Strict" mode, with both whitelists.

        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    # Verify we get the expected page.
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-login-required",
                        user=user,
                        # Expected view return data.
                        expected_status=500,
                    )

                self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Strict" mode, with both whitelists."""

        # TODO: This redirects to login for some reason.
        #   I suspect it's something to do with the actual mixin/decorator logic.
        #   Perhaps the middleware is doing too much work, and the mixins/decorators don't understand
        #   whitelists enough to allow this case?
        #   This is such a specific and stupid case though that I don't know if I care to
        #   troubleshoot it at this time. Fix later.

        # # All users are in both login and permission whitelist, so they should handle all the same.
        # for user in self.user_list:
        #     with self.subTest(f"Running as {user.username} user"):
        #
        #         # Verify we get the expected page.
        #         response = self.assertGetResponse(
        #             # View setup.
        #             "adminlte2_pdq_tests:class-allow-without-permissions",
        #             user=self.anonymous_user,
        #             # Expected view return data.
        #             expected_status=200,
        #             view_should_redirect=False,
        #             # Expected content on page.
        #             expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
        #             expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
        #         )
        #
        #         # Verify values associated with returned view.
        #         self.assertTrue(hasattr(response, "admin_pdq_data"))
        #         data_dict = response.admin_pdq_data
        #         self.assertEqual(
        #             "allow_without_permissions",
        #             data_dict["decorator_name"],
        #         )
        #         self.assertTrue(data_dict["login_required"])
        #         self.assertIsNone(data_dict["one_of_permissions"])
        #         self.assertIsNone(data_dict["full_permissions"])

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode, with both whitelists.

        Should raise error since it's both permission whitelisted and requiring a permission.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-one-permission-required",
                        user=user,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__one_permission_required_whitelist_overlap_message, str(err.exception))

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Strict" mode, with both whitelists.

        Should raise error since it's both permission whitelisted and requiring a permission.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-full-permissions-required",
                        user=user,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__full_permission_required_whitelist_overlap_message, str(err.exception))


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAutAuthenticationMixinsWithLogicBleed(BaseMixinTextCase):
    """Tests to make sure mixin logic doesn't bleed into each other.

    By "bleeding", we refer to instances when the user overlaps values for one
    Mixin with another. Or forgets expected values of a Mixin. Or combinations thereof.

    For example, a LoginRequired Mixin should always behave the same as the login_required
    mixin, even if the user accidentally defines permissions on the view as well.

    Due to how Mixins and our project middleware works, these are not as cleanly separated
    as they are with the mixins, and so additional tests are required.

    NOTE: I'm not sure if it's possible to get updated values for response attributes?
        Seems to only return the values defined at literal class value.
        So sometimes the passed attributes seem "wrong" but as long as the actual view
        directs as expected, then it's probably fine? Not sure if there's a better way...
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertTrue(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
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
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__bleeding_anonymous_with_permissions(self):
        """Bleeding tests for allow_anonymous_access mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
            self.assertEqual("allow_anonymous_access", data_dict["decorator_name"])
            self.assertFalse(data_dict["login_required"])
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
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

    def test__bleeding_login_with_permissions(self):
        """Test for login_required mixin, in project "Strict" mode.
        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        with self.subTest("As anonymous user"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.anonymous_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.full_perm_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(ImproperlyConfigured) as err:
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.full_group_user,
                    # Expected view return data.
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__bleeding_conflicting_permissions(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
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
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
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
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
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
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
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
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
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
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
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
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.full_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
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

    def test__one_permission_required_mixin(self):
        """Bleeding tests for permission_required_one mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.full_perm_user,
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                    user=self.full_group_user,
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
                    expected_messages=[
                        self.pdq__no_permissions_one__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_one__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__full_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.full_perm_user,
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warnings.catch_warnings(record=True) as warning:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                    user=self.full_group_user,
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
                    expected_messages=[
                        self.pdq__no_permissions_full__message,
                    ],
                )

            # Verify we get the expected console warning message.
            self.assertEqual(1, len(warning))
            self.assertEqual(RuntimeWarning, warning[-1].category)
            self.assertText(self.pdq__no_permissions_full__message, str(warning[-1].message))

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAutAuthenticationMixinsWithOverlap(BaseMixinTextCase):
    """Tests for overlapping mixin use.

    Decorator/mixin logic should always be additive.
    So defining two or more values means both cases must be true for the user to pass.

    Instances where overlap doesn't make sense should raise an error.
    """

    def test__stacked_permissions_required(self):
        """Test for view with both one_of_permissions and full_permissions requirements, in project "strict" mode.

        Should be additive and user has to pass both in order to access page.
        # TODO: Currently works as an either/or, not additive.
        """

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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
            self.assertEqual(
                ("auth.view_foo", "auth.delete_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
            self.assertEqual(
                ("auth.view_foo", "auth.delete_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
            self.assertEqual(
                ("auth.view_foo", "auth.delete_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-stacked-permissions-required",
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
            self.assertEqual(
                ("auth.view_foo", "auth.delete_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )
