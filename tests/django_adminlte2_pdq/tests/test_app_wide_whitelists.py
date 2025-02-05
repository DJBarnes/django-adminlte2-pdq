"""
Tests for the "app-wide" whitelist settings. Aka:
 * ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST
 * ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST
"""

# System Imports.
from unittest.mock import patch
from pytest import warns

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django_expanded_test_cases import IntegrationTestCase


# Module Variables.
UserModel = get_user_model()


@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
class Test_LoginRequiredMode_AppWideWhitelistSettings(IntegrationTestCase):
    """Test for project "app-wide" whitelist settings.

    For these tests, we only use the Anonymous user and the default user, without any modifications.
    All the work should be done by the whitelists.
    """

    LOGIN_EXEMPT_FUZZY_WHITELIST = ("/tests-2/",)
    STRICT_POLICY_FUZZY_WHITELIST_VIEWS = ("/tests-2/",)

    def test__ensure_views_cannot_be_accessed_without_settings(self):
        """Sanity check tests, to ensure these specific views cannot be accessed by default."""

        # Should fail and redirect to login for anyone unauthenticated.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

        # Should succeed and load as expected.
        with self.subTest("As default standard user"):
            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

    @override_settings(ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST)
    @override_settings(LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST)
    @patch("adminlte2_pdq.constants.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST)
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST)
    def test__verify_login_whitelist(self):
        """Tests to verify handling of "app-wide" login whitelist."""

        # Should succeed and load as expected.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

        # Should succeed and load as expected.
        with self.subTest("As default standard user"):
            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

    @override_settings(ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @override_settings(STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.constants.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    def test__verify_perm_whitelist(self):
        """Tests to verify handling of "app-wide" perm whitelist.
        In this case, should handle identical to no settings provided.
        """

        # Should fail and redirect to login for anyone unauthenticated.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

        # Should succeed and load as expected.
        with self.subTest("As default standard user"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

    @override_settings(ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST)
    @override_settings(LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST)
    @override_settings(ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @override_settings(STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.constants.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST)
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST)
    @patch("adminlte2_pdq.constants.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    def test__verify_both_whitelists(self):
        """Tests to verify handling of combined "app-wide" login and permission whitelists."""

        # Should succeed and load as expected.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

        # Should succeed and load as expected.
        with self.subTest("As default standard user"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )


@override_settings(ADMINLTE2_USE_LOGIN_REQUIRED=True)
@override_settings(LOGIN_REQUIRED=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch("adminlte2_pdq.constants.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class Test_StrictMode_AppWideWhitelistSettings(IntegrationTestCase):
    """Test for project "app-wide" whitelist settings.

    For these tests, we only use the Anonymous user and the default user, without any modifications.
    All the work should be done by the whitelists.
    """

    LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS = ("/tests-2/",)
    STRICT_POLICY_FUZZY_WHITELIST_VIEWS = ("/tests-2/",)

    def test__ensure_views_cannot_be_accessed_without_settings(self):
        """Sanity check tests, to ensure these specific views cannot be accessed by default."""

        # Should fail and redirect to login for anyone unauthenticated.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

        # Should fail and redirect to home.
        with self.subTest("As default standard user"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_content=[
                    "Monthly Recap Report",
                    "Visitors Report",
                    "Inventory",
                    "Downloads",
                ],
            )

    @override_settings(ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @override_settings(LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.constants.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    def test__verify_login_whitelist(self):
        """Tests to verify handling of "app-wide" login whitelist."""

        # Should fail and redirect to home.
        with self.subTest("As Anonymous User"):
            with warns(Warning) as warning_info:

                # Should fail and redirect to home. But then home requires login so it still redirects to login.
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests_2:standard-1",
                    user=AnonymousUser(),
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Login |",
                    expected_content=[
                        "Sign in to start your session",
                        "Remember Me",
                        "I forgot my password",
                    ],
                )

        # Should fail and redirect to home.
        with self.subTest("As default standard user"):
            with warns(Warning) as warning_info:

                # Verify we get the expected page.
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests_2:standard-1",
                    user=self.test_user,
                    # Expected view return data.
                    expected_status=200,
                    view_should_redirect=True,
                    # Expected content on page.
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=[
                        "Monthly Recap Report",
                        "Visitors Report",
                        "Inventory",
                        "Downloads",
                    ],
                )

    @override_settings(ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @override_settings(STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.constants.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    def test__verify_perm_whitelist(self):
        """Tests to verify handling of "app-wide" perm whitelist."""

        # Should fail and redirect to login for anyone unauthenticated.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=True,
                # Expected content on page.
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

        # Should succeed and load as expected.
        with self.subTest("As default standard user"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

    @override_settings(ADMINLTE2_LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @override_settings(LOGIN_EXEMPT_FUZZY_WHITELIST=LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @override_settings(ADMINLTE2_STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @override_settings(STRICT_POLICY_FUZZY_WHITELIST=STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.constants.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.constants.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    def test__verify_both_whitelists(self):
        """Tests to verify handling of combined "app-wide" login and permission whitelists."""

        # Should succeed and load as expected.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=AnonymousUser(),
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )

        # Should succeed and load as expected.
        with self.subTest("As default standard user"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_2:standard-1",
                user=self.test_user,
                # Expected view return data.
                expected_status=200,
                view_should_redirect=False,
                # Expected content on page.
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    "Django AdminLtePdq | Standard View Subheader",
                    "Django AdminLtePdq | Standard View Content",
                ],
            )
