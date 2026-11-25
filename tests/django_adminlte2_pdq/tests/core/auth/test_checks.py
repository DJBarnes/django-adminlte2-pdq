"""
Tests for the package's system checks.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.core import checks
from django.test import SimpleTestCase, override_settings

# Internal Imports.
from adminlte2_pdq.checks import _resolved_patterns, check_views_define_permissions
from tests.django_adminlte2_pdq.django_test_project import views


BROKEN_VIEWS = {
    "BleedingOnePermissionMissingPermissionsView",
    "BleedingFullPermissionMissingPermissionsView",
}


def _flagged_view_names(warnings):
    return {warning.obj.__name__ for warning in warnings}


class ViewsDefinePermissionsCheckTestCase(SimpleTestCase):
    """Tests for the adminlte2_pdq.W001 check."""

    def test__registered_automatically(self):
        """The check runs with Django's system checks, with no project setup."""
        warnings = checks.run_checks(tags=["adminlte2_pdq"])

        self.assertEqual(BROKEN_VIEWS, _flagged_view_names(warnings))
        self.assertEqual({"adminlte2_pdq.W001"}, {warning.id for warning in warnings})

    def test__loose_mode(self):
        """Only views that explicitly require permissions are checked."""
        self.assertEqual(BROKEN_VIEWS, _flagged_view_names(check_views_define_permissions(None)))

    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__strict_mode(self):
        """In strict mode, views without a decorator or mixin also need permissions, function and class based.

        Views exempt from permissions aren't listed: whitelisted views (such as the package's home, sample form,
        and demo pages), the Django admin, and redirect views. The test project's home and demo_css views are
        listed: their no-slash routes aren't in the whitelist.
        """
        warnings = check_views_define_permissions(None)

        self.assertEqual(
            BROKEN_VIEWS | {"StandardView", "standard_view", "home", "demo_css"}, _flagged_view_names(warnings)
        )
        # The package's own home and demo_css routes are whitelisted, so each view is listed once, for its test route.
        self.assertEqual(
            {"home": ["(/tests/home)"], "demo_css": ["(/tests/demo-css-no-slash)"]},
            {
                name: [warning.msg.split(" ")[4] for warning in warnings if warning.obj.__name__ == name]
                for name in ("home", "demo_css")
            },
        )

    @override_settings(
        MIDDLEWARE=[entry for entry in settings.MIDDLEWARE if entry != "adminlte2_pdq.middleware.AuthMiddleware"]
    )
    def test__middleware_not_installed(self):
        """Without AuthMiddleware the check does nothing."""
        self.assertEqual([], check_views_define_permissions(None))

    @patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
    def test__views_are_not_changed(self):
        """The check doesn't set admin_pdq_data on views, as the middleware does during requests."""
        had_data = "admin_pdq_data" in views.StandardView.__dict__
        check_views_define_permissions(None)

        self.assertEqual(had_data, "admin_pdq_data" in views.StandardView.__dict__)

    def test__other_url_entries_are_skipped(self):
        """URL list entries that are neither a URL pattern nor an include are skipped."""

        class OtherEntry:
            pattern = "other/"

        self.assertEqual(list(_resolved_patterns([OtherEntry()], "/", (), ())), [])
