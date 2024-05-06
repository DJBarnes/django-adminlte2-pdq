"""
Tests for Mixins
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.views import View

from adminlte2_pdq.mixins import LoginRequiredMixin, PermissionRequiredMixin


UserModel = get_user_model()


class MixinTestCase(TestCase):
    """
    Test Mixins
    """

    def setUp(self):
        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        Permission.objects.create(
            name="add_foo",
            codename='add_foo',
            content_type=self.permission_content_type,
        )
        Permission.objects.create(
            name="change_foo",
            codename='change_foo',
            content_type=self.permission_content_type,
        )
        # Add permissions auth.add_foo and auth.change_foo to full_user
        full_perms = Permission.objects.filter(codename__in=('add_foo', 'change_foo'))
        self.user = UserModel.objects.create(username='john', password='qwerty')
        self.full_user = UserModel.objects.create(username='johnfull', password='qwerty')
        self.full_user.user_permissions.add(*full_perms)

        self.anonymous_user = AnonymousUser()

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

    def test_mixin_works_with_permission_required_defined_as_string(self):
        """Test mixin works with permission required defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = 'auth.add_foo'

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

    def test_mixin_works_with_permission_required_one_defined_as_string(self):
        """Test mixing works with permission required one defined"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = 'auth.add_foo'

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_mixin_prevents_access_for_no_perms_all(self):
        """Test mixin prevents access for no perms all"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required = 'auth.add_foo'

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        with self.assertRaises(PermissionDenied):
            request = self.factory.get('/rand')
            setattr(request, 'user', self.user)
            TestView.as_view()(request)

    def test_mixin_prevents_access_for_no_perms_one(self):
        """Test mixin prevents access for no perms one"""

        class TestView(PermissionRequiredMixin, View):
            """Test View Class"""

            permission_required_one = 'auth.add_foo'

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        with self.assertRaises(PermissionDenied):
            request = self.factory.get('/rand')
            setattr(request, 'user', self.user)
            TestView.as_view()(request)

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

    # |-------------------------------------------------------------------------
    # | Test login_required
    # |-------------------------------------------------------------------------

    def test_login_required_mixin_works(self):
        """Test login_required mixin works"""

        class TestView(LoginRequiredMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.full_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_login_required_mixin_works_when_user_not_logged_in(self):
        """Test login_required mixin works when user not logged in"""

        class TestView(LoginRequiredMixin, View):
            """Test View Class"""

            def get(self, request):
                """Test get method"""
                return HttpResponse('foobar')

        request = self.factory.get('/rand')
        setattr(request, 'user', self.anonymous_user)
        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)
