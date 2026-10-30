"""
Tests for AuthMiddleware's URL processing, with APPEND_SLASH on and off.
"""

# System Imports.
from copy import copy
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from .base_test_case import MiddlewareBaseTestCase


# Module Variables.

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
@override_settings(APPEND_SLASH=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class MiddlewareUrlProcessingTestCaseAppendSlashTrue(MiddlewareBaseTestCase):
    """Test Middleware URL Processing with the APPEND_SLASH setting set to True"""

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
        self.assertTrue(settings.APPEND_SLASH)

    def test__trailing_slash__with_valid_url(self):
        """Tests handling of trailing url slashes with valid urls, when APPEND_SLASH is True."""

        with self.subTest("Processing url with a trailing slash"):
            # Should handle as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq:demo-css")

            # Verify url ends with slash.
            self.assertEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

            # Verify expected final url.
            self.assertEqual(url, response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then proceed as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq:demo-css")[:-1]

            # Verify url does NOT end with slash.
            self.assertNotEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS")

            # Verify expected final url.
            self.assertEqual(url + "/", response.request["PATH_INFO"])

    def test__trailing_slash__with_invalid_url(self):
        """Tests handling of trailing url slashes with bad urls, when APPEND_SLASH is True."""

        with self.subTest("Processing url with a trailing slash"):
            # Process response.
            response = self.client.get("/invalid-url/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then redirect to login.

            # Process response.
            response = self.client.get("/invalid-url", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

    def test__trailing_slash__with_valid_url_and_post_request(self):
        """Tests handling of trailing url slashes with valid urls,
        when APPEND_SLASH is True, but request is a POST request."""

        with self.subTest("Processing url with a trailing slash"):
            # Should handle as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq:demo-css")

            # Verify url ends with slash.
            self.assertEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.post(url)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

            # Verify expected final url.
            self.assertEqual(url, response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then proceed as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq:demo-css")[:-1]

            # Verify url does NOT end with slash.
            self.assertNotEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)

            with self.assertRaises(RuntimeError) as rte:
                response = self.client.post(url, follow=True)

            self.assertIn("You called this URL via", str(rte.exception))


@override_settings(DEBUG=True)
@override_settings(APPEND_SLASH=False)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class MiddlewareUrlProcessingTestCaseAppendSlashFalse(MiddlewareBaseTestCase):
    """Test Middleware URL Processing with the APPEND_SLASH setting set to False"""

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
        self.assertFalse(settings.APPEND_SLASH)

    def test__trailing_slash__with_valid_url(self):
        """Tests handling of trailing url slashes with valid urls, when APPEND_SLASH is False."""

        # NOTE: The APPEND_SLASH settings does just that, it will append a slash if it is missing
        # and the setting is set to True. It will NOT however remove any slashes.
        # So, if APPEND_SLASH is False and the URL is defined as "/foobar", when the user tries to
        # visit "/foobar/", Django will NOT remove the slash to make it "match". Thus the user should
        # get a 404 that causes a redirect to the Home route with the 404 message.

        with self.subTest("Processing url with a trailing slash"):
            # Should auto-magically remove the trailing slash, and then proceed as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq_tests:demo-css-no-slash") + "/"

            # Verify url ends with slash.
            self.assertEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request["PATH_INFO"], reverse("adminlte2_pdq:home"))
            self.assertContains(response, "Dashboard")
            self.assertContains(response, "The page you were looking for does not exist")

        with self.subTest("Processing url without a trailing slash"):
            # Should handle as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq_tests:demo-css-no-slash")

            # Verify url does NOT end with slash.
            self.assertNotEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

            # Verify expected final url.
            self.assertEqual(url, response.request["PATH_INFO"])

    def test__trailing_slash__with_invalid_url(self):
        """Tests handling of trailing url slashes with bad urls, when APPEND_SLASH is False."""

        # NOTE: Even though we are testing with AppendSlash set to False, the login
        # route is defined with a trailing slash. So, when we fail with an invalid url
        # we will get redirected to a URL that has a trailing slash (login).

        with self.subTest("Processing url with a trailing slash"):
            # Process response.
            response = self.client.get("invalid-url/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then redirect to login.
            # Process response.
            response = self.client.get("/invalid-url", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])
