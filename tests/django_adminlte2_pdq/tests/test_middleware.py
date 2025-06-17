"""
Tests for Middleware
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Permission
from django.test import override_settings, TestCase
from django.urls import reverse
from pytest import warns

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST


# Module Variables.
UserModel = get_user_model()  # pylint: disable=invalid-name
UPDATED_LOGIN_EXEMPT_WHITELIST = LOGIN_EXEMPT_WHITELIST + ["adminlte2_pdq:demo-css"]
UPDATED_STRICT_POLICY_WHITELIST = STRICT_POLICY_WHITELIST + ["adminlte2_pdq:demo-css"]


class MiddlewareBaseTestCase(TestCase):
    """Setup class for Middleware TestCases."""

    # region Expected Test Messages

    pdq_strict__no_decorator_message = (
        "AdminLtePdq Warning: This project is set to run in strict mode, and "
        "the function-based view 'demo_css' does not have any decorators set. "
        "This means that this view is inaccessible until permission decorators "
        "are set for the view, or the view is added to the "
        "ADMINLTE2_STRICT_POLICY_WHITELIST setting."
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )

    pdq_strict__ineffective_login_whitelist_message = (
        "AdminLtePdq Warning: The function-based view 'demo_css' is login whitelisted, "
        "but the view still requires permissions. A user must login to have permissions, so the login whitelist is "
        "redundant and probably not achieving the desired effect. Correct this by adding the view to "
        "the permission whitelist setting (ADMINLTE2_STRICT_POLICY_WHITELIST), or by adding the "
        "'allow_without_permissions' decorator."
    )

    # endregion Expected Test Messages

    def setUp(self):
        self.test_anonymous_user = AnonymousUser()

        self.test_user_w_perms = UserModel()
        self.test_user_w_perms.username = "test_user_w_perms"
        self.test_user_w_perms.set_password("password")
        self.test_user_w_perms.save()

        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            self.test_user_w_perms.user_permissions.add(permission)


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
            self.assertContains(response, "<h1>Demo CSS</h1>")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")


@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class LoginRequiredMiddlewareTestCase(MiddlewareBaseTestCase):
    """Test Middleware handling when in "LOGIN_REQUIRED" authentication mode."""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify values imported from middleware file.
        # We don't use constants.py values because the above settings technically don't override such.
        # Plus this test is a middleware test so it's probably fine.
        # pylint:disable=redefined-outer-name reimported import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_whitelists(self):
        """Test when "LOGIN_REQUIRED" mode and no whitelists set."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test__with_login_whitelist(self):
        """Test when "LOGIN_REQUIRED" mode and login whitelist is set."""

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")


@override_settings(DEBUG=True)
@override_settings(APPEND_SLASH=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class MiddlewareUrlProcessingTestCaseAppendSlashTrue(MiddlewareBaseTestCase):
    """Test Middleware URL Processing with the APPEND_SLASH setting set to True"""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify values imported from middleware file.
        # We don't use constants.py values because the above settings technically don't override such.
        # Plus this test is a middleware test so it's probably fine.
        # pylint:disable=redefined-outer-name reimported import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))
        self.assertTrue(settings.APPEND_SLASH)

    def test__trailing_slash__with_valid_url(self):
        """Tests handling of trailing url slashes with valid urls, when APPEND_SLASH is True."""

        with self.subTest("Processing url with a trailing slash"):
            # Should handle as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq:demo-css")

            # Verify url ends with slash.
            self.assertEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

            # Verify expected final url.
            self.assertEqual(url, response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then proceed as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq:demo-css")[:-1]

            # Verify url does NOT end with slash.
            self.assertNotEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS")

            # Verify expected final url.
            self.assertEqual(url + "/", response.request["PATH_INFO"])

    def test__trailing_slash__with_invalid_url(self):
        """Tests handling of trailing url slashes with bad urls, when APPEND_SLASH is True."""

        with self.subTest("Processing url with a trailing slash"):
            # Process response.
            response = self.client.get("/invalid-url/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then redirect to login.

            # Process response.
            response = self.client.get("/invalid-url", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])


@override_settings(DEBUG=True)
@override_settings(APPEND_SLASH=False)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class MiddlewareUrlProcessingTestCaseAppendSlashFalse(MiddlewareBaseTestCase):
    """Test Middleware URL Processing with the APPEND_SLASH setting set to False"""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify values imported from middleware file.
        # We don't use constants.py values because the above settings technically don't override such.
        # Plus this test is a middleware test so it's probably fine.
        # pylint:disable=redefined-outer-name reimported import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))
        self.assertFalse(settings.APPEND_SLASH)

    def test__trailing_slash__with_valid_url(self):
        """Tests handling of trailing url slashes with valid urls, when APPEND_SLASH is False."""

        # NOTE: The APPEND_SLASH settings does just that, it will append a slash if it is missing
        # and the setting is set to True. It will NOT however remove any slashes.
        # So, if APPEND_SLASH is False and the URL is defined as "/foobar", when the user tries to
        # visit "/foobar/", Django will NOT remove the slash to make it "match". Thus the user should
        # get a 404 that causes a redirect to the Home route with the 404 message.

        with self.subTest("Processing url with a trailing slash"):
            # Should auto-magically remove the trailing slash, and then proceed as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq_tests:demo-css-no-slash") + "/"

            # Verify url ends with slash.
            self.assertEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request["PATH_INFO"], reverse("adminlte2_pdq:home"))
            self.assertContains(response, "Dashboard")
            self.assertContains(response, "The page you were looking for does not exist")

        with self.subTest("Processing url without a trailing slash"):
            # Should handle as normal.

            # Get actual url.
            url = reverse("adminlte2_pdq_tests:demo-css-no-slash")

            # Verify url does NOT end with slash.
            self.assertNotEqual(str(url)[-1], "/")

            # Process response. Should succeed and load as expected.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(url, follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

            # Verify expected final url.
            self.assertEqual(url, response.request["PATH_INFO"])

    def test__trailing_slash__with_invalid_url(self):
        """Tests handling of trailing url slashes with bad urls, when APPEND_SLASH is False."""

        # NOTE: Even though we are testing with AppendSlash set to False, the login
        # route is defined with a trailing slash. So, when we fail with an invalid url
        # we will get redirected to a URL that has a trailing slash (login).

        with self.subTest("Processing url with a trailing slash"):
            # Process response.
            response = self.client.get("invalid-url/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])

        with self.subTest("Processing url without a trailing slash"):
            # Should auto-magically add the trailing slash, and then redirect to login.
            # Process response.
            response = self.client.get("/invalid-url", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")
            self.assertContains(response, "Remember Me")

            # Verify expected final url.
            self.assertEqual("/accounts/login/", response.request["PATH_INFO"])


# TODO: Even though the value in constants should always set LOGIN_REQUIRED = True when in STRICT mode,
#       this patch doesn't seem to. Not sure if there's a better way to handle overriding the settings.
@override_settings(DEBUG=True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class StrictMiddlewareTestCase(MiddlewareBaseTestCase):
    """Test Middleware handling when in "STRICT" authentication mode."""

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify values imported from middleware file.
        # We don't use constants.py values because the above settings technically don't override such.
        # Plus this test is a middleware test so it's probably fine.
        # pylint:disable=redefined-outer-name reimported import-outside-toplevel
        from adminlte2_pdq.middleware import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertTrue(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_whitelists(self):
        """Test when "STRICT" mode and no whitelist is set."""

        with self.subTest("As anonymous user"):
            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

        with self.subTest("As user with full permissions"):
            with warns(Warning) as warning_info:
                # Process response.
                self.client.force_login(self.test_user_w_perms)
                response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_strict__no_decorator_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

    def test__no_whitelists__admin_page(self):
        """Test when "STRICT" mode and accessing the admin page."""

        with self.subTest("As user with full permissions"):
            # Process response.
            self.test_user_w_perms.is_staff = True
            self.test_user_w_perms.save()

            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("admin:auth_user_changelist"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Select user to change")

    def test__no_whitelists__unknown_page(self):
        """Test when "STRICT" mode and accessing a "bad" url."""

        with self.subTest("As user with full permissions"):
            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get("unknown/route/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Home")

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", UPDATED_LOGIN_EXEMPT_WHITELIST)
    def test__with_login_whitelist(self):
        """Test when "STRICT" mode and login whitelist is set."""

        with self.subTest("As anonymous user"):
            # Should go to demo-css, fails the strict policy, then go to home.
            # Home is a new request that fails the login required being on and thus redirect to login page.
            with warns(Warning) as warning_info:
                # Process response.
                response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)
                self.assertEqual(response.status_code, 200)

                # Verify values associated with returned view.
                self.assertContains(response, "Login")

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_strict__no_decorator_message),
                (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

        with self.subTest("As user with full permissions"):
            # Should go to demo-css, fail the strict policy, then go to home.
            # Home is a new request that succeeds.
            with warns(Warning) as warning_info:
                self.client.force_login(self.test_user_w_perms)

                # Process response.
                response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)
                self.assertEqual(response.status_code, 200)

            # Verify values associated with returned view.
            self.assertContains(response, "Home")

            # Collect actual warnings that occurred.
            actual_warns = {(warn.category, warn.message.args[0]) for warn in warning_info}
            # Define expected warnings that should have occurred.
            expected_warns = {
                (RuntimeWarning, self.pdq_strict__no_decorator_message),
                (RuntimeWarning, self.pdq_strict__ineffective_login_whitelist_message),
            }
            # Assert warnings match.
            self.assertEqual(expected_warns, actual_warns)

    @patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", UPDATED_STRICT_POLICY_WHITELIST)
    def test__with_permission_whitelist(self):
        """Test when "STRICT" mode and permission whitelist is set."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", UPDATED_LOGIN_EXEMPT_WHITELIST)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", UPDATED_STRICT_POLICY_WHITELIST)
    def test__with_both_whitelists(self):
        """Test when "STRICT" mode and both whitelists are set."""

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            # Process response.
            self.client.force_login(self.test_user_w_perms)
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/")  # Pretend the root url is a media file.
    def test__no_whitelists_and_home_page_is_media_route(self):
        """Test no white lists and home page is media route"""
        # MEDIA_URL should not be allowed to be the root of a website, thus can not skip the login required check.

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get("/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

    @patch("adminlte2_pdq.middleware.MEDIA_ROUTE", "/demo-css/")  # Pretend the demo-css route is a media file.
    def test__no_whitelists_and_misc_page_is_media_route(self):
        """Test no white lists and misc page is media route"""

        with self.subTest("As anonymous user"):
            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")

    @patch("adminlte2_pdq.middleware.WEBSOCKET_ROUTE", "/")  # Pretend the root url is a websocket file.
    def test__no_whitelists_and_home_page_is_websocket_route(self):
        """Test no white lists and home page is websocket route"""
        # WEBSOCKET_URL should not be allowed to be the root of a website, thus can not skip the login required check.

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            # Process response.
            response = self.client.get("/", follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Login")

    @patch("adminlte2_pdq.middleware.WEBSOCKET_ROUTE", "/demo-css/")  # Pretend the demo-css route is a websocket file.
    def test__no_whitelists_and_misc_page_is_websocket_route(self):
        """Test no white lists and misc page is websocket route"""

        with self.subTest("As anonymous user"):
            # Process response.
            response = self.client.get(reverse("adminlte2_pdq:demo-css"), follow=True)

            # Verify values associated with returned view.
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<h1>Demo CSS</h1>")
