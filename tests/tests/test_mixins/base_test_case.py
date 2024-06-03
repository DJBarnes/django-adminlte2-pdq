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
from adminlte2_pdq.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Module Variables.
UserModel = get_user_model()


class BaseMixinTextCase(IntegrationTestCase):
    """Base class for Mixin tests."""

    # region Expected Test Messages

    # BUG: Some instances of accessing a Mixin reads as a decorator instead.
    #   Possibly resolved: Might have just been poorly organized testing urls. Double check later.
    pdq_loose__allow_anonymous_access_decorator_message = (
        "The allow_anonymous_access decorator is not supported in AdminLtePdq LOOSE mode. "
        "This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_without_permissions_decorator_message = (
        "The allow_without_permissions decorator is not supported in AdminLtePdq LOOSE mode. "
        "This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_anonymous_access_mixin_message = (
        "The allow_anonymous_access mixin is not supported in AdminLtePdq LOOSE mode. "
        "This mixin only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_without_permissions_mixin_message = (
        "The allow_without_permissions mixin is not supported in AdminLtePdq LOOSE mode. "
        "This mixin only exists for clarity of permission access in STRICT mode."
    )
    pdq__no_permissions_one__message = (
        "AdminLtePdq Warning: The class-based view 'BleedingOnePermissionMissingPermissionsView' "
        "has permission requirements, but does not have any permissions set. "
        "This means that this view is inaccessible until permissions are set for the view."
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )
    pdq__no_permissions_full__message = (
        "AdminLtePdq Warning: The class-based view 'BleedingFullPermissionMissingPermissionsView' "
        "has permission requirements, but does not have any permissions set. "
        "This means that this view is inaccessible until permissions are set for the view."
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )

    pdq_strict__no_mixin_message = (
        "AdminLtePdq Warning: This project is set to run in strict mode, and "
        "the class-based view 'StandardView' does not have any mixins set. "
        "This means that this view is inaccessible until permission mixins "
        "are set for the view, or the view is added to the "
        "ADMINLTE2_STRICT_POLICY_WHITELIST setting."
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )
    pdq_strict__login_required_mixin_message = (
        "The login_required mixin is not supported in AdminLtePdq STRICT mode. "
        "Having STRICT mode on implicitly assumes login and permissions are required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the allow_anonymous_access or allow_without_permissions mixins."
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

    #     class TestView(PermissionRequiredMixin, View):
    #         """Test View Class"""
    #
    #         permission_required = 'auth.add_foo'
    #
    #         def get(self, request):
    #             """Test get method"""
    #             return HttpResponse('foobar')
    #
    #     with self.assertRaises(PermissionDenied):
    #         request = self.factory.get('/rand')
    #         setattr(request, 'user', self.user)
    #         TestView.as_view()(request)
    #
    # def test_mixin_prevents_access_for_no_perms_one(self):
    #     """Test mixin prevents access for no perms one"""
    #
    #     class TestView(PermissionRequiredMixin, View):
    #         """Test View Class"""
    #
    #         permission_required_one = 'auth.add_foo'
    #
    #         def get(self, request):
    #             """Test get method"""
    #             return HttpResponse('foobar')
    #
    #     with self.assertRaises(PermissionDenied):
    #         request = self.factory.get('/rand')
    #         setattr(request, 'user', self.user)
    #         TestView.as_view()(request)

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

    # |-------------------------------------------------------------------------
    # | Test login_required
    # |-------------------------------------------------------------------------

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
