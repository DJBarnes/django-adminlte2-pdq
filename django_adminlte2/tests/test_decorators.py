"""
Tests for Decorators
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django_adminlte2.decorators import (
    requires_all_permissions,
    requires_one_permission
)

UserModel = get_user_model()


class DecoratorTestCase(TestCase):
    """
    Test Decorators
    """

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(
            Permission
        )
        self.factory = RequestFactory()

        Permission.objects.create(
            name="add_foo",
            codename='add_foo',
            content_type=self.permission_content_type
        )
        Permission.objects.create(
            name="change_foo",
            codename='change_foo',
            content_type=self.permission_content_type
        )
        # Add permissions auth.add_foo and auth.change_foo to full_user
        full_perms = Permission.objects.filter(
            codename__in=(
                'add_foo',
                'change_foo'
            )
        )
        self.full_user = UserModel.objects.create(
            username='johnfull',
            password='qwerty'
        )
        self.full_user.user_permissions.add(*full_perms)

        # Add permission auth.add_foo to partial_user
        partial_perms = Permission.objects.filter(
            codename='add_foo'
        )

        self.partial_user = UserModel.objects.create(
            username='janepartial',
            password='qwerty'
        )
        self.partial_user.user_permissions.add(*partial_perms)

        # Add no permissions to none_user
        self.none_user = UserModel.objects.create(
            username='joenone',
            password='qwerty'
        )

    # |--------------------------------------------------------------------------
    # | Test requires_one_permission
    # |--------------------------------------------------------------------------

    def test_requires_one_permission_works_when_permission_is_a_string(self):
        """Test requires one permission works when permission is a string"""

        @requires_one_permission('auth.add_foo')
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.one_of_permissions,
            (
                'auth.add_foo',
            )
        )

    def test_requires_one_permission_works_when_user_has_all(self):
        """Test requires one permission work when user has all"""

        @requires_one_permission(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.one_of_permissions,
            (
                'auth.add_foo',
                'auth.change_foo'
            )
        )

    def test_requires_one_permission_works_when_user_has_one(self):
        """Test requires one permission works when user has one"""

        @requires_one_permission(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.partial_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.one_of_permissions,
            (
                'auth.add_foo',
                'auth.change_foo'
            )
        )

    def test_requires_one_permission_works_when_user_has_none(self):
        """Test requires one permission works when user has none"""

        @requires_one_permission(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.none_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            a_view.one_of_permissions,
            (
                'auth.add_foo',
                'auth.change_foo'
            )
        )

    def test_requires_one_permission_works_when_user_has_none_and_raise_exception(self):
        """Test requires one permission works when user has none and raise exception"""

        @requires_one_permission(('auth.add_foo', 'auth.change_foo'), raise_exception=True)
        def a_view(request):
            return HttpResponse('foobar')

        with self.assertRaises(PermissionDenied):

            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = a_view(request)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                a_view.one_of_permissions,
                (
                    'auth.add_foo',
                    'auth.change_foo'
                )
            )

    # |--------------------------------------------------------------------------
    # | Test requires_all_permissions
    # |--------------------------------------------------------------------------

    def test_requires_all_permissions_works_when_permission_is_a_string(self):
        """Test requires all permissions works when permission is a string"""

        @requires_all_permissions('auth.add_foo')
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.permissions,
            (
                'auth.add_foo',
            )
        )

    def test_requires_all_permissions_works_when_user_has_all(self):
        """Test requires all permissions works when user has all"""

        @requires_all_permissions(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            a_view.permissions,
            (
                'auth.add_foo',
                'auth.change_foo'
            )
        )

    def test_requires_all_permissions_works_when_user_has_one(self):
        """Test requires all permissions works when user has one"""

        @requires_all_permissions(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.partial_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            a_view.permissions,
            (
                'auth.add_foo',
                'auth.change_foo'
            )
        )

    def test_requires_all_permissions_works_when_user_has_none(self):
        """Test requires all permissions works when user has none"""

        @requires_all_permissions(('auth.add_foo', 'auth.change_foo'))
        def a_view(request):
            return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.none_user)
        response = a_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            a_view.permissions,
            (
                'auth.add_foo',
                'auth.change_foo'
            )
        )

    def test_requires_all_permissions_works_when_user_has_none_and_raise_exception(self):
        """Test requires all permissions works when user has none and raise exception"""

        @requires_all_permissions(('auth.add_foo', 'auth.change_foo'), raise_exception=True)
        def a_view(request):
            return HttpResponse('foobar')

        with self.assertRaises(PermissionDenied):

            request = self.factory.get('/rand')
            setattr(request, 'user', self.none_user)
            response = a_view(request)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                a_view.permissions,
                (
                    'auth.add_foo',
                    'auth.change_foo'
                )
            )
