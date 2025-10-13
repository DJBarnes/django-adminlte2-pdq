"""
Tests for Mixins
"""

# System Imports.

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.views import View

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST
from adminlte2_pdq.mixins import (
    AllowAnonymousAccessMixin,
    LoginRequiredMixin,
    AllowWithoutPermissionsMixin,
    PermissionRequiredMixin,
)


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

        # Add permissions auth.add_foo and auth.change_foo to full_user.
        full_perms = Permission.objects.filter(codename__in=("add_foo", "change_foo"))
        self.full_user = UserModel.objects.create(username="johnfull", password="qwerty")
        self.full_user.user_permissions.add(*full_perms)

        # Add permission auth.add_foo to partial_user.
        partial_perms = Permission.objects.filter(codename="add_foo")
        self.partial_user = UserModel.objects.create(username="janepartial", password="qwerty")
        self.partial_user.user_permissions.add(*partial_perms)

        # Add no permissions to none_user.
        self.none_user = UserModel.objects.create(username="joenone", password="qwerty")

        self.anonymous_user = AnonymousUser()

    # region Allow Anonymous Tests

    def test__allow_anonymous_access_mixin__allows_authenticated_access(self):
        """Without middleware, this is effectively identical to no authentication mixins."""

        class TestView(AllowAnonymousAccessMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test__allows_anonymous_mixin__allows_anonymous_access(self):
        """Without middleware, this is effectively identical to no authentication mixins."""

        class TestView(AllowAnonymousAccessMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.anonymous_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    # endregion Allow Anonymous Tests

    # region Login Required Tests

    def test__login_required_mixin__allows_authenticated_access(self):
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

    def test__login_required_mixin__prevents_anonymous_access(self):
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

    def test__allow_without_permissions_mixin__allows_authenticated_access(self):
        """Without middleware, this is effectively identical to LoginRequired."""

        class TestView(AllowWithoutPermissionsMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test__allow_without_permissions_mixin__prevents_anonymous_access(self):
        """Without middleware, this is effectively identical to LoginRequired."""

        class TestView(AllowWithoutPermissionsMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.anonymous_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    # endregion Allow Without Permissions Tests

    # region One Permission Required Tests

    def test__permission_required_one_mixin__allows_access_when_permission_is_a_string(self):
        """Test PermissionRequired mixin when only permission_required_one is defined."""

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

    def test__permission_required_one_mixin__allows_access_when_user_has_all(self):
        """Test PermissionRequired mixin when only permission_required_one is defined."""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = ("auth.add_foo", "auth.change_foo")

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test__permission_required_one_mixin__allows_access_when_user_has_one(self):
        """Test PermissionRequired mixin when only permission_required_one is defined."""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = ("auth.add_foo", "auth.change_foo")

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.partial_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test__permission_required_one_mixin__prevents_access_when_user_has_none(self):
        """Test PermissionRequired mixin when only permission_required_one is defined."""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = ("auth.add_foo", "auth.change_foo")

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.none_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    # endregion One Permission Required Tests

    # region Permission Required Tests

    def test__permission_required_mixin__allows_access_when_permission_is_a_string(self):
        """Test PermissionRequired mixin when only permission_required is defined."""

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

    def test__permission_required_mixin__allows_access_when_user_has_all(self):
        """Test PermissionRequired mixin when only permission_required is defined."""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = ("auth.add_foo", "auth.change_foo")

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test__permission_required_mixin__prevents_access_when_user_has_one(self):
        """Test PermissionRequired mixin when only permission_required is defined."""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = ("auth.add_foo", "auth.change_foo")

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.partial_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test__permission_required_mixin__prevents_access_when_user_has_none(self):
        """Test PermissionRequired mixin when only permission_required is defined."""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = ("auth.add_foo", "auth.change_foo")

            def get(self, request):
                """Test get method"""
                return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.none_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test__permission_required_mixin__raises_error_when_no_permissions_defined(self):
        """Test PermissionRequired mixin when only permission_required is defined."""

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
