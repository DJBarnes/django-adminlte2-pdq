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
from .base_test_case import BaseMixinTextCase


# Module Variables.
UserModel = get_user_model()


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationMixins(BaseMixinTextCase):
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

    @override_settings(DEBUG=False)
    @patch("adminlte2_pdq.middleware.REDIRECT_TO_HOME_ON_403", False)
    def test__no_decorators__redirect_on_403_turned_off(self):
        """Test for view with perms, in project "Strict" mode
        and the redirect on 403 setting is set to False.
        Unauthenticated users should get redirected to login.
        Everyone else should raise a 403 error rather than redirecting to Home.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required-strict",
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

        # Should fail and return 403 message, for all authenticated users lacking correct perms.
        user_list_missing_perms = self.user_list__no_permissions + self.user_list__partial_permissions
        for user_instance, user_str in user_list_missing_perms:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required-strict",
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

        # Should succeed for all users that have correct perms
        for user_instance, user_str in self.user_list__full_permissions:
            with self.subTest(f"As {user_str}"):

                # Verify we get the expected page.
                response = self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests:class-full-permissions-required-strict",
                    user=user_instance,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=False,
                    # Expected content on page.
                    expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                    expected_content=[
                        "Full Permissions Required",
                    ],
                )

                # Verify values associated with returned view.
                # View had no decorators so should be no data.
                self.assertAdminPdqData(response, is_empty=True)


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationMixinsWithLogicBleed(BaseMixinTextCase):
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
class TestStrictAuthenticationMixinsWithOverlap(BaseMixinTextCase):
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


@override_settings(DEBUG=False)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationMixinsWithLogicBleedInProduction(BaseMixinTextCase):
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

    def test__bleeding_conflicting_permissions__in_production(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Strict" mode in production."""

        # Should fail and redirect to login for anyone unauthenticated.
        for user_instance, user_str in self.user_list__unauthenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
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
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(response, is_empty=True)

        # Should succeed and load as expected for all authenticated users.
        for user_instance, user_str in self.user_list__authenticated:
            with self.subTest(f"As {user_str}"):

                #  Verify we get the expected page.
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
                )

                # Verify values associated with returned view.
                self.assertAdminPdqData(
                    response,
                    decorator_name="allow_without_permissions",
                    login_required=True,
                    allow_without_permissions=True,
                    one_of_permissions=("auth.add_foo", "auth.change_foo"),
                    full_permissions=("auth.add_foo", "auth.change_foo"),
                )
