"""
Tests for AuthMiddleware's URL processing, with APPEND_SLASH on and off.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from .base_test_case import MiddlewareBaseTestCase


@override_settings(DEBUG=True)
@override_settings(APPEND_SLASH=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class AppendSlashTrueTestCase(MiddlewareBaseTestCase):
    """URL processing with the APPEND_SLASH setting set to True."""

    def test__valid_url_with_trailing_slash(self):
        """The url loads as normal."""
        url = reverse("adminlte2_pdq:demo-css")
        self.assertTrue(url.endswith("/"))

        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")
        self.assertEqual(url, response.request["PATH_INFO"])

    def test__valid_url_without_trailing_slash(self):
        """The trailing slash is added, then the url loads as normal."""
        url = reverse("adminlte2_pdq:demo-css")[:-1]
        self.assertFalse(url.endswith("/"))

        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS")
        self.assertEqual(url + "/", response.request["PATH_INFO"])

    def test__invalid_url_with_trailing_slash(self):
        """An anonymous user is redirected to login."""
        response = self.client.get("/invalid-url/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Remember Me")
        self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

    def test__invalid_url_without_trailing_slash(self):
        """An anonymous user is redirected to login."""
        response = self.client.get("/invalid-url", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Remember Me")
        self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

    def test__post_to_valid_url_with_trailing_slash(self):
        """A POST request loads as normal."""
        url = reverse("adminlte2_pdq:demo-css")
        self.assertTrue(url.endswith("/"))

        self.client.force_login(self.test_user_w_perms)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")
        self.assertEqual(url, response.request["PATH_INFO"])

    def test__post_to_valid_url_without_trailing_slash(self):
        """Django can't add the slash to a POST request without losing the data, so it raises an error."""
        url = reverse("adminlte2_pdq:demo-css")[:-1]
        self.assertFalse(url.endswith("/"))

        self.client.force_login(self.test_user_w_perms)
        with self.assertRaises(RuntimeError) as rte:
            self.client.post(url, follow=True)

        self.assertIn("You called this URL via", str(rte.exception))


@override_settings(DEBUG=True)
@override_settings(APPEND_SLASH=False)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class AppendSlashFalseTestCase(MiddlewareBaseTestCase):
    """URL processing with the APPEND_SLASH setting set to False."""

    def test__valid_url_with_trailing_slash(self):
        """APPEND_SLASH only adds slashes, it never removes them. A url defined without a trailing slash but requested
        with one doesn't match, so the user is redirected home with the 404 message."""
        url = reverse("adminlte2_pdq_tests:demo-css-no-slash") + "/"

        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], reverse("adminlte2_pdq:home"))
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "The page you were looking for does not exist")

    def test__valid_url_without_trailing_slash(self):
        """The url loads as normal."""
        url = reverse("adminlte2_pdq_tests:demo-css-no-slash")
        self.assertFalse(url.endswith("/"))

        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")
        self.assertEqual(url, response.request["PATH_INFO"])

    def test__invalid_url_with_trailing_slash(self):
        """An anonymous user is redirected to login. The login url has a trailing slash."""
        response = self.client.get("invalid-url/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Remember Me")
        self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

    def test__invalid_url_without_trailing_slash(self):
        """An anonymous user is redirected to login. The login url has a trailing slash."""
        response = self.client.get("/invalid-url", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Remember Me")
        self.assertEqual("/accounts/login/", response.request["PATH_INFO"])
