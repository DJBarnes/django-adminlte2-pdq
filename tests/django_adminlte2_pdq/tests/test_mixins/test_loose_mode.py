"""
Tests for Mixin login in project "loose" authentication mode.
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

        # Should succeed and load as expected for all users.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
                    user=user_instance,
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
        """Test for allow_anonymous_access mixin, in project "Loose" mode."""

        # Invalid decorator used for loose mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-anonymous-access",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Loose" mode."""

        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
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

        # Should succeed and load as expected for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-login-required",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Login Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Login Required View Header",
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="login_required",
                    login_required=True,
                )

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq_tests:class-login-required"])
    def test__login_required_decorator_and_login_whitelisted(self):
        """Test when both login_required decorator used and view is login whitelisted
        in "Loose" mode raises improperly configured error."""

        # Conflict between decorator and whitelist for login required. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-login-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__login_required_mixin_login_whitelist_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Loose" mode."""

        # Invalid decorator used for loose mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-without-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Loose" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-one-permission-required",
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
                    "adminlte2_pdq_tests:class-one-permission-required",
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
                        self.pdq__user_failed_perm_check.format(view_name="OnePermissionRequiredView"),
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
                    "adminlte2_pdq_tests:class-one-permission-required",
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

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Loose" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
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
                    "adminlte2_pdq_tests:class-full-permissions-required",
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
                        self.pdq__user_failed_perm_check.format(view_name="FullPermissionsRequiredView"),
                    ],
                )

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for anyone with expected perms.
        for user_instance, user_str in self.user_list__full_permissions:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required",
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

    def test_one_permission_mixin_works_with_strings(self):
        """Tests that a function view using the OnePermissions decorator works
        when a string is provided instead of a list or tuple.
        """

        with self.subTest("As user with failing perm check"):

            # Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required-as-string",
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
                        "AdminLtePdq Warning: Attempted to access class-based view "
                        "'OnePermissionRequiredViewAsString' which "
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

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-one-permission-required-as-string",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
                expected_not_messages=[
                    (
                        "AdminLtePdq Warning: Attempted to access class-based view "
                        "'OnePermissionRequiredViewAsString' which "
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

    def test_full_permission_mixin_works_with_strings(self):
        """Tests that a function view using the FullPermissions decorator works
        when a string is provided instead of a list or tuple.
        """

        with self.subTest("As user with failing perm check"):

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required-as-string",
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
                        "AdminLtePdq Warning: Attempted to access class-based view "
                        "'FullPermissionsRequiredViewAsString' which "
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

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests:class-full-permissions-required-as-string",
                user=self.full_perm_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
                expected_not_messages=[
                    (
                        "AdminLtePdq Warning: Attempted to access class-based view "
                        "'FullPermissionsRequiredViewAsString' which "
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


@override_settings(DEBUG=True)
class TestLooseAutAuthenticationMixinsWithLogicBleed(BaseMixinTextCase):
    """Tests to make sure mixin logic doesn't bleed into each other.

    By "bleeding", we refer to instances when the user overlaps values for one
    Mixin with another. Or forgets expected values of a Mixin. Or combinations thereof.

    For example, a LoginRequired Mixin should always behave the same as the login_required
    mixin, even if the user accidentally defines permissions on the view as well.

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

        # Invalid mixin used for Loose mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

    def test__bleeding_login_with_permissions(self):
        """Bleeding tests for login_required mixin, in project "Loose" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
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

        # Should succeed and load as expected for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Login Required View | Django AdminLtePdq Testing",
                    expected_header="Django AdminLtePdq | Login Required View Header",
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="login_required",
                    login_required=True,
                    one_of_permissions=("auth.add_foo", "auth.change_foo"),
                    full_permissions=("auth.add_foo", "auth.change_foo"),
                )

    def test__bleeding_conflicting_permissions(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Loose" mode."""

        # Invalid mixin used for Loose mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

    def test__bleeding_one_permission_missing_permissions(self):
        """Bleeding tests for permission_required_one mixin, in project "Loose" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                            self.pdq__no_permissions_one__message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq__no_permissions_one__message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Permission view incorrectly defined on view.
        # Should fail and redirect to "home" page for anyone authenticated.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
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
                            self.pdq__no_permissions_one__message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq__no_permissions_one__message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__bleeding_full_permission_missing_permissions(self):
        """Bleeding tests for permission_required_one mixin, in project "Loose" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                            self.pdq__no_permissions_full__message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq__no_permissions_full__message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Permission view incorrectly defined on view.
        # Should fail and redirect to "home" page for anyone authenticated.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
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
                            self.pdq__no_permissions_full__message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq__no_permissions_full__message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # Was redirected to login so should be no data.
                self.assertAdminPdqData(response, is_empty=True)
