"""
Tests for AuthMiddleware when the project's MIDDLEWARE setting is incomplete.
"""

# System Imports.
from copy import copy

# Third-Party Imports.
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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
