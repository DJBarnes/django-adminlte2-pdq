"""
Tests for AuthMiddleware's redirect to the login page.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.messages import get_messages
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST
from adminlte2_pdq.middleware import RESPONSE_403_DEBUG_MESSAGE
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


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch(
    "adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST",
    LOGIN_EXEMPT_WHITELIST + ["adminlte2_pdq_tests:function-one-permission-required"],
)
class FailedPermissionLoginRedirectTestCase(MiddlewareBaseTestCase):
    """Anonymous users who fail a permission check on a login whitelisted view are sent to the login page."""

    def test__anonymous_user(self):
        """The login redirect passes the view as "next", and adds no failed permissions message."""
        # The view is login whitelisted but requires permissions, so the middleware warns.
        with self.assertWarns(RuntimeWarning):
            response = self.client.get("/tests/function/one_permission/")

        self.assertRedirects(
            response, "/accounts/login/?next=/tests/function/one_permission/", fetch_redirect_response=False
        )
        failed_permissions_message = RESPONSE_403_DEBUG_MESSAGE.format(
            view_type="function-based", view_name="one_permission_required_view"
        )
        messages = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertNotIn(failed_permissions_message, messages)

    def test__logged_in_user(self):
        """A logged-in user without the permissions is still redirected home."""
        self.client.force_login(self.test_user_no_perms)

        with self.assertWarns(RuntimeWarning):
            response = self.client.get("/tests/function/one_permission/")

        self.assertRedirects(response, reverse("adminlte2_pdq:home"), fetch_redirect_response=False)
