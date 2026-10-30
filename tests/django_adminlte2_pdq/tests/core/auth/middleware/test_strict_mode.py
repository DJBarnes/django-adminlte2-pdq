"""
Tests for AuthMiddleware in strict mode.
"""

# System Imports.
from copy import copy
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.contrib.messages import get_messages
from django.test import override_settings
from django.urls import reverse
from pytest import warns

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST
from adminlte2_pdq.middleware import (
    RESPONSE_403_PRODUCTION_MESSAGE,
)
from .base_test_case import MiddlewareBaseTestCase


# Module Variables.
UPDATED_LOGIN_EXEMPT_WHITELIST = LOGIN_EXEMPT_WHITELIST + ["adminlte2_pdq:demo-css"]
UPDATED_STRICT_POLICY_WHITELIST = STRICT_POLICY_WHITELIST + ["adminlte2_pdq:demo-css"]
UPDATED_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST = ["/tests/"]

NO_SESSION_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_SESSION_MIDDLEWARE.remove("django.contrib.sessions.middleware.SessionMiddleware")
NO_AUTH_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_AUTH_MIDDLEWARE.remove("django.contrib.auth.middleware.AuthenticationMiddleware")
NO_MESSAGES_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_MESSAGES_MIDDLEWARE.remove("django.contrib.messages.middleware.MessageMiddleware")

NO_SESSION_AUTH_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_SESSION_AUTH_MIDDLEWARE.remove("django.contrib.sessions.middleware.SessionMiddleware")
NO_SESSION_AUTH_MIDDLEWARE.remove("django.contrib.auth.middleware.AuthenticationMiddleware")


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class StrictMiddlewareTestCase(MiddlewareBaseTestCase):
    """Test Middleware handling when in "STRICT" authentication mode."""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify values imported from middleware file.
        # We don't use constants.py values because the above settings technically don't override such.
        # Plus this test is a middleware test so it's probably fine.
        # pylint:disable=redefined-outer-name reimported import-outside-toplevel
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

    def test__no_whitelists(self):
        """Test when "STRICT" mode and no whitelist is set."""

        with self.subTest("As anonymous user"):
            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

        with self.subTest("As user with full permissions"):
            with warns(Warning) as warning_info:
                # Process response.
                self.client.force_login(self.test_user_w_perms)
                response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_strict__no_decorator_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

    def test__no_whitelists__admin_page(self):
        """Test when "STRICT" mode and accessing the admin page."""

        with self.subTest("As user with full permissions"):
            # Process response.
            self.test_user_w_perms.is_staff = True
            self.test_user_w_perms.save()

            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("admin:auth_user_changelist"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Select user to change")

    def test__no_whitelists__unknown_page(self):
        """Test when "STRICT" mode and accessing a "bad" url."""

        with self.subTest("As user with full permissions"):
            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get("unknown/route/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test__with_login_whitelist(self):
        """Test when "STRICT" mode and login whitelist is set."""

        with self.subTest("As anonymous user"):
            # Should go to demo-css, fails the strict policy, then go to home.
            # Home is a new request that fails the login required being on and thus redirect to login page.
            with warns(Warning) as warning_info:
                # Process response.
                response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)
                self.assertEqual(response.status_code, 200)

                # Verify values associated with returned view.
                self.assertContains(response, "Login")

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_strict__no_decorator_message),
                (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

        with self.subTest("As user with full permissions"):
            # Should go to demo-css, fail the strict policy, then go to home.
            # Home is a new request that succeeds.
            with warns(Warning) as warning_info:
                self.client.force_login(self.test_user_w_perms)

                # Process response.
                response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)
                self.assertEqual(response.status_code, 200)

            # Verify values associated with returned view.
            self.assertContains(response, "Home")

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_strict__no_decorator_message),
                (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

    @patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", UPDATED_STRICT_POLICY_WHITELIST)
    def test__with_permission_whitelist(self):
        """Test when "STRICT" mode and permission whitelist is set."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", UPDATED_LOGIN_EXEMPT_WHITELIST)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", UPDATED_STRICT_POLICY_WHITELIST)
    def test__with_both_whitelists(self):
        """Test when "STRICT" mode and both whitelists are set."""

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/")  # Pretend the root url is a media file.
    def test__no_whitelists_and_home_page_is_media_route(self):
        """Test no white lists and home page is media route"""
        # MEDIA_URL should not be allowed to be the root of a website, thus can not skip the login required check.

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get("/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/demo-css/")  # Pretend the demo-css route is a media file.
    def test__no_whitelists_and_misc_page_is_media_route(self):
        """Test no white lists and misc page is media route"""

        with self.subTest("As anonymous user"):
            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

    @patch("adminlte2_pdq.middleware.WEBSOCKET_ROUTE", "/")  # Pretend the root url is a websocket file.
    def test__no_whitelists_and_home_page_is_websocket_route(self):
        """Test no white lists and home page is websocket route"""
        # WEBSOCKET_URL should not be allowed to be the root of a website, thus can not skip the login required check.

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get("/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

    @patch("adminlte2_pdq.middleware.WEBSOCKET_ROUTE", "/demo-css/")  # Pretend the demo-css route is a websocket file.
    def test__no_whitelists_and_misc_page_is_websocket_route(self):
        """Test no white lists and misc page is websocket route"""

        with self.subTest("As anonymous user"):
            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

    @override_settings(DEBUG=False)
    def test__view_without_permissions_in_production(self):
        """In production, a view with permission requirements but no permissions logs the problem, and the user
        gets the 403 handling: a redirect home with the 403 production message."""
        self.client.force_login(self.test_user_no_perms)

        with self.assertLogs("adminlte2_pdq.middleware", level="ERROR") as logs:
            response = self.client.get(reverse("adminlte2_pdq_tests:class-standard"))

        self.assertEqual(["ERROR:adminlte2_pdq.middleware:" + self.pdq_strict__no_permissions_set_message], logs.output)
        self.assertRedirects(response, reverse("adminlte2_pdq:home"), fetch_redirect_response=False)
        self.assertEqual(
            [RESPONSE_403_PRODUCTION_MESSAGE], [str(message) for message in get_messages(response.wsgi_request)]
        )

    @patch(
        "adminlte2_pdq.middleware.STRICT_POLICY_SERVE_403_FUZZY_WHITELIST",
        UPDATED_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST,
    )
    @patch(
        "adminlte2_pdq.mixins.STRICT_POLICY_SERVE_403_FUZZY_WHITELIST",
        UPDATED_STRICT_POLICY_SERVE_403_FUZZY_WHITELIST,
    )
    def test__with_fuzzy_403_whitelist(self):
        """Test when "STRICT" mode and fuzzy 403 whitelist is set."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get(
                reverse("adminlte2_pdq_tests:class-full-permissions-required-as-string"), follow=True
            )

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

        with self.subTest("As user with no permissions"):
            # Should raise a 403 permission denied.

            # Process response.
            self.client.force_login(self.test_user_no_perms)
            response = self.client.get(
                reverse("adminlte2_pdq_tests:class-full-permissions-required-as-string"), follow=True
            )

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 403)

        with self.subTest("As user with no permissions and view with manual perm handling"):
            # Should raise a 403 permission denied.

            with warns(Warning) as warning_info:
                # Process response.
                self.client.force_login(self.test_user_no_perms)
                response = self.client.get(reverse("adminlte2_pdq_tests:class-standard"), follow=True)

                # Verify values associated with returned view.
                self.assertEqual(response.status_code, 403)

                # Collect actual warnings that occurred.
                actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
                # Define expected warnings that should have occurred.
                expected_warns = {
                    (RuntimeWarning, self.pdq_strict__no_permissions_set_message),
                }
                # Assert warnings match.
                self.assertEqual(expected_warns, actual_warns)
