"""
Base test case for the AuthMiddleware tests.
"""

# System Imports.
from copy import copy

# Third-Party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase

# Internal Imports.


# Module Variables.
UserModel = get_user_model()  # pylint: disable=invalid-name

NO_SESSION_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_SESSION_MIDDLEWARE.remove("django.contrib.sessions.middleware.SessionMiddleware")
NO_AUTH_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_AUTH_MIDDLEWARE.remove("django.contrib.auth.middleware.AuthenticationMiddleware")
NO_MESSAGES_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_MESSAGES_MIDDLEWARE.remove("django.contrib.messages.middleware.MessageMiddleware")

NO_SESSION_AUTH_MIDDLEWARE = copy(settings.MIDDLEWARE)
NO_SESSION_AUTH_MIDDLEWARE.remove("django.contrib.sessions.middleware.SessionMiddleware")
NO_SESSION_AUTH_MIDDLEWARE.remove("django.contrib.auth.middleware.AuthenticationMiddleware")


class MiddlewareBaseTestCase(TestCase):
    """Setup class for Middleware TestCases."""

    # region Expected Test Messages

    pdq_strict__no_permissions_set_message = (
        "AdminLtePdq Warning: The class-based view 'StandardView' has permission requirements, "
        "but does not have any permissions set. This means that this view is inaccessible until "
        "permissions are set for the view.\n\n\nFor further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )

    # endregion Expected Test Messages

    def setUp(self):

        self.test_user_no_perms = UserModel()
        self.test_user_no_perms.username = "test_user_no_perms"
        self.test_user_no_perms.set_password("password")
        self.test_user_no_perms.save()

        self.test_user_w_perms = UserModel()
        self.test_user_w_perms.username = "test_user_w_perms"
        self.test_user_w_perms.set_password("password")
        self.test_user_w_perms.save()

        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            self.test_user_w_perms.user_permissions.add(permission)
