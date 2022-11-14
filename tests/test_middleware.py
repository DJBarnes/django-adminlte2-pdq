"""
Tests for Middleware
"""

import warnings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST

UserModel = get_user_model()  # pylint: disable=invalid-name

UPDATED_LOGIN_EXEMPT_WHITELIST = LOGIN_EXEMPT_WHITELIST + ['adminlte2_pdq:demo-css']
UPDATED_STRICT_POLICY_WHITELIST = STRICT_POLICY_WHITELIST + ['adminlte2_pdq:demo-css']

class MiddlewareTestCase(TestCase):
    """
    Test Middleware
    """

    # |-------------------------------------------------------------------------
    # | Setup
    # |-------------------------------------------------------------------------
    def setUp(self):
        self.test_anonymous_user = AnonymousUser()

        self.test_user_w_perms = UserModel()
        self.test_user_w_perms.username = "test_user_w_perms"
        self.test_user_w_perms.set_password('password')
        self.test_user_w_perms.save()

        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            self.test_user_w_perms.user_permissions.add(permission)

    # |-------------------------------------------------------------------------
    # | Test middleware works as intended
    # |-------------------------------------------------------------------------

    # Test format is as follows:
    # def test_middleware_{result}_{user}_{login}_{strict}_{login_WL}_{strict_WL}

    # Additional details
    # {login} means that the LOGIN_REQUIRED middleware is active.
    # {strict} means that the STRICT_POLICY middleware is active.
    # {login_WL} means that the node's route is listed in the LOGIN_EXEMPT_WHITELIST - omitted means it isn't.
    # {strict_WL} means that the node's route is listed in the STRICT_POLICY_WHITELIST - omitted means it isn't.

    # **************************************************************************
    # Anonymous User
    # **************************************************************************

    def test_middleware_allows_when_user_anonymous_login_off_strict_off_login_wl_off_strict_wl_off(self):
        """test_middleware_allows_when_user_anonymous_login_off_strict_off_login_wl_off_strict_wl_off"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    def test_middleware_blocks_when_user_anonymous_login_on_strict_off_login_wl_off_strict_wl_off(self):
        """test_middleware_blocks_when_user_anonymous_login_on_strict_off_login_wl_off_strict_wl_off"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST', UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test_middleware_allows_when_user_anonymous_login_on_strict_off_login_wl_on_strict_wl_off(self):
        """test_middleware_allows_when_user_anonymous_login_on_strict_off_login_wl_on_strict_wl_off"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    def test_middleware_blocks_when_user_anonymous_login_off_strict_on_login_wl_off_strict_wl_off(self):
        """test_middleware_blocks_when_user_anonymous_login_off_strict_on_login_wl_off_strict_wl_off"""
        with warnings.catch_warnings(record=True) as wa:
            warning_message = (
                "The function-based view 'demo_css' does not have the"
                " permission_required, one_of_permission, or login_required"
                " decorator set and the option ADMINLTE2_USE_STRICT_POLICY is"
                " set to True. This means that this view is inaccessible until"
                " either permissions are set on the view or the url_name for the"
                " view is added to the ADMINLTE2_STRICT_POLICY_WHITELIST setting."
            )

            response = self.client.get(
                reverse('adminlte2_pdq:demo-css'),
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")
            self.assertEqual(len(wa), 1)
            self.assertIn(warning_message, str(wa[-1].message))

    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST', UPDATED_STRICT_POLICY_WHITELIST)
    def test_middleware_allows_when_user_anonymous_login_off_strict_on_login_wl_off_strict_wl_on(self):
        """test_middleware_allows_when_user_anonymous_login_off_strict_on_login_wl_off_strict_wl_on"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    def test_middleware_blocks_when_user_anonymous_login_on_strict_on_login_wl_off_strict_wl_off(self):
        """test_middleware_blocks_when_user_anonymous_login_on_strict_on_login_wl_off_strict_wl_off"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST', UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test_middleware_blocks_when_user_anonymous_login_on_strict_on_login_wl_on_strict_wl_off(self):
        """test_middleware_blocks_when_user_anonymous_login_on_strict_on_login_wl_on_strict_wl_off"""
        # NOTE: This test goes to demo-css, fails the strict policy, then goes to home.
        # Home is a new request that fails the login required being on and thus redirect to login page.
        with warnings.catch_warnings(record=True) as wa:
            warning_message = (
                "The function-based view 'demo_css' does not have the"
                " permission_required, one_of_permission, or login_required"
                " decorator set and the option ADMINLTE2_USE_STRICT_POLICY is"
                " set to True. This means that this view is inaccessible until"
                " either permissions are set on the view or the url_name for the"
                " view is added to the ADMINLTE2_STRICT_POLICY_WHITELIST setting."
            )

            response = self.client.get(
                reverse('adminlte2_pdq:demo-css'),
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertEqual(len(wa), 1)
            self.assertIn(warning_message, str(wa[-1].message))

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST', UPDATED_STRICT_POLICY_WHITELIST)
    def test_middleware_blocks_when_user_anonymous_login_on_strict_on_login_wl_off_strict_wl_on(self):
        """test_middleware_allows_when_user_anonymous_login_on_strict_on_login_wl_off_strict_wl_on"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST', UPDATED_LOGIN_EXEMPT_WHITELIST)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST', UPDATED_STRICT_POLICY_WHITELIST)
    def test_middleware_allows_when_user_anonymous_login_on_strict_on_login_wl_on_strict_wl_on(self):
        """test_middleware_allows_when_user_anonymous_login_on_strict_on_login_wl_on_strict_wl_on"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")


    # **************************************************************************
    # Logged In User - All Perms
    # **************************************************************************

    def test_middleware_allows_when_user_logged_in_login_off_strict_off_login_wl_off_strict_wl_off(self):
        """test_middleware_allows_when_user_logged_in_login_off_strict_off_login_wl_off_strict_wl_off"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    def test_middleware_allows_when_user_logged_in_login_on_strict_off_login_wl_off_strict_wl_off(self):
        """test_middleware_blocks_when_user_logged_in_login_on_strict_off_login_wl_off_strict_wl_off"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST', UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test_middleware_allows_when_user_logged_in_login_on_strict_off_login_wl_on_strict_wl_off(self):
        """test_middleware_allows_when_user_logged_in_login_on_strict_off_login_wl_on_strict_wl_off"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    def test_middleware_blocks_when_user_logged_in_login_off_strict_on_login_wl_off_strict_wl_off(self):
        """test_middleware_blocks_when_user_logged_in_login_off_strict_on_login_wl_off_strict_wl_off"""
        with warnings.catch_warnings(record=True) as wa:
            self.client.force_login(self.test_user_w_perms)
            warning_message = (
                "The function-based view 'demo_css' does not have the"
                " permission_required, one_of_permission, or login_required"
                " decorator set and the option ADMINLTE2_USE_STRICT_POLICY is"
                " set to True. This means that this view is inaccessible until"
                " either permissions are set on the view or the url_name for the"
                " view is added to the ADMINLTE2_STRICT_POLICY_WHITELIST setting."
            )

            response = self.client.get(
                reverse('adminlte2_pdq:demo-css'),
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")
            self.assertEqual(len(wa), 1)
            self.assertIn(warning_message, str(wa[-1].message))

    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST', UPDATED_STRICT_POLICY_WHITELIST)
    def test_middleware_allows_when_user_logged_in_login_off_strict_on_login_wl_off_strict_wl_on(self):
        """test_middleware_allows_when_user_logged_in_login_off_strict_on_login_wl_off_strict_wl_on"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    def test_middleware_blocks_when_user_logged_in_login_on_strict_on_login_wl_off_strict_wl_off(self):
        """test_middleware_blocks_when_user_logged_in_login_on_strict_on_login_wl_off_strict_wl_off"""
        with warnings.catch_warnings(record=True) as wa:
            self.client.force_login(self.test_user_w_perms)
            warning_message = (
                "The function-based view 'demo_css' does not have the"
                " permission_required, one_of_permission, or login_required"
                " decorator set and the option ADMINLTE2_USE_STRICT_POLICY is"
                " set to True. This means that this view is inaccessible until"
                " either permissions are set on the view or the url_name for the"
                " view is added to the ADMINLTE2_STRICT_POLICY_WHITELIST setting."
            )

            response = self.client.get(
                reverse('adminlte2_pdq:demo-css'),
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")
            self.assertEqual(len(wa), 1)
            self.assertIn(warning_message, str(wa[-1].message))

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST', UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test_middleware_blocks_when_user_logged_in_login_on_strict_on_login_wl_on_strict_wl_off(self):
        """test_middleware_blocks_when_user_logged_in_login_on_strict_on_login_wl_on_strict_wl_off"""
        with warnings.catch_warnings(record=True) as wa:
            self.client.force_login(self.test_user_w_perms)
            warning_message = (
                "The function-based view 'demo_css' does not have the"
                " permission_required, one_of_permission, or login_required"
                " decorator set and the option ADMINLTE2_USE_STRICT_POLICY is"
                " set to True. This means that this view is inaccessible until"
                " either permissions are set on the view or the url_name for the"
                " view is added to the ADMINLTE2_STRICT_POLICY_WHITELIST setting."
            )

            response = self.client.get(
                reverse('adminlte2_pdq:demo-css'),
                follow=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")
            self.assertEqual(len(wa), 1)
            self.assertIn(warning_message, str(wa[-1].message))

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST', UPDATED_STRICT_POLICY_WHITELIST)
    def test_middleware_allows_when_user_logged_in_login_on_strict_on_login_wl_off_strict_wl_on(self):
        """test_middleware_allows_when_user_logged_in_login_on_strict_on_login_wl_off_strict_wl_on"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST', UPDATED_LOGIN_EXEMPT_WHITELIST)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST', UPDATED_STRICT_POLICY_WHITELIST)
    def test_middleware_allows_when_user_logged_in_login_on_strict_on_login_wl_on_strict_wl_on(self):
        """test_middleware_allows_when_user_logged_in_login_on_strict_on_login_wl_on_strict_wl_on"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    @patch('adminlte2_pdq.middleware.MEDIA_ROUTE', '/demo-css/')  # Pretend the demo-css route is a media file.
    def test_middleware_allows_when_media_url_defined_login_on_strict_on_login_wl_on_strict_wl_on(self):
        """test_middleware_allows_when_media_url_defined_login_on_strict_on_login_wl_on_strict_wl_on"""
        response = self.client.get(
            reverse('adminlte2_pdq:demo-css'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Demo CSS</h1>")

    # **************************************************************************
    # Logged In User - All Perms - Staff Status - Can see Admin page.
    # **************************************************************************

    @patch('adminlte2_pdq.middleware.LOGIN_REQUIRED', True)
    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    def test_middleware_allows_admin_when_user_logged_in_login_on_strict_on_login_wl_on_strict_wl_on(self):
        """test_middleware_allows_admin_when_user_logged_in_login_on_strict_on_login_wl_on_strict_wl_on"""
        self.test_user_w_perms.is_staff = True
        self.test_user_w_perms.save()
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            reverse('admin:auth_user_changelist'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select user to change")

    # **************************************************************************
    # Logged In User - All Perms - Visiting 404
    # **************************************************************************

    @patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
    def test_middleware_blocks_when_user_logged_in_login_off_strict_on_login_wl_off_strict_wl_off_route_unknown(self):
        """test_middleware_blocks_when_user_logged_in_login_off_strict_on_login_wl_off_strict_wl_off_route_unknown"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(
            'unknown/route/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")
