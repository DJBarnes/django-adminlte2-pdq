"""
Tests for AuthMiddleware when the project's MIDDLEWARE setting is incomplete.
"""

# Third-Party Imports.
import django
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.urls import reverse

# Internal Imports.
from .base_test_case import (
    MiddlewareBaseTestCase,
    NO_AUTH_MIDDLEWARE,
    NO_MESSAGES_MIDDLEWARE,
    NO_SESSION_AUTH_MIDDLEWARE,
    NO_SESSION_MIDDLEWARE,
)


class ConfigurationMiddlewareTestCase(MiddlewareBaseTestCase):
    """Test that the project is set up correctly to use PDQ"""

    @override_settings(MIDDLEWARE=NO_SESSION_MIDDLEWARE)
    def test__missing_session_middleware_raises_error(self):
        """Test that project with missing session middleware raises error"""
        # Before Django 4.0, Django's AuthenticationMiddleware checks for the session with an assert.
        if django.VERSION < (4, 0):
            with self.assertRaises(AssertionError):
                self.client.get(reverse("adminlte2_pdq:demo-css"))
        else:
            with self.assertRaises(ImproperlyConfigured):
                self.client.get(reverse("adminlte2_pdq:demo-css"))

    @override_settings(MIDDLEWARE=NO_AUTH_MIDDLEWARE)
    def test__missing_auth_middleware_raises_error(self):
        """Test that project with missing auth middleware raises error"""
        with self.assertRaises(ImproperlyConfigured):
            self.client.get(reverse("adminlte2_pdq:demo-css"))

    @override_settings(MIDDLEWARE=NO_MESSAGES_MIDDLEWARE)
    def test__missing_message_middleware_raises_error(self):
        """Test that project with missing message middleware raises error"""
        with self.assertRaises(ImproperlyConfigured):
            self.client.get(reverse("adminlte2_pdq:demo-css"))

    @override_settings(MIDDLEWARE=NO_SESSION_AUTH_MIDDLEWARE)
    def test__missing_session_and_auth_middleware_raises_error(self):
        """Test that project with missing session and auth middleware raises error"""
        with self.assertRaises(ImproperlyConfigured):
            self.client.get(reverse("adminlte2_pdq:demo-css"))
