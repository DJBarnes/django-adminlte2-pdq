"""
Tests for the routes AuthMiddleware doesn't check: media, websocket, and admin pages.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from .base_test_case import MiddlewareBaseTestCase


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class SkippedRoutesTestCase(MiddlewareBaseTestCase):
    """In strict mode, anonymous users can open media and websocket routes, but those routes can't be the site root."""

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/demo-css/")  # Pretend the demo-css route is a media file.
    def test__media_route(self):
        """A url under the media route loads without login."""
        response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/")  # Pretend the root url is a media file.
    def test__media_route_at_site_root(self):
        """A media route of "/" is ignored, so it can't skip the login check for the whole site."""
        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    @patch("adminlte2_pdq.middleware.WEBSOCKET_ROUTE", "/demo-css/")  # Pretend the demo-css route is a websocket.
    def test__websocket_route(self):
        """A url under the websocket route loads without login."""
        response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")

    @patch("adminlte2_pdq.middleware.WEBSOCKET_ROUTE", "/")  # Pretend the root url is a websocket.
    def test__websocket_route_at_site_root(self):
        """A websocket route of "/" is ignored, so it can't skip the login check for the whole site."""
        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test__admin_page(self):
        """Admin pages don't need the package's decorators or mixins; Django's admin checks its own permissions."""
        self.test_user_w_perms.is_staff = True
        self.test_user_w_perms.save()
        self.client.force_login(self.test_user_w_perms)

        response = self.client.get(reverse("admin:auth_user_changelist"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select user to change")
