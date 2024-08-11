"""
Tests for Decorators
"""

# System Imports.

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST
from adminlte2_pdq.decorators import login_required, permission_required, permission_required_one


# Module Variables.
UserModel = get_user_model()
WHITELIST_VIEWS = [
    "adminlte2_pdq_tests:function-standard",
    "adminlte2_pdq_tests:function-allow-anonymous-access",
    "adminlte2_pdq_tests:function-login-required",
    "adminlte2_pdq_tests:function-allow-without-permissions",
    "adminlte2_pdq_tests:function-one-permission-required",
    "adminlte2_pdq_tests:function-full-permissions-required",
]
LOGIN_WHITELIST_VIEWS = LOGIN_EXEMPT_WHITELIST + WHITELIST_VIEWS
PERM_WHITELIST_VIEWS = STRICT_POLICY_WHITELIST + WHITELIST_VIEWS


class TestIsolatedDecorators(TestCase):
    """Test logic that DOES NOT seem to touch/trigger middleware.

    Thus, this tests Decorator logic for projects that do not have the package middleware enabled.
    """

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        Permission.objects.create(name="add_foo", codename="add_foo", content_type=self.permission_content_type)
        Permission.objects.create(name="change_foo", codename="change_foo", content_type=self.permission_content_type)
        # Add permissions auth.add_foo and auth.change_foo to full_user
        full_perms = Permission.objects.filter(codename__in=("add_foo", "change_foo"))
        self.full_user = UserModel.objects.create(username="johnfull", password="qwerty")
        self.full_user.user_permissions.add(*full_perms)

        # Add permission auth.add_foo to partial_user
        partial_perms = Permission.objects.filter(codename="add_foo")

        self.partial_user = UserModel.objects.create(username="janepartial", password="qwerty")
        self.partial_user.user_permissions.add(*partial_perms)

        # Add no permissions to none_user
        self.none_user = UserModel.objects.create(username="joenone", password="qwerty")

        self.anonymous_user = AnonymousUser()

    # region Allow Anonymous Tests

    # endregion Allow Anonymous Tests

    # region Login Required Tests

    def test_login_required_decorator_works(self):
        """Test login_required decorator works"""

        @login_required
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)

    def test_login_required_decorator_works_when_user_not_logged_in(self):
        """Test login_required decorator works when user not logged in"""

        @login_required
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.anonymous_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)

    # endregion Login Required Tests

    # region Allow Without Permissions Tests

    # endregion Allow Without Permissions Tests

    # region One Permission Required Tests

    def test_permission_required_one_works_when_permission_is_a_string(self):
        """Test permission_required_one works when permission is a string"""

        @permission_required_one("auth.add_foo")
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.admin_pdq_data["one_of_permissions"],
            ("auth.add_foo",),
        )

    def test_permission_required_one_works_when_user_has_all(self):
        """Test permission_required_one work when user has all"""

        @permission_required_one(("auth.add_foo", "auth.change_foo"))
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.admin_pdq_data["one_of_permissions"],
            ("auth.add_foo", "auth.change_foo"),
        )

    def test_permission_required_one_works_when_user_has_one(self):
        """Test permission_required_one works when user has one"""

        @permission_required_one(("auth.add_foo", "auth.change_foo"))
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.partial_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.admin_pdq_data["one_of_permissions"],
            ("auth.add_foo", "auth.change_foo"),
        )

    def test_permission_required_one_works_when_user_has_none(self):
        """Test permission_required_one works when user has none"""

        @permission_required_one(("auth.add_foo", "auth.change_foo"))
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.none_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            a_view.admin_pdq_data["one_of_permissions"],
            ("auth.add_foo", "auth.change_foo"),
        )

    def test_permission_required_one_works_when_user_has_none_and_raise_exception(self):
        """Test permission_required_one works when user has none and raise exception"""

        @permission_required_one(("auth.add_foo", "auth.change_foo"), raise_exception=True)
        def a_view(request):
            return HttpResponse("foobar")

        with self.assertRaises(PermissionDenied):

            request = self.factory.get("/rand")
            setattr(request, "user", self.none_user)
            response = a_view(request)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                a_view.admin_pdq_data["one_of_permissions"],
                ("auth.add_foo", "auth.change_foo"),
            )

    # endregion One Permission Required Tests

    # region Permission Required Tests

    def test_permission_required_works_when_permission_is_a_string(self):
        """Test permission_required works when permission is a string"""

        @permission_required("auth.add_foo")
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.admin_pdq_data["full_permissions"],
            ("auth.add_foo",),
        )

    def test_permission_required_works_when_user_has_all(self):
        """Test permission_required works when user has all"""

        @permission_required(("auth.add_foo", "auth.change_foo"))
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.admin_pdq_data["full_permissions"],
            ("auth.add_foo", "auth.change_foo"),
        )

    def test_permission_required_works_when_user_has_one(self):
        """Test permission_required works when user has one"""

        @permission_required(("auth.add_foo", "auth.change_foo"))
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.partial_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            a_view.admin_pdq_data["full_permissions"],
            ("auth.add_foo", "auth.change_foo"),
        )

    def test_permission_required_works_when_user_has_none(self):
        """Test permission_required works when user has none"""

        @permission_required(("auth.add_foo", "auth.change_foo"))
        def a_view(request):
            return HttpResponse("foobar")

        request = self.factory.get("/rand")
        setattr(request, "user", self.none_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            a_view.admin_pdq_data["full_permissions"],
            ("auth.add_foo", "auth.change_foo"),
        )

    def test_permission_required_works_when_user_has_none_and_raise_exception(self):
        """Test permission_required works when user has none and raise exception"""

        @permission_required(("auth.add_foo", "auth.change_foo"), raise_exception=True)
        def a_view(request):
            return HttpResponse("foobar")

        with self.assertRaises(PermissionDenied):

            request = self.factory.get("/rand")
            setattr(request, "user", self.none_user)
            response = a_view(request)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                a_view.admin_pdq_data["full_permissions"],
                ("auth.add_foo", "auth.change_foo"),
            )

    # endregion Permission Required Tests
