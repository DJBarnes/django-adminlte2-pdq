"""
Tests for Decorator login in project "strict" authentication mode.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from adminlte2_pdq.middleware import RESPONSE_403_PRODUCTION_MESSAGE
from .base_test_case import BaseDecoratorTestCase


# Module Variables.
UserModel = get_user_model()


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class TestStrictAuthenticationDecorators(BaseDecoratorTestCase):
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
    def test__no_decorators__production_403_message_shown_once(self):
        """In production, a view with no decorators adds the 403 message once, not twice."""

        self.client.force_login(self.none_user)
        response = self.client.get(reverse("adminlte2_pdq_tests:function-standard"))

        message_texts = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertEqual(1, message_texts.count(RESPONSE_403_PRODUCTION_MESSAGE))

    @override_settings(DEBUG=False)
    @patch("adminlte2_pdq.middleware.RESPONSE_403_PRODUCTION_MESSAGE", "")
    def test__no_decorators__empty_production_403_message_adds_no_message(self):
        """An empty 403 production message adds no message, whether redirecting or raising PermissionDenied."""

        self.client.force_login(self.none_user)

        with self.subTest("Redirect to home"):
            response = self.client.get(reverse("adminlte2_pdq_tests:function-standard"))
            self.assertEqual([], list(get_messages(response.wsgi_request)))

        with self.subTest("PermissionDenied"):
            with patch("adminlte2_pdq.middleware.REDIRECT_TO_HOME_ON_403", False):
                response = self.client.get(reverse("adminlte2_pdq_tests:function-standard"))
            self.assertEqual(403, response.status_code)
            self.assertEqual([], list(get_messages(response.wsgi_request)))

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
class TestStrictAuthenticationDecoratorsWithOverlap(BaseDecoratorTestCase):
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
