"""
Tests for Decorator login in project "strict" authentication mode.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from pytest import warns

# Internal Imports.
from .base_test_case import BaseDecoratorTestCase, LOGIN_WHITELIST_VIEWS, PERM_WHITELIST_VIEWS


# Module Variables.
UserModel = get_user_model()


class StrictModeMixin:
    """Test project authentication decorators, under project "Strict" mode.

    This class is a parent class that should not run by itself.
    It needs to be imported into other classes to execute.
    """

    def test__no_decorators(self):
        """Test for view with no decorators, in project "Strict" mode.
        Everything should redirect with a warning message.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-standard",
                    user=user_instance,
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

        # Should fail and redirect to home with a warning message, for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-standard",
                        user=user_instance,
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
                            self.pdq_strict__no_decorator_message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_decorator_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_decorator(self):
        """Test for allow_anonymous_access decorator, in project "Strict" mode."""

        # Should succeed and load as expected for all users.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-allow-anonymous-access",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="allow_anonymous_access",
                    allow_anonymous_access=True,
                )

    def test__login_required_decorator(self):
        """Test for login_required decorator, in project "Strict" mode.
        In strict mode, this decorator should NOT work, and instead raise errors.
        """

        # Invalid decorator used for Strict mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-login-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

    def test__allow_without_permissions_decorator(self):
        """Test for allow_without_permissions decorator, in project "Strict" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-allow-without-permissions",
                    user=user_instance,
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
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for anyone authenticated.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-allow-without-permissions",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="allow_without_permissions",
                    login_required=True,
                    allow_without_permissions=True,
                )

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Strict" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-one-permission-required",
                    user=user_instance,
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

        # Should fail and redirect to "home" page for anyone missing perms.
        for user_instance, user_str in self.user_list__no_permissions:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-one-permission-required",
                    user=user_instance,
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
                        self.pdq__user_failed_perm_check.format(view_name="one_permission_required_view"),
                    ],
                )

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for anyone with at least one expected perm.
        for user_instance, user_str in (
            *self.user_list__partial_permissions,
            *self.user_list__full_permissions,
        ):
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-one-permission-required",
                    user=user_instance,
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

    def test__full_permission_required_decorator(self):
        """Test for permission_required decorator, in project "Strict" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-full-permissions-required",
                    user=user_instance,
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

        # Should fail and redirect to "home" page for anyone missing perms.
        for user_instance, user_str in (
            *self.user_list__no_permissions,
            *self.user_list__partial_permissions,
        ):
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-full-permissions-required",
                    user=user_instance,
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
                        self.pdq__user_failed_perm_check.format(view_name="full_permissions_required_view"),
                    ],
                )

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for anyone with full perms.
        for user_instance, user_str in self.user_list__full_permissions:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-full-permissions-required",
                    user=user_instance,
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
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationDecorators(BaseDecoratorTestCase, StrictModeMixin):
    """Runtime test execution of decorators under "Strict" mode."""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # NOTE: The heavy lifting of these tests is done in the middleware.
        # Therefore the patch that is used needs to target the imports in the middleware.
        # Import from the middleware to verify that the patch works as intended.
        # Settings do not need to be overridden because every setting is first converted
        # to a constant. So, we only need to patch the constant in the middleware.

        # Verify values imported from middleware.py file.
        # pylint: disable=import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    @override_settings(DEBUG=False)
    @patch("adminlte2_pdq.middleware.REDIRECT_TO_HOME_ON_403", False)
    def test__no_decorators__redirect_on_403_turned_off(self):
        """Test for view with no decorators, in project "Strict" mode
        and the redirect on 403 setting is set to False.
        Everything should raise a 403 error rather than redirecting to Home.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-standard",
                    user=user_instance,
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

        # Should fail and redirect to home with a warning message, for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-standard",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=403,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="403 Forbidden",
                    expected_content=[
                        "403 Forbidden",
                    ],
                )

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
class TestStrictAuthenticationDecoratorsWithLoginWhitelist(BaseDecoratorTestCase, StrictModeMixin):
    """Runtime test execution of decorators under "Strict" mode, with login whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    In this case, due to strict mode, this whitelist mostly doesn't do anything by itself,
    other than cause warnings.

    Modified States are:
    * "no_decorator" - Raises "ineffective whitelist" warning and the default STRICT_MODE warning.
    * "allow_anonymous_access" - Raises "ineffective whitelist" warning and "overlaps with whitelist" warning.
    * "one_of_perms"/"full_perms" - Raises only the "ineffective whitelist" warning.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # NOTE: The heavy lifting of these tests is done in the middleware.
        # Therefore the patch that is used needs to target the imports in the middleware.
        # Import from the middleware to verify that the patch works as intended.
        # Settings do not need to be overridden because every setting is first converted
        # to a constant. So, we only need to patch the constant in the middleware.

        # Verify values imported from middleware.py file.
        # pylint: disable=import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(13, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_decorators(self):
        """Test for view with no decorators, in project "Strict" mode, with login whitelist.

        Raises "ineffective whitelist" warning and the default STRICT_MODE warning.
        """

        # View configured incorrectly for strict mode. Should initially redirect to "home".
        # But then since we're also not logged in, it redirects to login required page.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-standard",
                        user=user_instance,
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
                            self.pdq_strict__no_decorator_message,
                            self.pdq_strict__ineffective_login_whitelist_message__no_decorator,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_decorator_message),
                    (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message__no_decorator),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # View configured incorrectly for strict mode.
        # Should fail and redirect to home with a warning message, for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-standard",
                        user=user_instance,
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
                            self.pdq_strict__no_decorator_message,
                            self.pdq_strict__ineffective_login_whitelist_message__no_decorator,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_decorator_message),
                    (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message__no_decorator),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_decorator(self):
        """Test for allow_anonymous_access decorator, in project "Strict" mode, with login whitelist.

        Raises "ineffective whitelist" warning and "overlaps with whitelist" warning.
        """

        # Should succeed and load as expected for all users.
        # However, should raise a "ineffective whitelist" warning.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-anonymous-access",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=200,
                        view_should_redirect=False,
                        # Expected content on page.
                        expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                        expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                        expected_messages=[
                            self.pdq_login__allow_anonymous_access_whitelist_overlap_message,
                            self.pdq_strict__ineffective_login_whitelist_message__anonymous_access,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_login__allow_anonymous_access_whitelist_overlap_message),
                    (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message__anonymous_access),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "login required" mode, with login whitelist.

        Raises only the "ineffective whitelist" warning.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-one-permission-required",
                        user=user_instance,
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

        # Should fail and redirect to "home" page for anyone missing perms.
        for user_instance, user_str in self.user_list__no_permissions:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-one-permission-required",
                        user=user_instance,
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
                            self.pdq__user_failed_perm_check.format(view_name="one_permission_required_view"),
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

        # Should succeed and load as expected for anyone with at least one expected perm.
        # However, should raise a "ineffective whitelist" warning.
        for user_instance, user_str in (
            *self.user_list__partial_permissions,
            *self.user_list__full_permissions,
        ):
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-one-permission-required",
                        user=user_instance,
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

    def test__full_permission_required_decorator(self):
        """Test for permission_required decorator, in project "login required" mode, with login whitelist.

        Raises only the "ineffective whitelist" warning.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-full-permissions-required",
                        user=user_instance,
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

        # Should fail and redirect to "home" page for anyone missing perms.
        for user_instance, user_str in (
            *self.user_list__no_permissions,
            *self.user_list__partial_permissions,
        ):
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-full-permissions-required",
                        user=user_instance,
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
                            self.pdq__user_failed_perm_check.format(view_name="full_permissions_required_view"),
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

        # Should succeed and load as expected for anyone with expected perms.
        # However, should raise a "ineffective whitelist" warning.
        for user_instance, user_str in self.user_list__full_permissions:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-full-permissions-required",
                        user=user_instance,
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


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", PERM_WHITELIST_VIEWS)
class TestStrictAuthenticationDecoratorsWithPermWhitelist(BaseDecoratorTestCase, StrictModeMixin):
    """Runtime test execution of decorators under "Strict" mode, with permission whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    Modified States are:
    * "one_of_permissions"/"full_permissions" - Raises errors because they don't make sense.
    * Everything else should effectively behave as if it was in "Login Required" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # NOTE: The heavy lifting of these tests is done in the middleware.
        # Therefore the patch that is used needs to target the imports in the middleware.
        # Import from the middleware to verify that the patch works as intended.
        # Settings do not need to be overridden because every setting is first converted
        # to a constant. So, we only need to patch the constant in the middleware.

        # Verify values imported from middleware.py file.
        # pylint: disable=import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(16, len(STRICT_POLICY_WHITELIST))

    def test__no_decorators(self):
        """Test for view with no decorators, in project "STRICT" mode, with perm whitelist.

        Effectively runs the same as LoginRequired no_mixin tests.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-standard",
                    user=user_instance,
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

        # Should succeed and load as expected for anyone authenticated.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-standard",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Standard View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Standard View Header",
                )

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_without_permissions_decorator(self):
        """Test for allow_without_permissions decorator, in project "Strict" mode, with perm whitelist.

        Raises warnings about redundancy with whitelist.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-without-permissions",
                        user=user_instance,
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

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__allow_without_permissions_whitelist_overlap_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for all authenticated users.
        # However, should raise a "redundant whitelist" warning.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-without-permissions",
                        user=user_instance,
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

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__allow_without_permissions_whitelist_overlap_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="allow_without_permissions",
                    login_required=True,
                    allow_without_permissions=True,
                )

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Strict" mode, with perm whitelist.

        Raises error because it doesn't make sense to be in a permission whitelist
        AND have a permission_required decorator.
        """

        # All users should raise the same error.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-one-permission-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__one_permission_required_whitelist_overlap_message, str(err.exception))

    def test__full_permission_required_decorator(self):
        """Test for permission_required decorator, in project "Strict" mode, with perm whitelist.

        Raises error because it doesn't make sense to be in a permission whitelist
        AND have a permission_required decorator.
        """

        # All users should raise the same error.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-full-permissions-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__full_permission_required_whitelist_overlap_message, str(err.exception))


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST_VIEWS)
@patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", PERM_WHITELIST_VIEWS)
class TestStrictAuthenticationDecoratorsWithBothWhitelists(BaseDecoratorTestCase, StrictModeMixin):
    """Runtime test execution of decorators under "Strict" mode, with both whitelists set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    In this case, pretty much everything should be visible to all user types, as long as it's
    a decorator that can be used in strict mode at all.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # NOTE: The heavy lifting of these tests is done in the middleware.
        # Therefore the patch that is used needs to target the imports in the middleware.
        # Import from the middleware to verify that the patch works as intended.
        # Settings do not need to be overridden because every setting is first converted
        # to a constant. So, we only need to patch the constant in the middleware.

        # Verify values imported from middleware.py file.
        # pylint: disable=import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(13, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(16, len(STRICT_POLICY_WHITELIST))

    def test__no_decorators(self):
        """Test for view with no decorators, in project "strict" mode, with both whitelists."""

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"Running as {user_str} user"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-standard",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Standard View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Standard View Header",
                )

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_decorator(self):
        """Test for allow_anonymous_access decorator, in project "Strict" mode, with both whitelists."""

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-anonymous-access",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=200,
                        view_should_redirect=False,
                        # Expected content on page.
                        expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                        expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
                        expected_messages=[
                            self.pdq_login__allow_anonymous_access_whitelist_overlap_message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_login__allow_anonymous_access_whitelist_overlap_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(response, decorator_name="allow_anonymous_access", allow_anonymous_access=True)

    def test__login_required_decorator(self):
        """Test for login_required decorator, in project "Strict" mode, with both whitelists.

        In strict mode, this decorator should NOT work, and instead raise errors.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    # Verify we get the expected page.
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-login-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )

                self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

    def test__allow_without_permissions_decorator(self):
        """Test for allow_without_permissions decorator, in project "Strict" mode, with both whitelists."""

        # NOTE: For unauthenticated users, they will pass all of the middleware checks correctly here.
        # However, the decorator "allow_without_permissions" assumes that the user needs to be logged in.
        # It does because the "allow_without_permissions" decorator uses the django "login_required" decorator
        # under the hood. This means that even though we have whitelisted the view in the login required
        # whitelist, it has no effect because the "login_required" decorator does not look at the whitelist
        # to know if it needs to still allow the request to go through. Maybe we need to fix this.
        # In short, the middleware works as intended. But, since the actual "allow_without_permission"
        # decorator uses "login_required", login is still required.
        # TODO: Consider changing how the "allow_without_permission" decorator works.

        # Anonymous users will need to be logged in despite it being whitelisted for the reasons above.
        # Thus they will see the login page.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-without-permissions",
                        user=user_instance,
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

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__allow_without_permissions_whitelist_overlap_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # All logged in users will be able to get to the view as intended.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-without-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=200,
                        view_should_redirect=False,
                        # Expected content on page.
                        expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                        expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__allow_without_permissions_whitelist_overlap_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="allow_without_permissions",
                    login_required=True,
                    allow_without_permissions=True,
                )

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Strict" mode, with both whitelists.

        Should raise error since it's both permission whitelisted and requiring a permission.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-one-permission-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__one_permission_required_whitelist_overlap_message, str(err.exception))

    def test__full_permission_required_decorator(self):
        """Test for permission_required decorator, in project "Strict" mode, with both whitelists.

        Should raise error since it's both permission whitelisted and requiring a permission.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-full-permissions-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__full_permission_required_whitelist_overlap_message, str(err.exception))


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAutAuthenticationMixinsWithOverlap(BaseDecoratorTestCase):
    """Tests for overlapping decorator use.

    Decorator/mixin logic should always be additive.
    So defining two or more values means both cases must be true for the user to pass.

    Instances where overlap doesn't make sense should raise an error.
    """

    def setUp(self, *args, **kwargs):

        # Call parent logic.
        super().setUp(*args, **kwargs)

        # Create new user equivalent to original full_perm_user.
        self.full_perm_user_plus_one = self.get_user("john_full_plus_one")
        self.add_user_permission("add_foo", user=self.full_perm_user_plus_one)
        self.add_user_permission("change_foo", user=self.full_perm_user_plus_one)
        # Add one of the "plus one" permissions required to pass the stacked permission tests.
        self.add_user_permission("view_foo", user=self.full_perm_user_plus_one)

        # Create new user equivalent to original staff full_perm_user.
        self.full_perm_staff_user_plus_one = self.get_user("jessie_staff_full_plus_one")
        self.add_user_permission("add_foo", user=self.full_perm_staff_user_plus_one)
        self.add_user_permission("change_foo", user=self.full_perm_staff_user_plus_one)
        # Add one of the "plus one" permissions required to pass the stacked permission tests.
        self.add_user_permission("delete_foo", user=self.full_perm_staff_user_plus_one)

        # Create new user equivalent to original full_group_user.
        self.full_group_user_plus_one = self.get_user("jenny_full_plus_one")
        self.add_user_group("add_bar", user=self.full_group_user_plus_one)
        self.add_user_group("change_bar", user=self.full_group_user_plus_one)
        # Add one of the "plus one" permissions required to pass the stacked permission tests.
        self.add_user_group("view_bar", user=self.full_group_user_plus_one)

    def test__stacked_permissions_required(self):
        """Test for view with both one_of_permissions and full_permissions requirements, in project "strict" mode.

        Should be additive and user has to pass both in order to access page.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-full-permissions-required",
                    user=user_instance,
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

        # Should fail and redirect to "home" page for anyone missing perms.
        # Here, we only check for our original "no perm", "partial perm", and "full perm" users.
        # Both original sets of users with perms will pass one stack check, but fail the other.
        # Thus, all should redirect to home.
        for user_instance, user_str in (
            *self.user_list__no_permissions,
            *self.user_list__partial_permissions,
            # "Full Perms" users, but minus the superuser.
            [self.full_perm_user, "user with full permissions"],
            [self.full_perm_staff_user, "staff user with full permissions"],
            [self.full_group_user, "user with full groups"],
        ):
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-stacked-permissions-required",
                    user=user_instance,
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

        # Should succeed and load as expected for anyone with both sets of perms.
        for user_instance, user_str in (
            [self.full_perm_user_plus_one, "user with orig full permissions, plus extra stacked one"],
            [self.full_perm_staff_user_plus_one, "staff user with orig full permissions, plus extra stacked one"],
            [self.full_group_user_plus_one, "user with orig full groups, plus extra stacked one"],
            [self.super_user, "superuser"],
        ):
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-stacked-permissions-required",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                )

                # Verify values associated with returned view.
                # TODO: Doesn't seem to return expected view data, but the login/auth redirects seem to
                #   handle as desired, so maybe it's fine?
                #   Should have both one_of_permissions and full_permissions defined, due to stacking.
                #   Same as how the equivalent mixin tests work.
                self.assertAdminPdqData(
                    response,
                    decorator_name="permission_required",
                    login_required=True,
                    one_of_permissions=("auth.view_foo", "auth.delete_foo"),
                )
