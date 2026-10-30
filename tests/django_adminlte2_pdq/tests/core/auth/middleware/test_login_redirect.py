"""
Tests for AuthMiddleware's redirect to the login page.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.test import override_settings

# Internal Imports.
from .base_test_case import MiddlewareBaseTestCase


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class LoginRedirectTestCase(MiddlewareBaseTestCase):
    """The login redirect passes the requested path, including any query string, as "next"."""

    def test__next_is_the_requested_path(self):
        """The requested path is passed as "next"."""
        response = self.client.get("/demo-css/")

        self.assertRedirects(response, "/accounts/login/?next=/demo-css/", fetch_redirect_response=False)

    def test__next_includes_the_query_string(self):
        """The query string is passed as part of "next"."""
        response = self.client.get("/demo-css/?tab=1&sort=name")

        self.assertRedirects(
            response,
            "/accounts/login/?next=/demo-css/%3Ftab%3D1%26sort%3Dname",
            fetch_redirect_response=False,
        )

    @patch("adminlte2_pdq.middleware.LOGIN_URL", "login")
    def test__login_url_is_a_url_name(self):
        """A LOGIN_URL that is a url name is resolved to its path."""
        response = self.client.get("/demo-css/")

        self.assertRedirects(response, "/accounts/login/?next=/demo-css/", fetch_redirect_response=False)
