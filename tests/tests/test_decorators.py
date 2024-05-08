"""
Tests for Decorators
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.test import TestCase, override_settings, RequestFactory
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.decorators import login_required, permission_required, permission_required_one


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


@override_settings(ADMINLTE2_USE_STRICT_POLICY=False)
@override_settings(STRICT_POLICY=False)
@patch('adminlte2_pdq.constants.STRICT_POLICY', False)
@patch('adminlte2_pdq.middleware.STRICT_POLICY', False)
class ReworkedDecoratorTestCase__Standard(IntegrationTestCase):
    """
    Test project authentication decorators, under project "Loose" mode.
    """

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        # Generate test permissions.
        # First permission. Generally used anywhere at least one permission is required.
        Permission.objects.create(
            name="add_foo",
            codename='add_foo',
            content_type=self.permission_content_type,
        )
        # Second permission. Generally used anywhere multiple permissions are required.
        Permission.objects.create(
            name="change_foo",
            codename='change_foo',
            content_type=self.permission_content_type,
        )
        # Third permission. Extra permission that's not explicitly used anywhere.
        # To verify permission logic still works with extra, unrelated permissions in the project.
        Permission.objects.create(
            name="unused_foo",
            codename='unused_foo',
            content_type=self.permission_content_type,
        )

        # Define various permission sets to test against.
        self.full_perms = Permission.objects.filter(codename__in=('add_foo', 'change_foo'))
        self.partial_perms = Permission.objects.filter(codename='add_foo')

        # Add permissions auth.add_foo and auth.change_foo to full_user.
        self.full_user = self.get_user('john_full')
        self.add_user_permission('add_foo', user=self.full_user)
        self.add_user_permission('change_foo', user=self.full_user)

        # Add permission auth.add_foo to partial_user.
        self.partial_user = self.get_user('jane_partial')
        self.add_user_permission('add_foo', user=self.partial_user)

        # Add no permissions to none_user.
        self.none_user = self.get_user('joe_none')

        # Easy access to anonymous user.
        self.anonymous_user = AnonymousUser()

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

        # region Utility Helper Functions

        def standard_view(request):
            """Standard testing view. No decorators."""
            return render(request, 'standard_view.html')

        # endregion Utility Helper Functions

        with self.subTest('As anonymous user'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.anonymous_user)
            response = standard_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Standard View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Standard View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(standard_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(standard_view, 'permissions', None),
            )

        with self.subTest('As user with no permissions'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = standard_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Standard View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Standard View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(standard_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(standard_view, 'permissions', None),
            )

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.partial_user)
            response = standard_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Standard View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Standard View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(standard_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(standard_view, 'permissions', None),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.full_user)
            response = standard_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Standard View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Standard View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(standard_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(standard_view, 'permissions', None),
            )

    def test__login_required_decorator(self):
        """Test for login_required decorator, in project "Loose" mode."""

        # region Utility Helper Functions

        @login_required
        def login_required_view(request):
            """Standard testing view."""
            return render(request, 'login_required_view.html')

        # endregion Utility Helper Functions

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.anonymous_user)
            response = login_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Verify is redirect.
            self.assertTrue(isinstance(response, HttpResponseRedirect))
            self.assertEqual(
                settings.LOGIN_URL + '?next=/rand',
                response.url,
            )

            # Check status code.
            self.assertEqual(response.status_code, 302)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(login_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(login_required_view, 'permissions', None),
            )

        with self.subTest('As user with no permissions'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = login_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Login Required View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Login Required View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(login_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(login_required_view, 'permissions', None),
            )

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.partial_user)
            response = login_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Login Required View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Login Required View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(login_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(login_required_view, 'permissions', None),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.full_user)
            response = login_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Login Required View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Login Required View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(login_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(login_required_view, 'permissions', None),
            )

    def test__one_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Loose" mode."""

        # region Utility Helper Functions

        @permission_required_one(['auth.add_foo', 'auth.change_foo'])
        def one_permission_required_view(request):
            """Testing view with decorator requirement."""
            return render(request, 'one_permission_required_view.html')

        # endregion Utility Helper Functions

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.anonymous_user)
            response = one_permission_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Verify is redirect.
            self.assertTrue(isinstance(response, HttpResponseRedirect))
            self.assertEqual(
                settings.LOGIN_URL + '?next=/rand',
                response.url,
            )

            # Check status code.
            self.assertEqual(response.status_code, 302)

            # Also verify permissions associated with view.
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(one_permission_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(one_permission_required_view, 'permissions', None),
            )

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = one_permission_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Verify is redirect.
            self.assertTrue(isinstance(response, HttpResponseRedirect))
            self.assertEqual(
                settings.LOGIN_URL + '?next=/rand',
                response.url,
            )

            # Check status code.
            self.assertEqual(response.status_code, 302)

            # Also verify permissions associated with view.
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(one_permission_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(one_permission_required_view, 'permissions', None),
            )

        with self.subTest('As user with one permission'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.partial_user)
            response = one_permission_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'One Permission Required View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | One Permission Required View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(one_permission_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(one_permission_required_view, 'permissions', None),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.full_user)
            response = one_permission_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'One Permission Required View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | One Permission Required View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(one_permission_required_view, 'one_of_permissions', None),
            )
            self.assertIsNone(
                getattr(one_permission_required_view, 'permissions', None),
            )

    def test__full_permission_required_decorator(self):
        """Test for permission_required_one decorator, in project "Loose" mode."""

        # region Utility Helper Functions

        @permission_required(['auth.add_foo', 'auth.change_foo'])
        def full_permissions_required_view(request):
            """Testing view with decorator requirement."""
            return render(request, 'full_permissions_required_view.html')

        # endregion Utility Helper Functions

        with self.subTest('As anonymous user'):
            # Should fail and redirect to login.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.anonymous_user)
            response = full_permissions_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Verify is redirect.
            self.assertTrue(isinstance(response, HttpResponseRedirect))
            self.assertEqual(
                settings.LOGIN_URL + '?next=/rand',
                response.url,
            )

            # Check status code.
            self.assertEqual(response.status_code, 302)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(full_permissions_required_view, 'one_of_permissions', None),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(full_permissions_required_view, 'permissions', None),
            )

        with self.subTest('As user with no permissions'):
            # Should fail and redirect to login.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = full_permissions_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Verify is redirect.
            self.assertTrue(isinstance(response, HttpResponseRedirect))
            self.assertEqual(
                settings.LOGIN_URL + '?next=/rand',
                response.url,
            )

            # Check status code.
            self.assertEqual(response.status_code, 302)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(full_permissions_required_view, 'one_of_permissions', None),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(full_permissions_required_view, 'permissions', None),
            )

        with self.subTest('As user with one permission'):
            # Should fail and redirect to login.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.partial_user)
            response = full_permissions_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Verify is redirect.
            self.assertTrue(isinstance(response, HttpResponseRedirect))
            self.assertEqual(
                settings.LOGIN_URL + '?next=/rand',
                response.url,
            )

            # Check status code.
            self.assertEqual(response.status_code, 302)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(full_permissions_required_view, 'one_of_permissions', None),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(full_permissions_required_view, 'permissions', None),
            )

        with self.subTest('As user with full permissions'):
            # Should succeed and load as expected.

            # Get view.
            request = self.factory.get('/rand')
            setattr(request, 'user', self.full_user)
            response = full_permissions_required_view(request)

            # Display debug information for response.
            self.full_debug_print(response)

            # Check some page content, to ensure we're on the expected page.
            self.assertPageTitle(response, 'Full Permissions Required View | Django AdminLtePdq Testing')
            self.assertPageHeader(response, 'Django AdminLtePdq | Full Permissions Required View Header')

            # Check status code.
            self.assertEqual(response.status_code, 200)

            # Also verify permissions associated with view.
            self.assertIsNone(
                getattr(full_permissions_required_view, 'one_of_permissions', None),
            )
            self.assertEqual(
                ('auth.add_foo', 'auth.change_foo'),
                getattr(full_permissions_required_view, 'permissions', None),
            )


@override_settings(ADMINLTE2_USE_STRICT_POLICY=True)
@override_settings(STRICT_POLICY=True)
@patch('adminlte2_pdq.constants.STRICT_POLICY', True)
@patch('adminlte2_pdq.middleware.STRICT_POLICY', True)
class ReworkedDecoratorTestCase__Strict(IntegrationTestCase):
    """
    Test project authentication decorators, under project "Strict" mode.
    """

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        # Generate test permissions.
        # First permission. Generally used anywhere at least one permission is required.
        Permission.objects.create(
            name="add_foo",
            codename='add_foo',
            content_type=self.permission_content_type,
        )
        # Second permission. Generally used anywhere multiple permissions are required.
        Permission.objects.create(
            name="change_foo",
            codename='change_foo',
            content_type=self.permission_content_type,
        )
        # Third permission. Extra permission that's not explicitly used anywhere.
        # To verify permission logic still works with extra, unrelated permissions in the project.
        Permission.objects.create(
            name="unused_foo",
            codename='unused_foo',
            content_type=self.permission_content_type,
        )

        # Define various permission sets to test against.
        self.full_perms = Permission.objects.filter(codename__in=('add_foo', 'change_foo'))
        self.partial_perms = Permission.objects.filter(codename='add_foo')

        # Add permissions auth.add_foo and auth.change_foo to full_user.
        self.full_user = self.get_user('john_full')
        self.add_user_permission('add_foo', user=self.full_user)
        self.add_user_permission('change_foo', user=self.full_user)

        # Add permission auth.add_foo to partial_user.
        self.partial_user = self.get_user('jane_partial')
        self.add_user_permission('add_foo', user=self.partial_user)

        # Add no permissions to none_user.
        self.none_user = self.get_user('joe_none')

        # Easy access to anonymous user.
        self.anonymous_user = AnonymousUser()

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
