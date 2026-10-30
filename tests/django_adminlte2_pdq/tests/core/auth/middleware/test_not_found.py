"""
Tests for AuthMiddleware's handling of unknown URLs (404s).
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.test import override_settings, RequestFactory
from django.urls import reverse

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST
from adminlte2_pdq.middleware import (
    AuthMiddleware,
    RESPONSE_404_DEBUG_MESSAGE,
    RESPONSE_404_PRODUCTION_MESSAGE,
)
from .base_test_case import MiddlewareBaseTestCase


class NotFound404HandlingTestCase(MiddlewareBaseTestCase):
    """Test that the middleware handles 404s as intended."""

    def test__unknown_static_url_returns_404(self):
        """Test that an unknown static url returns the default Django 404 page
        vs redirecting to the home page"""
        response = self.client.get("/static/missing.css")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.content.decode())

    @patch("adminlte2_pdq.middleware.STATIC_ROUTE", "/")
    def test__unknown_static_url_redirects_to_home_when_static_setting_incorrect(self):
        """Test that an unknown static url redirects to home when the
        static setting is incorrect"""
        response = self.client.get("/static/missing.css", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test__unknown_media_url_returns_404(self):
        """Test that an unknown static url returns the default Django 404 page
        vs redirecting to the home page"""
        response = self.client.get("/media/missing.png", follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.content.decode())

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/")
    def test__unknown_media_url_redirects_to_home_when_media_setting_incorrect(self):
        """Test that an unknown media url redirects to home when the
        media setting is incorrect"""
        response = self.client.get("/media/missing.png", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test__unknown_favicon_url_returns_404(self):
        """Test that an unknown static url returns the default Django 404 page
        vs redirecting to the home page"""
        response = self.client.get("/favicon.ico", follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.content.decode())

    def test__unknown_whitelisted_url_returns_404(self):
        """Test that an unknown static url returns the default Django 404 page
        vs redirecting to the home page"""
        response = self.client.get("/.well-known/appspecific/com.chrome.devtools.json", follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.content.decode())

    def test__unknown_app_url_redirects_to_home(self):
        """Test that an unknown app url redirects to the home page"""
        response = self.client.get("/missing/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    @patch("adminlte2_pdq.middleware.REDIRECT_TO_HOME_ON_404", False)
    def test__unknown_app_url_returns_404_when_redirect_turned_off(self):
        """Test that an unknown static url returns the default Django 404 page
        vs redirecting to the home page when redirect turned off"""
        response = self.client.get("/missing/", follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.content.decode())


class NotFound404LoginWallTestCase(MiddlewareBaseTestCase):
    """Unknown urls behind a login wall look the same as existing pages to anonymous users."""

    login_url = "/accounts/login/?next=%2Fmissing%2F"

    def _get(self, path="/missing/", user=None):
        """Request a url with a new client, so no messages are left over from an earlier request."""
        self.client = self.client_class()
        if user:
            self.client.force_login(user)
        response = self.client.get(path)
        return response, [str(message) for message in get_messages(response.wsgi_request)]

    def _assert_home_with_message(self, expected_message, path="/missing/", user=None):
        for debug, message in ((True, RESPONSE_404_DEBUG_MESSAGE), (False, RESPONSE_404_PRODUCTION_MESSAGE)):
            with self.subTest(debug=debug):
                with override_settings(DEBUG=debug):
                    response, messages = self._get(path, user)
                    self.assertRedirects(response, reverse("adminlte2_pdq:home"), fetch_redirect_response=False)
                    self.assertEqual([message] if expected_message else [], messages)

    def test__loose_mode(self):
        """No login wall: anonymous users are redirected home with the message."""
        self._assert_home_with_message(True)

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test__login_required__anonymous(self):
        """Anonymous users go to the login page, the same as for an existing page."""
        response, messages = self._get()
        self.assertRedirects(response, self.login_url, fetch_redirect_response=False)
        self.assertEqual([], messages)

        # An existing page that requires login redirects the same way.
        response, _messages = self._get("/sample1/")
        self.assertRedirects(response, "/accounts/login/?next=%2Fsample1%2F", fetch_redirect_response=False)

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict__anonymous(self):
        """Anonymous users go to the login page in strict mode."""
        response, messages = self._get()
        self.assertRedirects(response, self.login_url, fetch_redirect_response=False)
        self.assertEqual([], messages)

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    def test__login_required__logged_in(self):
        """Logged-in users are redirected home with the message."""
        self._assert_home_with_message(True, user=self.test_user_w_perms)

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict__logged_in(self):
        """Logged-in users are redirected home with the message in strict mode."""
        self._assert_home_with_message(True, user=self.test_user_w_perms)

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.REDIRECT_TO_HOME_ON_404", False)
    def test__login_required__redirect_turned_off(self):
        """With the redirect off, anonymous users still go to the login page; logged-in users get a 404."""
        response, _messages = self._get()
        self.assertRedirects(response, self.login_url, fetch_redirect_response=False)

        response, _messages = self._get(user=self.test_user_w_perms)
        self.assertEqual(404, response.status_code)

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", ("/public/",))
    def test__login_required__public_path__home_requires_login(self):
        """An unknown url under a public prefix is redirected home, without the message, which would show on login."""
        self._assert_home_with_message(False, path="/public/missing/")

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", ("/public/",))
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_EXEMPT_WHITELIST + ["adminlte2_pdq:home"])
    def test__login_required__public_path__public_home(self):
        """An unknown url under a public prefix, with a public home page, is redirected home with the message."""
        self._assert_home_with_message(True, path="/public/missing/")

    @patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.middleware.HOME_ROUTE", "/no-such-home-page/")
    def test__home_requires_login__home_page_not_found(self):
        """A home route that doesn't resolve to a view is not treated as requiring login."""
        request = RequestFactory().get("/missing/")
        request.user = AnonymousUser()
        self.assertFalse(AuthMiddleware(lambda request: None).home_requires_login(request))
