"""
Tests for Decorators
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, override_settings, RequestFactory
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.decorators import login_required, permission_required, permission_required_one


# Module Variables.
UserModel = get_user_model()


class DecoratorTestCase(TestCase):
    """Original decorator tests by Dave."""

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        Permission.objects.create(name="add_foo", codename='add_foo', content_type=self.permission_content_type)
        Permission.objects.create(name="change_foo", codename='change_foo', content_type=self.permission_content_type)
        # Add permissions auth.add_foo and auth.change_foo to full_user
        full_perms = Permission.objects.filter(codename__in=('add_foo', 'change_foo'))
        self.full_user = UserModel.objects.create(username='johnfull', password='qwerty')
        self.full_user.user_permissions.add(*full_perms)

        # Add permission auth.add_foo to partial_user
        partial_perms = Permission.objects.filter(codename='add_foo')

        self.partial_user = UserModel.objects.create(username='janepartial', password='qwerty')
        self.partial_user.user_permissions.add(*partial_perms)

        # Add no permissions to none_user
        self.none_user = UserModel.objects.create(username='joenone', password='qwerty')

        self.anonymous_user = AnonymousUser()

    # |--------------------------------------------------------------------------
    # | Test permission_required_one
    # |--------------------------------------------------------------------------

    def test_permission_required_one_works_when_permission_is_a_string(self):
        """Test permission_required_one works when permission is a string"""

        @permission_required_one('auth.add_foo')
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(a_view.one_of_permissions, ('auth.add_foo',))

    def test_permission_required_one_works_when_user_has_all(self):
        """Test permission_required_one work when user has all"""

        @permission_required_one(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(a_view.one_of_permissions, ('auth.add_foo', 'auth.change_foo'))

    def test_permission_required_one_works_when_user_has_one(self):
        """Test permission_required_one works when user has one"""

        @permission_required_one(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.partial_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(a_view.one_of_permissions, ('auth.add_foo', 'auth.change_foo'))

    def test_permission_required_one_works_when_user_has_none(self):
        """Test permission_required_one works when user has none"""

        @permission_required_one(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.none_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(a_view.one_of_permissions, ('auth.add_foo', 'auth.change_foo'))

    def test_permission_required_one_works_when_user_has_none_and_raise_exception(self):
        """Test permission_required_one works when user has none and raise exception"""

        @permission_required_one(('auth.add_foo', 'auth.change_foo'), raise_exception=True)
        def a_view(request):
            return HttpResponse('foobar')

        with self.assertRaises(PermissionDenied):

            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = a_view(request)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(a_view.one_of_permissions, ('auth.add_foo', 'auth.change_foo'))

    # |--------------------------------------------------------------------------
    # | Test permission_required
    # |--------------------------------------------------------------------------

    def test_permission_required_works_when_permission_is_a_string(self):
        """Test permission_required works when permission is a string"""

        @permission_required('auth.add_foo')
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(a_view.permissions, ('auth.add_foo',))

    def test_permission_required_works_when_user_has_all(self):
        """Test permission_required works when user has all"""

        @permission_required(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(a_view.permissions, ('auth.add_foo', 'auth.change_foo'))

    def test_permission_required_works_when_user_has_one(self):
        """Test permission_required works when user has one"""

        @permission_required(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.partial_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(a_view.permissions, ('auth.add_foo', 'auth.change_foo'))

    def test_permission_required_works_when_user_has_none(self):
        """Test permission_required works when user has none"""

        @permission_required(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.none_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(a_view.permissions, ('auth.add_foo', 'auth.change_foo'))

    def test_permission_required_works_when_user_has_none_and_raise_exception(self):
        """Test permission_required works when user has none and raise exception"""

        @permission_required(('auth.add_foo', 'auth.change_foo'), raise_exception=True)
        def a_view(request):
            return HttpResponse('foobar')

        with self.assertRaises(PermissionDenied):

            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = a_view(request)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(a_view.permissions, ('auth.add_foo', 'auth.change_foo'))

    # |-------------------------------------------------------------------------
    # | Test login_required
    # |-------------------------------------------------------------------------

    def test_login_required_decorator_works(self):
        """Test login_required decorator works"""

        @login_required
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)

    def test_login_required_decorator_works_when_user_not_logged_in(self):
        """Test login_required decorator works when user not logged in"""

        @login_required
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.anonymous_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)


class DecoratorTestCaseBase(IntegrationTestCase):
    """Base class for Decorator tests."""

    # region Expected Test Messages

    pdq_loose__allow_anonymous_access_decorator_message = (
        'The allow_anonymous_access decorator is not supported in AdminLtePdq LOOSE mode. '
        'This decorator only exists for clarity of permission access in STRICT mode.'
    )
    pdq_loose__allow_without_permissions_decorator_message = (
        'The allow_without_permissions decorator is not supported in AdminLtePdq LOOSE mode. '
        'This decorator only exists for clarity of permission access in STRICT mode.'
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
        'The login_required decorator is not supported in AdminLtePdq STRICT mode. '
        'Having STRICT mode on implicitly assumes login and permissions are required '
        'for all views that are not in a whitelist setting.'
        '\n\n'
        'Also consider the allow_anonymous_access or allow_without_permissions decorators.'
    )

    # endregion Expected Test Messages

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        # Generate test permissions.

        # First permission. Generally used anywhere at least one permission is required.
        add_foo = Permission.objects.create(
            name="add_foo",
            codename='add_foo',
            content_type=self.permission_content_type,
        )
        # Second permission. Generally used anywhere multiple permissions are required.
        change_foo = Permission.objects.create(
            name="change_foo",
            codename='change_foo',
            content_type=self.permission_content_type,
        )
        # Extra permissions used in some edge case tests.
        view_foo = Permission.objects.create(
            name="view_foo",
            codename='view_foo',
            content_type=self.permission_content_type,
        )
        delete_foo = Permission.objects.create(
            name="delete_foo",
            codename='delete_foo',
            content_type=self.permission_content_type,
        )
        # Final extra permission that's not explicitly used anywhere.
        # To verify permission logic still works with extra, unrelated permissions in the project.
        unused_foo = Permission.objects.create(
            name="unused_foo",
            codename='unused_foo',
            content_type=self.permission_content_type,
        )

        # Define various permission sets to test against.
        self.full_perms = Permission.objects.filter(codename__in=('add_foo', 'change_foo'))
        self.partial_perms = Permission.objects.filter(codename='add_foo')

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
        self.full_groups = Group.objects.filter(name__in=('add_bar', 'change_bar'))
        self.partial_groups = Group.objects.filter(name='add_bar')

        # Define our actual users to test against.

        # Add permissions auth.add_foo and auth.change_foo to full_perm_user.
        self.full_perm_user = self.get_user('john_full')
        self.add_user_permission('add_foo', user=self.full_perm_user)
        self.add_user_permission('change_foo', user=self.full_perm_user)

        # Add permission auth.add_foo to partial_perm_user.
        self.partial_perm_user = self.get_user('jane_partial')
        self.add_user_permission('add_foo', user=self.partial_perm_user)

        # Add add_barr and change_bar groups to full_group_user.
        self.full_group_user = self.get_user('jenny_full')
        self.add_user_group('add_bar', user=self.full_group_user)
        self.add_user_group('change_bar', user=self.full_group_user)

        # Add add_barr and change_bar groups to partial_group_user.
        self.partial_group_user = self.get_user('jimmy_partial')
        self.add_user_group('add_bar', user=self.partial_group_user)

        # Add only "unused" permission to this incorrect_group_user.
        self.incorrect_group_user = self.get_user('johnny_wrong')
        self.add_user_group('unused_bar', user=self.incorrect_group_user)

        # Add no permissions/groups to none_user.
        self.none_user = self.get_user('joe_none')

        # Easy access to anonymous user.
        self.anonymous_user = AnonymousUser()


@override_settings(ADMINLTE2_USE_STRICT_POLICY=False)
@override_settings(STRICT_POLICY=False)
@patch('adminlte2_pdq.constants.STRICT_POLICY', False)
@patch('adminlte2_pdq.middleware.STRICT_POLICY', False)
class ReworkedDecoratorTestCase__Standard(DecoratorTestCaseBase):
    """
    Test project authentication decorators, under project "Loose" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, 'ADMINLTE2_USE_LOGIN_REQUIRED', False))
        self.assertFalse(getattr(settings, 'STRICT_POLICY', False))
        self.assertEqual(0, len(getattr(settings, 'LOGIN_EXEMPT_WHITELIST', [])))
        self.assertEqual(0, len(getattr(settings, 'STRICT_POLICY_WHITELIST', [])))

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

    def test__no_decorators(self):
        """Test for view with no decorators, in project "Loose" mode. For sanity checking."""

        with self.subTest('As anonymous user'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.none_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with incorrect groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Standard View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Standard View Header',
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

    def test__allow_anonymous_access_decorator(self):
        """Test for allow_anonymous_access decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

        with self.subTest('As user with no permissions'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

        with self.subTest('As user with one permission'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

        with self.subTest('As user with full permissions'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

        with self.subTest('As user with incorrect groups'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

        with self.subTest('As user with one group'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

        with self.subTest('As user with full groups'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-anonymous-access',
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_anonymous_access_decorator_message, str(err.exception))

    def test__login_required_decorator(self):
        """Test for login_required decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.none_user,
                expected_status=200,
                expected_title='Login Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Login Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'login_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='Login Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Login Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'login_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Login Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Login Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'login_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title='Login Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Login Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'login_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='Login Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Login Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'login_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-login-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Login Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Login Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'login_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

    def test__allow_without_permissions_decorator(self):
        """Test for allow_without_permissions decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

        with self.subTest('As user with no permissions'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

        with self.subTest('As user with one permission'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

        with self.subTest('As user with full permissions'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

        with self.subTest('As user with incorrect groups'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

        with self.subTest('As user with one group'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

        with self.subTest('As user with full groups'):
            # Invalid decorator used for loose mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-allow-without-permissions',
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_loose__allow_without_permissions_decorator_message, str(err.exception))

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

    def test__full_permission_required_decorator(self):
        """Test for permission_required decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Full Permissions Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Full Permissions Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one group'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Full Permissions Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Full Permissions Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'permissions'),
            )

    def test__one_group_required_decorator(self):
        """Test for permission_required_one decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with full permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='One Group Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Group Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertTrue(hasattr(response, 'one_of_groups'))
            self.assertTrue(hasattr(response, 'groups'))
            self.assertEqual(
                'group_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )
            self.assertEqual(
                ('add_bar', 'change_bar'),
                getattr(response, 'one_of_groups'),
            )
            self.assertIsNone(
                getattr(response, 'groups'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='One Group Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Group Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertTrue(hasattr(response, 'one_of_groups'))
            self.assertTrue(hasattr(response, 'groups'))
            self.assertEqual(
                'group_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )
            self.assertEqual(
                ('add_bar', 'change_bar'),
                getattr(response, 'one_of_groups'),
            )
            self.assertIsNone(
                getattr(response, 'groups'),
            )

    def test__full_group_required_decorator(self):
        """Test for group_required decorator, in project "Loose" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with full permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one group'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Full Groups Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Full Groups Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertTrue(hasattr(response, 'one_of_groups'))
            self.assertTrue(hasattr(response, 'groups'))
            self.assertEqual(
                'group_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_groups'),
            )
            self.assertEqual(
                ('add_bar', 'change_bar'),
                getattr(response, 'groups'),
            )


@override_settings(DEBUG=True)
@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch('adminlte2_pdq.constants.STRICT_POLICY', True)
@patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
class ReworkedDecoratorTestCase__Strict(DecoratorTestCaseBase):
    """
    Test project authentication decorators, under project "Strict" mode.
    """

    def test__verify_patch_settings(self):
        """Sanity check tests, to make sure settings are set as intended, even if other tests fail."""

        # Verify actual project settings values.
        self.assertFalse(getattr(settings, 'ADMINLTE2_USE_LOGIN_REQUIRED', False))
        self.assertTrue(getattr(settings, 'STRICT_POLICY', False))
        self.assertEqual(0, len(getattr(settings, 'LOGIN_EXEMPT_WHITELIST', [])))
        self.assertEqual(0, len(getattr(settings, 'STRICT_POLICY_WHITELIST', [])))

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

    def test__no_decorators(self):
        """Test for view with no decorators, in project "Strict" mode.
        Everything should redirect with a warning message.
        """

        with self.subTest('As anonymous user'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.none_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one permission'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full permissions'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with incorrect groups'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one group'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full groups'):
            # View configured incorrectly for strict mode. Should redirect to "home".

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-standard',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Dashboard',
                expected_header='Dashboard <small>Version 2.0</small>',
                expected_messages=[
                    self.pdq_strict__no_decorator_message,
                ],
            )

            # Verify values associated with returned view.
            # View had no decorators so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

    def test__allow_anonymous_access_decorator(self):
        """Test for allow_anonymous_access decorator, in project "Strict" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with no permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.none_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-anonymous-access',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Allow Anonymous Access View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Anonymous Access View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_anonymous_access',
                getattr(response, 'decorator_name'),
            )
            self.assertFalse(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

    def test__login_required_decorator(self):
        """Test for login_required decorator, in project "Strict" mode.
        In strict mode, this decorator should NOT work, and instead raise errors.
        """

        with self.subTest('As anonymous user'):
            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.anonymous_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

        with self.subTest('As user with no permissions'):
            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.none_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

        with self.subTest('As user with one permission'):
            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.partial_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.full_perm_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

        with self.subTest('As user with incorrect groups'):
            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.incorrect_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

        with self.subTest('As user with one group'):
            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.partial_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            # Invalid decorator used for strict mode. Should raise error.

            with self.assertRaises(PermissionError) as err:
                self.assertGetResponse(
                    'adminlte2_pdq_tests:function-login-required',
                    user=self.full_group_user,
                    expected_status=500,
                )
            self.assertText(self.pdq_strict__login_required_decorator_message, str(err.exception))

    def test__allow_without_permissions_decorator(self):
        """Test for allow_without_permissions decorator, in project "Strict" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            self.assertIsNone(
                getattr(response, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(response, 'permissions', None),
            )

        with self.subTest('As user with no permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.none_user,
                expected_status=200,
                expected_title='Allow Without Permissions View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Without Permissions View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_without_permissions',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='Allow Without Permissions View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Without Permissions View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_without_permissions',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Allow Without Permissions View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Without Permissions View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_without_permissions',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_title='Allow Without Permissions View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Without Permissions View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_without_permissions',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='Allow Without Permissions View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Without Permissions View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_without_permissions',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-allow-without-permissions',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Allow Without Permissions View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Allow Without Permissions View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'allow_without_permissions',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Strict" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-permission-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='One Permission Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Permission Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )

    def test__full_permission_required_decorator(self):
        """Test for permission_required decorator, in project "Strict" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_title='Full Permissions Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Full Permissions Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'permissions'),
            )

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with one group'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-permissions-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Full Permissions Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Full Permissions Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertEqual(
                'permission_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(response, 'permissions'),
            )

    def test__one_group_required_decorator(self):
        """Test for group_required_one decorator, in project "Strict" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_title='Login |',
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with full permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            # Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one group'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_title='One Group Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Group Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertTrue(hasattr(response, 'one_of_groups'))
            self.assertTrue(hasattr(response, 'groups'))
            self.assertEqual(
                'group_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )
            self.assertEqual(
                ('add_bar', 'change_bar'),
                getattr(response, 'one_of_groups'),
            )
            self.assertIsNone(
                getattr(response, 'groups'),
            )

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-one-group-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='One Group Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | One Group Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertTrue(hasattr(response, 'one_of_groups'))
            self.assertTrue(hasattr(response, 'groups'))
            self.assertEqual(
                'group_required_one',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )
            self.assertEqual(
                ('add_bar', 'change_bar'),
                getattr(response, 'one_of_groups'),
            )
            self.assertIsNone(
                getattr(response, 'groups'),
            )

    def test__full_groups_required_decorator(self):
        """Test for group_required decorator, in project "Strict" mode."""

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.anonymous_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.none_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.partial_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with full permissions'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.full_perm_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with incorrect groups'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.incorrect_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with one group'):
            # Should fail and redirect to login.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.partial_group_user,
                expected_status=200,
                expected_content=[
                    'Sign in to start your session',
                    'Remember Me',
                    'I forgot my password',
                ],
            )

            # Verify values associated with returned view.
            # Was redirected to login so should be no data.
            self.assertFalse(hasattr(response, 'decorator_name'))
            self.assertFalse(hasattr(response, 'login_required'))
            self.assertFalse(hasattr(response, 'one_of_permissions'))
            self.assertFalse(hasattr(response, 'permissions'))
            self.assertFalse(hasattr(response, 'one_of_groups'))
            self.assertFalse(hasattr(response, 'groups'))

        with self.subTest('As user with full groups'):
            # Should succeed and load as expected.

            #  Verify we get the expected page.
            response = self.assertGetResponse(
                'adminlte2_pdq_tests:function-full-groups-required',
                user=self.full_group_user,
                expected_status=200,
                expected_title='Full Groups Required View | Django AdminLtePdq Testing',
                expected_header='Django AdminLtePdq | Full Groups Required View Header',
            )

            # Verify values associated with returned view.
            self.assertTrue(hasattr(response, 'decorator_name'))
            self.assertTrue(hasattr(response, 'login_required'))
            self.assertTrue(hasattr(response, 'one_of_permissions'))
            self.assertTrue(hasattr(response, 'permissions'))
            self.assertTrue(hasattr(response, 'one_of_groups'))
            self.assertTrue(hasattr(response, 'groups'))
            self.assertEqual(
                'group_required',
                getattr(response, 'decorator_name'),
            )
            self.assertTrue(
                getattr(response, 'login_required'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_permissions'),
            )
            self.assertIsNone(
                getattr(response, 'permissions'),
            )
            self.assertIsNone(
                getattr(response, 'one_of_groups'),
            )
            self.assertEqual(
                ('add_bar', 'change_bar'),
                getattr(response, 'groups'),
            )
