"""
Tests for Mixins
"""

# System Imports.

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.views import View
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST
from adminlte2_pdq.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Module Variables.
UserModel = get_user_model()
WHITELIST_VIEWS = [
    "adminlte2_pdq_tests:class-standard",
    "adminlte2_pdq_tests:class-allow-anonymous-access",
    "adminlte2_pdq_tests:class-login-required",
    "adminlte2_pdq_tests:class-allow-without-permissions",
    "adminlte2_pdq_tests:class-one-permission-required",
    "adminlte2_pdq_tests:class-full-permissions-required",
]
LOGIN_WHITELIST_VIEWS = LOGIN_EXEMPT_WHITELIST + WHITELIST_VIEWS
PERM_WHITELIST_VIEWS = STRICT_POLICY_WHITELIST + WHITELIST_VIEWS


class TestIsolatedMixins(TestCase):
    """Test logic that DOES NOT seem to touch/trigger middleware.

    Thus, this  tests Mixin logic for projects that do not have the package middleware enabled.
    """

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        Permission.objects.create(
            name="add_foo",
            codename="add_foo",
            content_type=self.permission_content_type,
        )
        Permission.objects.create(
            name="change_foo",
            codename="change_foo",
            content_type=self.permission_content_type,
        )
        # Add permissions auth.add_foo and auth.change_foo to full_user
        full_perms = Permission.objects.filter(codename__in=("add_foo", "change_foo"))
        self.user = UserModel.objects.create(username="john", password="qwerty")
        self.full_user = UserModel.objects.create(username="johnfull", password="qwerty")
        self.full_user.user_permissions.add(*full_perms)

        self.anonymous_user = AnonymousUser()

    # region Allow Anonymous Tests

    # endregion Allow Anonymous Tests

    # region Login Required Tests

    def test_login_required_mixin_works(self):
        """Test login_required mixin works"""

        class TestView(LoginRequiredMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_login_required_mixin_works_when_user_not_logged_in(self):
        """Test login_required mixin works when user not logged in"""

        class TestView(LoginRequiredMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.anonymous_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    # endregion Login Required Tests

    # region Allow Without Permissions Tests

    # endregion Allow Without Permissions Tests

    # region One Permission Required Tests

    # endregion One Permission Required Tests

    # region Permission Required Tests

    def test_mixin_works_with_permission_required_defined(self):
        """Test mixin works with permission required defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = ["auth.add_foo"]

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_works_with_permission_required_defined_as_string(self):
        """Test mixin works with permission required defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = "auth.add_foo"

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_works_with_permission_required_one_defined(self):
        """Test mixing works with permission required one defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = ["auth.add_foo"]

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_works_with_permission_required_one_defined_as_string(self):
        """Test mixing works with permission required one defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = "auth.add_foo"

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_prevents_access_for_no_perms_all(self):
        """Test mixin prevents access for no perms all"""

    def test_mixin_has_error_when_no_permissions_defined(self):
        """Test mixin has error when no permissions defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        with self.assertRaises(ImproperlyConfigured):

            request = self.factory.get("/rand")
            setattr(request, "user", self.full_user)
            TestView.as_view()(request)

    # endregion Permission Required Tests
