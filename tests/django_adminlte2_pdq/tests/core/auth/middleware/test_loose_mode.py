"""
Tests for AuthMiddleware in loose mode.
"""

# System Imports.
from copy import copy

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
class StandardMiddlewareTestCase(MiddlewareBaseTestCase):
    """Test Middleware handling when in "LOOSE" authentication mode."""

    def test__no_whitelists(self):
        """Test when "loose" mode and no whitelists set."""

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
