"""
Tests for Decorator login in project "loose" authentication mode.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

# Internal Imports.
from .base_test_case import BaseDecoratorTestCase


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=False)
@override_settings(STRICT_POLICY=False)
@patch("adminlte2_pdq.constants.STRICT_POLICY", False)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", False)
class TestLooseAuthenticationDecorators(BaseDecoratorTestCase):
    """
    Test project authentication decorators, under project "Loose" mode.
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

    def test__no_decorators(self):
        """Test for view with no decorators, in project "Loose" mode. For sanity checking."""

        # Should succeed and load as expected for all users.
        for user_instance, user_str in self.user_list__full:
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

    def test__allow_anonymous_access_decorator(self):
        """Test for allow_anonymous_access decorator, in project "Loose" mode."""

        # Invalid decorator used for loose mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-anonymous-access",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

    def test__login_required_decorator(self):
        """Test for login_required decorator, in project "Loose" mode."""

        # Should fail and redirect to login for anyone un-authenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):
                # Should fail and redirect to login.

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-login-required",
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

        # Should succeed and load as expected for anyone that is properly authenticated.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):
                # Should succeed and load as expected.

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:function-login-required",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Login Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Login Required View Header",
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(response, decorator_name="login_required", login_required=True)

    def test__allow_without_permissions_decorator(self):
        """Test for allow_without_permissions decorator, in project "Loose" mode."""

        # Invalid decorator used for loose mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"Running as {user_str} user"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:function-allow-without-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Loose" mode."""

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
        """Test for permission_required decorator, in project "Loose" mode."""

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

        # Should succeed and load as expected for anyone with at least all expected perms.
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

    def test_one_permission_decorator_works_with_strings(self):
        """Tests that a function view using the OnePermissions decorator works
        when a string is provided instead of a list or tuple.
        """

        with self.subTest("As user with failing perm check"):

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:function-one-permission-required-as-string",
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
                    (
                        "AdminLtePdq Warning: Attempted to access function-based view "
                        "'one_permission_required_view_as_string' which "
                        "requires permissions, and user permission requirements were not met. "
                        "Redirected to project home instead. \n"
                        "\n\n"
                        "For further information, please see the docs: "
                        "https://django-adminlte2-pdq.readthedocs.io/"
                    ),
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with passing perm check"):

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:function-one-permission-required-as-string",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
                expected_not_messages=[
                    (
                        "AdminLtePdq Warning: Attempted to access function-based view "
                        "'one_permission_required_view_as_string' which "
                        "requires permissions, and user permission requirements were not met. "
                        "Redirected to project home instead. \n"
                        "\n\n"
                        "For further information, please see the docs: "
                        "https://django-adminlte2-pdq.readthedocs.io/"
                    ),
                ],
            )

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                one_of_permissions=("auth.add_foo",),
            )

    def test_full_permission_decorator_works_with_strings(self):
        """Tests that a function view using the FullPermissions decorator works
        when a string is provided instead of a list or tuple.
        """

        with self.subTest("As user with failing perm check"):

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:function-full-permissions-required-as-string",
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
                    (
                        "AdminLtePdq Warning: Attempted to access function-based view "
                        "'full_permissions_required_view_as_string' which "
                        "requires permissions, and user permission requirements were not met. "
                        "Redirected to project home instead. \n"
                        "\n\n"
                        "For further information, please see the docs: "
                        "https://django-adminlte2-pdq.readthedocs.io/"
                    ),
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertAdminPdqData(response, is_empty=True)

        with self.subTest("As user with passing perm check"):

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:function-full-permissions-required-as-string",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                expected_not_messages=[
                    (
                        "AdminLtePdq Warning: Attempted to access function-based view "
                        "'full_permissions_required_view_as_string' which "
                        "requires permissions, and user permission requirements were not met. "
                        "Redirected to project home instead. \n"
                        "\n\n"
                        "For further information, please see the docs: "
                        "https://django-adminlte2-pdq.readthedocs.io/"
                    ),
                ],
            )

            # Verify values associated with returned view.
            self.assertAdminPdqData(
                response,
                decorator_name="permission_required",
                login_required=True,
                full_permissions=("auth.add_foo",),
            )
