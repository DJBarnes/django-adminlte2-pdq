"""
Tests for AuthMiddleware in login-required mode.
"""

# System Imports.
from copy import copy
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST
from .base_test_case import MiddlewareBaseTestCase


# Module Variables.
UPDATED_LOGIN_EXEMPT_WHITELIST = LOGIN_EXEMPT_WHITELIST + ["adminlte2_pdq:demo-css"]

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
class LoginRequiredMiddlewareTestCase(MiddlewareBaseTestCase):
    """Test Middleware handling when in "LOGIN_REQUIRED" authentication mode."""

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
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_whitelists(self):
        """Test when "LOGIN_REQUIRED" mode and no whitelists set."""

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

    def test__login_redirect_next_url(self):
        """The login redirect passes the requested path, including any query string, as "next"."""

        with self.subTest("Path only"):
            response = self.client.get("/demo-css/")

            self.assertRedirects(response, "/accounts/login/?next=/demo-css/", fetch_redirect_response=False)

        with self.subTest("Path with query string"):
            response = self.client.get("/demo-css/?tab=1&sort=name")

            self.assertRedirects(
                response,
                "/accounts/login/?next=/demo-css/%3Ftab%3D1%26sort%3Dname",
                fetch_redirect_response=False,
            )

        with self.subTest("LOGIN_URL is a url name"):
            with patch("adminlte2_pdq.middleware.LOGIN_URL", "login"):
                response = self.client.get("/demo-css/")

            self.assertRedirects(response, "/accounts/login/?next=/demo-css/", fetch_redirect_response=False)

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test__with_login_whitelist(self):
        """Test when "LOGIN_REQUIRED" mode and login whitelist is set."""

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
