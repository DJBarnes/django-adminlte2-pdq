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
from adminlte2_pdq.decorators import login_required, permission_required, permission_required_one


# Module Variables.
UserModel = get_user_model()


class BaseDecoratorTestCase(IntegrationTestCase):
    """Base class for Decorator tests."""

    # region Expected Test Messages

    pdq_loose__allow_anonymous_access_decorator_message = (
        "The allow_anonymous_access decorator is not supported in AdminLtePdq LOOSE mode. "
        "This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_without_permissions_decorator_message = (
        "The allow_without_permissions decorator is not supported in AdminLtePdq LOOSE mode. "
        "This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_login__login_required_decorator_message = (
        "The login_required decorator is not supported in AdminLtePdq LOGIN REQUIRED mode. "
        "Having LOGIN REQUIRED mode on implicitly assumes login is required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the allow_anonymous_access decorator."
    )
    pdq_login__allow_without_permissions_decorator_message = (
        "The allow_without_permissions decorator is not supported in AdminLtePdq LOGIN REQUIRED mode. "
        "This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_strict__no_decorator_message = (
        "AdminLtePdq Warning: This project is set to run in strict mode, and "
        "the function-based view 'standard_view' does not have any decorators set. "
        "This means that this view is inaccessible until permission decorators "
        "are set for the view, or the view is added to the "
        "ADMINLTE2_STRICT_POLICY_WHITELIST setting."
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )
    pdq_strict__login_required_decorator_message = (
        "The login_required decorator is not supported in AdminLtePdq STRICT mode. "
        "Having STRICT mode on implicitly assumes login and permissions are required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the allow_anonymous_access or allow_without_permissions decorators."
    )

    # endregion Expected Test Messages

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        # Generate test permissions.

        # First permission. Generally used anywhere at least one permission is required.
        add_foo = Permission.objects.create(
            name="add_foo",
            codename="add_foo",
            content_type=self.permission_content_type,
        )
        # Second permission. Generally used anywhere multiple permissions are required.
        change_foo = Permission.objects.create(
            name="change_foo",
            codename="change_foo",
            content_type=self.permission_content_type,
        )
        # Extra permissions used in some edge case tests.
        view_foo = Permission.objects.create(
            name="view_foo",
            codename="view_foo",
            content_type=self.permission_content_type,
        )
        delete_foo = Permission.objects.create(
            name="delete_foo",
            codename="delete_foo",
            content_type=self.permission_content_type,
        )
        # Final extra permission that's not explicitly used anywhere.
        # To verify permission logic still works with extra, unrelated permissions in the project.
        unused_foo = Permission.objects.create(
            name="unused_foo",
            codename="unused_foo",
            content_type=self.permission_content_type,
        )

        # Define various permission sets to test against.
        self.full_perms = Permission.objects.filter(codename__in=("add_foo", "change_foo"))
        self.partial_perms = Permission.objects.filter(codename="add_foo")

        # Generate test groups. To ensure that as Group logic is handled as expected as well.
        group_instance = Group.objects.create(name="add_bar")
        group_instance.permissions.add(add_foo)
        group_instance = Group.objects.create(name="change_bar")
        group_instance.permissions.add(change_foo)
        group_instance = Group.objects.create(name="view_foo")
        group_instance.permissions.add(view_foo)
        group_instance = Group.objects.create(name="delete_bar")
        group_instance.permissions.add(delete_foo)
        group_instance = Group.objects.create(name="unused_bar")
        group_instance.permissions.add(unused_foo)

        # Define various group sets to test against.
        self.full_groups = Group.objects.filter(name__in=("add_bar", "change_bar"))
        self.partial_groups = Group.objects.filter(name="add_bar")

        # Define our actual users to test against.

        # Easy access to anonymous user.
        self.anonymous_user = AnonymousUser()

        # Add inactive user.
        self.inactive_user = self.get_user("inactive_jacob")
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # Add no permissions/groups to none_user.
        self.none_user = self.get_user("joe_none")

        # Add permission auth.add_foo to partial_perm_user.
        self.partial_perm_user = self.get_user("jane_partial")
        self.add_user_permission("add_foo", user=self.partial_perm_user)

        # Add permissions auth.add_foo and auth.change_foo to full_perm_user.
        self.full_perm_user = self.get_user("john_full")
        self.add_user_permission("add_foo", user=self.full_perm_user)
        self.add_user_permission("change_foo", user=self.full_perm_user)

        # Add no permissions/groups to staff none_user.
        self.none_staff_user = self.get_user("jacob_staff_none")

        # Add permission auth.add_foo to staff partial_perm_user.
        self.partial_perm_staff_user = self.get_user("jack_staff_partial")
        self.add_user_permission("add_foo", user=self.partial_perm_staff_user)

        # Add permissions auth.add_foo and auth.change_foo to staff full_perm_user.
        self.full_perm_staff_user = self.get_user("jessie_staff_full")
        self.add_user_permission("add_foo", user=self.full_perm_staff_user)
        self.add_user_permission("change_foo", user=self.full_perm_staff_user)

        # Add only "unused" permission to this incorrect_group_user.
        self.incorrect_group_user = self.get_user("johnny_wrong")
        self.add_user_group("unused_bar", user=self.incorrect_group_user)

        # Add add_barr and change_bar groups to partial_group_user.
        self.partial_group_user = self.get_user("jimmy_partial")
        self.add_user_group("add_bar", user=self.partial_group_user)

        # Add add_barr and change_bar groups to full_group_user.
        self.full_group_user = self.get_user("jenny_full")
        self.add_user_group("add_bar", user=self.full_group_user)
        self.add_user_group("change_bar", user=self.full_group_user)

        # Add super user.
        self.super_user = self.get_user("super_jessica")
        self.super_user.is_superuser = True
        self.super_user.save()


class TestIsolatedDecorators(TestCase):
    """Test logic that DOES NOT seem to touch/trigger middleware.

    Thus, this  tests Decorator logic for projects that do not have the package middleware enabled.
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

    # |--------------------------------------------------------------------------
    # | Test permission_required_one
    # |--------------------------------------------------------------------------

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

    # |--------------------------------------------------------------------------
    # | Test permission_required
    # |--------------------------------------------------------------------------

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

    # |-------------------------------------------------------------------------
    # | Test login_required
    # |-------------------------------------------------------------------------

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
