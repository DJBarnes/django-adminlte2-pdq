"""
Tests for Views
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.test import TestCase, RequestFactory
from django.urls import reverse

from adminlte2_pdq import views


UserModel = get_user_model()  # pylint: disable=invalid-name
MOCK_SITE = {"name": "Website", "domain": "www.example.com"}


class ViewsTestCase(TestCase):
    """
    Test Views
    """

    # |-------------------------------------------------------------------------
    # | Setup
    # |-------------------------------------------------------------------------

    def setUp(self):
        self.test_user_no_perms = UserModel()
        self.test_user_no_perms.username = "test_user_no_perms"
        self.test_user_no_perms.set_password("password")
        self.test_user_no_perms.save()

        self.test_user_w_perms = UserModel()
        self.test_user_w_perms.username = "test_user_w_perms"
        self.test_user_w_perms.set_password("password")
        self.test_user_w_perms.save()

        all_permissions = Permission.objects.all()
        for permission in all_permissions:
            self.test_user_w_perms.user_permissions.add(permission)

    # |-------------------------------------------------------------------------
    # | Test that views show correct template
    # |-------------------------------------------------------------------------

    def test_home_view_returns_correct_template(self):
        """Test home view returns correct template"""
        request = RequestFactory().get("home/")
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.home(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")

    def test_register_view_returns_correct_template(self):
        """Test register view returns correct template"""
        request = RequestFactory().get("accounts/register/")
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.register(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_sample_form_view_returns_correct_template(self):
        """Test sample1 view returns correct template"""
        request = RequestFactory().get("sample_form/")
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.sample_form(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the sample form page!")

    def test_sample1_view_returns_correct_template(self):
        """Test sample1 view returns correct template"""
        request = RequestFactory().get("sample1/")
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.sample1(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the sample1 page!")

    def test_sample2_view_returns_correct_template(self):
        """Test sample2 view returns correct template"""
        request = RequestFactory().get("sample2/")
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.sample2(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the sample2 page!")

    def test_demo_view_returns_correct_template(self):
        """Test demo view returns correct template"""
        request = RequestFactory().get("demo-css/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demo CSS")
        self.assertContains(response, "Dropdown Menus")
        self.assertContains(response, "Buttons")
        self.assertContains(response, "Labels")
        self.assertContains(response, "Boxes")
        self.assertContains(response, "Alerts and Callouts")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Tables")

    # |-------------------------------------------------------------------------
    # | Test views work as expected using Client
    # |-------------------------------------------------------------------------

    def test_home_view_works_when_not_authenticated(self):
        """Test home view works when not authenticated"""
        response = self.client.get(
            reverse(getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home")), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")

    def test_register_view_works_when_not_authenticated(self):
        """Test register view works when not authenticated"""
        response = self.client.get(reverse("adminlte2_pdq:register"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_sample_form_view_redirects_to_login_when_not_authenticated(self):
        """Test sample_form view redirects to login when not authenticated"""
        response = self.client.get(reverse("adminlte2_pdq:sample_form"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is the sample_form page!")
        self.assertContains(response, "Username")
        self.assertContains(response, "Login")

    def test_sample1_view_redirects_to_login_when_not_authenticated(self):
        """Test sample1 view redirects to login when not authenticated"""
        response = self.client.get(reverse("adminlte2_pdq:sample1"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is the sample1 page!")
        self.assertContains(response, "Username")
        self.assertContains(response, "Login")

    def test_sample2_view_redirects_to_login_when_not_authenticated(self):
        """Test sample2 view redirects to login when not authenticated"""
        response = self.client.get(reverse("adminlte2_pdq:sample2"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is the sample2 page!")
        self.assertContains(response, "Username")
        self.assertContains(response, "Login")

    def test_sample1_view_redirects_to_login_when_authenticated_with_incorrect_permissions(self):
        """Test sample1 view redirects to login when authenticated with incorrect permissions"""
        self.client.force_login(self.test_user_no_perms)
        response = self.client.get(reverse("adminlte2_pdq:sample1"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is the sample1 page!")
        self.assertContains(response, "Username")
        self.assertContains(response, "Login")

    def test_sample2_view_redirects_to_login_when_authenticated_with_incorrect_permissions(self):
        """Test sample2 view redirects to login when authenticated with incorrect permissions"""
        self.client.force_login(self.test_user_no_perms)
        response = self.client.get(reverse("adminlte2_pdq:sample2"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is the sample2 page!")
        self.assertContains(response, "Username")
        self.assertContains(response, "Login")

    def test_sample_form_view_works_when_authenticated_with_no_permissions(self):
        """Test sample_form view works when authenticated with no permissions"""
        self.client.force_login(self.test_user_no_perms)
        response = self.client.get(reverse("adminlte2_pdq:sample_form"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the sample form page!")
        self.assertNotContains(response, "Username")

    def test_sample1_view_works_when_authenticated_with_correct_permissions(self):
        """Test sample1 view works when authenticated with correct permissions"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(reverse("adminlte2_pdq:sample1"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the sample1 page!")
        self.assertNotContains(response, "Username")

    def test_sample2_view_works_when_authenticated_with_correct_permissions(self):
        """Test sample2 view works when authenticated with correct permissions"""
        self.client.force_login(self.test_user_w_perms)
        response = self.client.get(reverse("adminlte2_pdq:sample2"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the sample2 page!")
        self.assertNotContains(response, "Username")

    def test_404_view_works_when_triggered(self):
        """Test 404 view works when triggered"""
        self.client.force_login(self.test_user_no_perms)
        response = self.client.get("unknown/route/")
        self.assertEqual(response.status_code, 302)

    def test_404_view_works_when_triggered_and_followed(self):
        """Test 404 view works when triggered"""
        self.client.force_login(self.test_user_no_perms)
        response = self.client.get("unknown/route/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The page you were looking for does not exist")
