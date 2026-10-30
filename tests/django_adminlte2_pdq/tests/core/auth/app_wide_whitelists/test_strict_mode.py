"""
Tests for the "app-wide" whitelist settings in strict mode.
"""

# System Imports.
from unittest.mock import patch
from pytest import warns

# Third-Party Imports.
from django.contrib.auth.models import AnonymousUser
from django_expanded_test_cases import IntegrationTestCase


# Module Variables.


@patch("adminlte2_pdq.middleware.LOGIN_REQUIRED", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class StrictModeWhitelistTestCase(IntegrationTestCase):
    """Test for project "app-wide" whitelist settings.

    For these tests, we only use the Anonymous user and the default user, without any modifications.
    All the work should be done by the whitelists.
    """

    LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS = ("/tests-fuzzy/",)
    STRICT_POLICY_FUZZY_WHITELIST_VIEWS = ("/tests-fuzzy/",)

    def test__ensure_views_cannot_be_accessed_without_settings(self):
        """Sanity check tests, to ensure these specific views cannot be accessed by default."""

        # Should fail and redirect to login for anyone unauthenticated.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_fuzzy:standard-1",
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
                "adminlte2_pdq_tests_fuzzy:standard-1",
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

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    def test__verify_login_whitelist(self):
        """Tests to verify handling of "app-wide" login whitelist."""

        # Should fail and redirect to home.
        with self.subTest("As Anonymous User"):
            with warns(Warning) as _warning_info:

                # Should fail and redirect to home. But then home requires login so it still redirects to login.
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests_fuzzy:standard-1",
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
            with warns(Warning) as _warning_info:

                # Verify we get the expected page.
                self.assertGetResponse(
                    # View setup.
                    "adminlte2_pdq_tests_fuzzy:standard-1",
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

    @patch("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    def test__verify_perm_whitelist(self):
        """Tests to verify handling of "app-wide" perm whitelist."""

        # Should fail and redirect to login for anyone unauthenticated.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_fuzzy:standard-1",
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
                "adminlte2_pdq_tests_fuzzy:standard-1",
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

    @patch("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", LOGIN_EXEMPT_FUZZY_WHITELIST_VIEWS)
    @patch("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", STRICT_POLICY_FUZZY_WHITELIST_VIEWS)
    def test__verify_both_whitelists(self):
        """Tests to verify handling of combined "app-wide" login and permission whitelists."""

        # Should succeed and load as expected.
        with self.subTest("As Anonymous User"):

            # Verify we get the expected page.
            self.assertGetResponse(
                # View setup.
                "adminlte2_pdq_tests_fuzzy:standard-1",
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
                "adminlte2_pdq_tests_fuzzy:standard-1",
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
