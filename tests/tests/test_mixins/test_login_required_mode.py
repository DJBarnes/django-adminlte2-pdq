"""
Tests for Mixin login in project "login required" authentication mode.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from pytest import warns

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

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
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Login Required" mode.

        In Login Required mode, this mixin should NOT work, and instead raise errors.
        """

        # Invalid mixin used for Login Required mode. Should raise error for all user types.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-login-required",
                        user=user,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_login__login_required_mixin_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Login Required" mode.

        In Login Required mode, this mixin should NOT work, and instead raise errors.
        """

        # Invalid mixin used for Login Required mode. Should raise error for all user types.
        for user in self.user_list:
            with self.subTest(f"Running as {user.username} user"):
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-without-permissions",
                        user=user,
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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to "home" page.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to "home" page.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to "home" page.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with one permission"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As staff user with one permission"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_staff_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.incorrect_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with one group"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_group_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
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
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
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
    * "no_mixin" - The "anonymous" and "inactive" users can now access the page.
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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

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
            self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Login Required" mode, with login whitelist.

        Raises a "whitelist overlap" warning.
        """

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As an inactive user"):
            # Shouldn't really be possible.
            # But testing anyway since package does a lot of background magic with auth logic.
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As staff user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_login__allow_anonymous_whitelist_overlap_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Login Required" mode, with login whitelist.

        Raises an "ineffective whitelist" warning.
        """

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to "home" page.

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to "home" page.

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As staff user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to "home" page.

            # Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__one_of_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__one_of_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo", "auth.change_foo"),
            )

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Login Required" mode, with login whitelist.

        Raises an "ineffective whitelist" warning.
        """

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As an inactive user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.none_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with one permission"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.partial_perm_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As staff user with no permissions"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.none_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As staff user with one permission"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.partial_perm_staff_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As staff user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.incorrect_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with one group"):
            # Should fail and redirect to "home" page.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
                    user=self.partial_group_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                    expected_messages=[
                        self.pdq__ineffective_login_whitelist_message__full_perms,
                    ],
                )

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
            )

        with self.subTest("As a superuser"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            with warns(Warning) as warning_info:
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

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq__ineffective_login_whitelist_message__full_perms),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo", "auth.change_foo"),
            )
