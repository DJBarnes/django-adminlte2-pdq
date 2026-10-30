"""
Tests for AuthMiddleware's handling of failed permission checks (403s) in strict mode.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.messages import get_messages
from django.test import override_settings
from django.urls import reverse
from pytest import warns

# Internal Imports.
from adminlte2_pdq.middleware import RESPONSE_403_PRODUCTION_MESSAGE
from .base_test_case import MiddlewareBaseTestCase


# Module Variables.
SERVE_403_FUZZY_WHITELIST = ("/tests/",)


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class StrictMode403HandlingTestCase(MiddlewareBaseTestCase):
    """Test the 403 handling in strict mode."""

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


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY_SERVE_403_FUZZY_WHITELIST", SERVE_403_FUZZY_WHITELIST)
@patch("adminlte2_pdq.mixins.STRICT_POLICY_SERVE_403_FUZZY_WHITELIST", SERVE_403_FUZZY_WHITELIST)
class Serve403FuzzyWhitelistTestCase(MiddlewareBaseTestCase):
    """Urls in the serve-403 fuzzy whitelist get a 403 response instead of a redirect home."""

    def test__anonymous_user(self):
        """Anonymous users still go to the login page."""
        response = self.client.get(
            reverse("adminlte2_pdq_tests:class-full-permissions-required-as-string"), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test__user_without_permissions(self):
        """A user without the view's permissions gets a 403."""
        self.client.force_login(self.test_user_no_perms)

        response = self.client.get(
            reverse("adminlte2_pdq_tests:class-full-permissions-required-as-string"), follow=True
        )

        self.assertEqual(response.status_code, 403)

    def test__view_without_permissions(self):
        """A view with permission requirements but no permissions set gets a 403, with a warning."""
        self.client.force_login(self.test_user_no_perms)

        with warns(Warning) as warning_info:
            response = self.client.get(reverse("adminlte2_pdq_tests:class-standard"), follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            {(RuntimeWarning, self.pdq_strict__no_permissions_set_message)},
            {(warn.category, warn.message.args[0]) for warn in warning_info},
        )
