"""
Tests for Mixins
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.views import View

from django_adminlte2.mixins import PermissionRequiredMixin

UserModel = get_user_model()


class MixinTestCase(TestCase):
    """
    Test Mixins
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

    def test_mixin_works_with_permission_required_defined(self):
        """Test mixin works with permission required defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""
            permission_required = ['auth.add_foo']

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_works_with_permission_required_one_defined(self):
        """Test mixing works with permission required one defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""
            permission_required_one = ['auth.add_foo']

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_has_error_when_no_permissions_defined(self):
        """Test mixin has error when no permissions defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        with self.assertRaises(ImproperlyConfigured):

            request = self.factory.get('/rand')
            setattr(request, 'user', self.full_user)
            TestView.as_view()(request)
