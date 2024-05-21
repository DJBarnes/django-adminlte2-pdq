"""
Tests for Mixins
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import override_settings, RequestFactory, TestCase
from django.views import View
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Module Variables.
UserModel = get_user_model()


class DaveMixinTestCase(TestCase):
    """Original mixin tests by Dave."""

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


class MixinTextCaseBase(IntegrationTestCase):
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

        # Add permissions auth.add_foo and auth.change_foo to full_perm_user.
        self.full_perm_user = self.get_user("john_full")
        self.add_user_permission("add_foo", user=self.full_perm_user)
        self.add_user_permission("change_foo", user=self.full_perm_user)

        # Add permission auth.add_foo to partial_perm_user.
        self.partial_perm_user = self.get_user("jane_partial")
        self.add_user_permission("add_foo", user=self.partial_perm_user)

        # Add add_barr and change_bar groups to full_group_user.
        self.full_group_user = self.get_user("jenny_full")
        self.add_user_group("add_bar", user=self.full_group_user)
        self.add_user_group("change_bar", user=self.full_group_user)

        # Add add_barr and change_bar groups to partial_group_user.
        self.partial_group_user = self.get_user("jimmy_partial")
        self.add_user_group("add_bar", user=self.partial_group_user)

        # Add only "unused" permission to this incorrect_group_user.
        self.incorrect_group_user = self.get_user("johnny_wrong")
        self.add_user_group("unused_bar", user=self.full_group_user)

        # Add no permissions/groups to none_user.
        self.none_user = self.get_user("joe_none")

        # Easy access to anonymous user.
        self.anonymous_user = AnonymousUser()


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=False)
@override_settings(STRICT_POLICY=False)
@patch("adminlte2_pdq.constants.STRICT_POLICY", False)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", False)
class StandardMixinTestCase(MixinTextCaseBase):
    """
    Test project authentication mixins, under project "Loose" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertFalse(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from contants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        # Test for expected setting values.
        self.assertFalse(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Loose" mode. For sanity checking."""

        with self.subTest("As anonymous user"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.none_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Standard View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Standard View Header",
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-anonymous-access",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.none_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-login-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-allow-without-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

            # with self.subTest('As user with one permission'):
            #     # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=False)
@override_settings(STRICT_POLICY=False)
@patch("adminlte2_pdq.constants.STRICT_POLICY", False)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", False)
class StandardBleedingMixinTestCase(MixinTextCaseBase):
    """Tests to make sure mixin logic doesn't bleed into each other.

    By "bleeding", we refer to instances when the user overlaps values for one
    Mixin with another. Or forgets expected values of a Mixin. Or combinations thereof.

    For example, a LoginRequired Mixin should always behave the same as the login_required
    decorator, even if the user accidentally defines permissions on the view as well.

    Due to how Mixins and our project middleware works, these are not as cleanly separated
    as they are with the decorators, and so additional tests are required.

    NOTE: I'm not sure if it's possible to get updated values for response attributes?
          Seems to only return the values defined at literal class value.
          So sometimes the passed attributes seem "wrong" but as long as the actual view
          directs as expected, then it's probably fine? Not sure if there's a better way...
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertFalse(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from contants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        # Test for expected setting values.
        self.assertFalse(LOGIN_REQUIRED)
        self.assertFalse(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__bleeding_anonymous_with_permissions(self):
        """Bleeding tests for allow_anonymous_access mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_mixin_message, str(err.exception))

    def test__bleeding_login_with_permissions(self):
        """Bleeding tests for login_required mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.none_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full permissions"):
            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full groups"):
            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Login Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Login Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "login_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

    def test__bleeding_conflicting_permissions(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_mixin_message, str(err.exception))

    def test__bleeding_one_permission_missing_permissions(self):
        """Bleeding tests for permission_required_one mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__bleeding_full_permission_missing_permissions(self):
        """Bleeding tests for permission_required_one mixin, in project "Loose" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class StrictMixinTestCase(MixinTextCaseBase):
    """
    Test project authentication mixins, under project "Strict" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from contants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertFalse(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__no_mixins(self):
        """Test for view with no mixins, in project "Strict" mode.
        Everything should redirect with a warning message.
        """

        with self.subTest("As anonymous user"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.none_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Dashboard",
                expected_header="Dashboard <small>Version 2.0</small>",
                expected_messages=[
                    self.pdq_strict__no_mixin_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no mixins so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__allow_anonymous_access_mixin(self):
        """Test for allow_anonymous_access mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.none_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-anonymous-access",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__login_required_mixin(self):
        """Test for login_required mixin, in project "Strict" mode.
        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        with self.subTest("As anonymous user"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-login-required",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__allow_without_permissions_mixin(self):
        """Test for allow_without_permissions mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.none_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-allow-without-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertIsNone(data_dict["full_permissions"])

    def test__one_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-one-permission-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="One Permission Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | One Permission Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertIsNone(data_dict["full_permissions"])

    def test__full_permission_required_mixin(self):
        """Test for permission_required mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-full-permissions-required",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Full Permissions Required View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Full Permissions Required View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "permission_required",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertIsNone(data_dict["one_of_permissions"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch("adminlte2_pdq.constants.STRICT_POLICY", True)
@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)
class StrictBleedingMixinTestCase(MixinTextCaseBase):
    """Tests to make sure mixin logic doesn't bleed into each other.

    By "bleeding", we refer to instances when the user overlaps values for one
    Mixin with another. Or forgets expected values of a Mixin. Or combinations thereof.

    For example, a LoginRequired Mixin should always behave the same as the login_required
    decorator, even if the user accidentally defines permissions on the view as well.

    Due to how Mixins and our project middleware works, these are not as cleanly separated
    as they are with the decorators, and so additional tests are required.

    NOTE: I'm not sure if it's possible to get updated values for response attributes?
          Seems to only return the values defined at literal class value.
          So sometimes the passed attributes seem "wrong" but as long as the actual view
          directs as expected, then it's probably fine? Not sure if there's a better way...
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, "ADMINLTE2_USE_LOGIN_REQUIRED", False))
        self.assertTrue(getattr(settings, "STRICT_POLICY", False))
        self.assertEqual(0, len(getattr(settings, "LOGIN_EXEMPT_WHITELIST", [])))
        self.assertEqual(0, len(getattr(settings, "STRICT_POLICY_WHITELIST", [])))

        # Verify values imported from contants.py file.
        from adminlte2_pdq.constants import (
            LOGIN_REQUIRED,
            STRICT_POLICY,
            LOGIN_EXEMPT_WHITELIST,
            STRICT_POLICY_WHITELIST,
        )

        self.assertFalse(LOGIN_REQUIRED)
        self.assertTrue(STRICT_POLICY)
        self.assertEqual(7, len(LOGIN_EXEMPT_WHITELIST))
        self.assertEqual(10, len(STRICT_POLICY_WHITELIST))

    def test__bleeding_anonymous_with_permissions(self):
        """Bleeding tests for allow_anonymous_access mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.none_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual("allow_anonymous_access", data_dict["decorator_name"])
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-anonymous-with-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Allow Anonymous Access View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Anonymous Access View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_anonymous_access",
                data_dict["decorator_name"],
            )
            self.assertFalse(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

    def test__bleeding_login_with_permissions(self):
        """Test for login_required mixin, in project "Strict" mode.
        In strict mode, this mixin should NOT work, and instead raise errors.
        """

        with self.subTest("As anonymous user"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with no permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one permission"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full permissions"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with incorrect groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with one group"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

        with self.subTest("As user with full groups"):
            # Invalid mixin used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    "adminlte2_pdq_tests:class-bleeding-login-with-permissions",
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_mixin_message, str(err.exception))

    def test__bleeding_conflicting_permissions(self):
        """Bleeding tests for allow_without_permissions mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
            )

            # Verify values associated with returned view.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.none_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one permission"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with incorrect groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with one group"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-conflicting-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_title="Allow Without Permissions View | Django AdminLtePdq Testing",
                expected_header="Django AdminLtePdq | Allow Without Permissions View Header",
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, "admin_pdq_data"))
            data_dict = response.admin_pdq_data
            self.assertEqual(
                "allow_without_permissions",
                data_dict["decorator_name"],
            )
            self.assertTrue(data_dict["login_required"])
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["one_of_permissions"]),
            )
            self.assertEqual(
                ("auth.add_foo", "auth.change_foo"),
                tuple(data_dict["full_permissions"]),
            )

    def test__one_permission_required_mixin(self):
        """Bleeding tests for permission_required_one mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_title="Login |",
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-one-permission-missing-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_one__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

    def test__full_permission_required_mixin(self):
        """Test for permission_required_one mixin, in project "Strict" mode."""

        with self.subTest("As anonymous user"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with no permissions"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one permission"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full permissions"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with incorrect groups"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with one group"):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))

        with self.subTest("As user with full groups"):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                "adminlte2_pdq_tests:class-bleeding-full-permission-missing-permissions",
                user=self.full_group_user,
                expected_status=200,
                expected_content=[
                    "Sign in to start your session",
                    "Remember Me",
                    "I forgot my password",
                ],
                expected_messages=[
                    self.pdq__no_permissions_full__message,
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, "admin_pdq_data"))
