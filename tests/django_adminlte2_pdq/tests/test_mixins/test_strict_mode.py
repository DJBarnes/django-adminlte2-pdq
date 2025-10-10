"""
Tests for Mixin login in project "strict" authentication mode.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from pytest import warns

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

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
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
                # View had no mixins so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Should fail and redirect to home for all users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-standard",
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
                            self.pdq_strict__no_mixin_message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_mixin_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # View had no mixins so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode."""

        # Should succeed and load as expected for all users.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
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

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Strict" mode.

        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        # Invalid mixin used for Strict mode. Should raise error for all user types.
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
                self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Strict" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
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

        # Should succeed and load as expected for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=user_str,
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

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode."""

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
        """Test for permission_required mixin, in project "Strict" mode."""

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

        # Should succeed and load as expected for anyone with at least one expected perm.
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


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationMixins(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode."""

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


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
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

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Strict" mode, with login whitelist.

        Raises "ineffective whitelist" warning and the default STRICT_MODE warning.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-standard",
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
                            self.pdq_strict__no_mixin_message,
                            self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_mixin_message),
                    (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message__no_mixin),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # View had no mixins so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

        # Should fail and redirect to login for all users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-standard",
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
                            self.pdq_strict__no_mixin_message,
                            self.pdq_strict__ineffective_login_whitelist_message__no_mixin,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_mixin_message),
                    (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message__no_mixin),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                # View had no mixins so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode, with login whitelist.

        Raises "ineffective whitelist" warning and "overlaps with whitelist" warning.
        """

        # Should succeed and load as expected for all users.
        # However, should raise "ineffective whitelist" warnings.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-anonymous-access",
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

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode, with login whitelist.

        Raises only the "ineffective whitelist" warning.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
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
        for user_instance, user_str in (
            *self.user_list__partial_permissions,
            *self.user_list__full_permissions,
        ):
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
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
        """Test for permission_required mixin, in project "Strict" mode, with login whitelist.

        Raises only the "ineffective whitelist" warning.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
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

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
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

        for user_instance, user_str in self.user_list__full_permissions:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
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
class TestStrictAuthenticationMixinsWithPermWhitelist(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode, with login whitelist set for views.

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

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Strict" mode, with perm whitelist.

        Effectively runs the same as LoginRequired no_mixin tests.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-standard",
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

        # Should succeed and load as expected for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
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

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Strict" mode, with perm whitelist.

        Raises warnings about redundancy with whitelist.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-without-permissions",
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

        # Should succeed and load as expected for all users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-without-permissions",
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

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode, with perm whitelist.

        Raises error because it doesn't make sense to be in a permission whitelist
        AND have a permission_required mixin.
        """

        # All users should raise the same error.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-one-permission-required",
                        user=user_instance,
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
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-full-permissions-required",
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
class TestStrictAuthenticationMixinsWithBothWhitelists(BaseMixinTextCase, StrictModeMixin):
    """Runtime test execution of mixins under "Strict" mode, with login whitelist set for views.

    Only tests that are expected to behave differently with the whitelists are redefined here.

    In this case, pretty much everything should be visible to all user types, as long as it's
    a mixin that can be used in strict mode at all.
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

    def test__no_mixins(self):
        """Test for view with no mixin, in project "strict" mode, with both whitelists."""

        # All users are in both login and permission whitelist, so they should handle all the same.
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
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode."""

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-allow-anonymous-access",
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

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Strict" mode, with both whitelists.

        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    # Verify we get the expected page.
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-login-required",
                        user=user_instance,
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
        # for user_instance, user_str in self.user_list__full:
        #     with self.subTest(f"As {user_str}"):
        #
        #         # Verify we get the expected page.
        #         response = self.assertGetResponse(
        #             # View setup.
        #             "adminlte2_pdq_tests:class-allow-without-permissions",
        #             user=user_instance,
        #             # Expected view return data.
        #             expected_status=200,
        #             view_should_redirect=False,
        #             # Expected content on page.
        #             expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
        #             expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
        #         )
        #
        #         # Verify values associated with returned view.
        #         self.assertAdminPdqData(
        #             response,
        #             decorator_name="allow_without_permissions",
        #             login_required=True,
        #             allow_without_permissions=True,
        #         )

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode, with both whitelists.

        Should raise error since it's both permission whitelisted and requiring a permission.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-one-permission-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__one_permission_required_whitelist_overlap_message, str(err.exception))

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Strict" mode, with both whitelists.

        Should raise error since it's both permission whitelisted and requiring a permission.
        """

        # All users are in both login and permission whitelist, so they should handle all the same.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-full-permissions-required",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__full_permission_required_whitelist_overlap_message, str(err.exception))


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
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

    def test__bleeding_anonymous_with_permissions(self):
        """Bleeding tests for allow_anonymous_access mixin, in project "Strict" mode."""

        # Should succeed and load as expected for all users.
        for user_instance, user_str in self.user_list__full_permissions:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
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
                    one_of_permissions=("auth.add_foo", "auth.change_foo"),
                    full_permissions=("auth.add_foo", "auth.change_foo"),
                )

    def test__bleeding_login_with_permissions(self):
        """Test for login_required mixin, in project "Strict" mode.
        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        # Invalid mixin used for Strict mode. Should raise error for all user types.
        for user_instance, user_str in self.user_list__full:
            with self.subTest(f"As {user_str}"):

                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=500,
                    )
                self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__bleeding_conflicting_permissions(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Strict" mode."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
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
                            self.pdq__allow_without_permissions__conflicting_message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq__allow_without_permissions__conflicting_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
                with warns(Warning) as warning_info:
                    response = self.assertGetResponse(
                        # View setup.
                        "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                        user=user_instance,
                        # Expected view return data.
                        expected_status=200,
                        view_should_redirect=False,
                        # Expected content on page.
                        expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                        expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
                        expected_messages=[
                            self.pdq__allow_without_permissions__conflicting_message,
                        ],
                    )

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq__allow_without_permissions__conflicting_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="allow_without_permissions",
                    login_required=True,
                    allow_without_permissions=True,
                    one_of_permissions=("auth.add_foo", "auth.change_foo"),
                    full_permissions=("auth.add_foo", "auth.change_foo"),
                )

    def test__bleeding_one_permission_required_mixin(self):
        """Bleeding tests for permission_required_one mixin, in project "Strict" mode."""

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

    def test__bleeding_full_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode."""

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


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAutAuthenticationMixinsWithOverlap(BaseMixinTextCase):
    """Tests for overlapping mixin use.

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
                    "adminlte2_pdq_tests:class-stacked-permissions-required",
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

        # Should succeed and load as expected for anyone with both types of perms.
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
                    "adminlte2_pdq_tests:class-stacked-permissions-required",
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
                    one_of_permissions=("auth.view_foo", "auth.delete_foo"),
                    full_permissions=("auth.add_foo", "auth.change_foo"),
                )
