"""
Tests for Views
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.test import override_settings, RequestFactory, TestCase
from django.urls import reverse

# Internal Imports.
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

    # region Demo CSS Views

    def test_demo_css_home_view_returns_correct_template(self):
        """Test Demo CSS Home view returns correct template"""

        request = RequestFactory().get("demo-css/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")
        self.assertContains(response, '<h3 class="box-title">Welcome!</h3>')

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css__view_returns_correct_template(self):
        """Test Demo CSS  view returns correct template"""

        request = RequestFactory().get("demo-css/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(response, "<h1>Demo CSS <small>Home</small></h1>")
        self.assertContains(response, '<h3 class="box-title">Welcome!</h3>')

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_typography_view_returns_correct_template(self):
        """Test Demo CSS Typography view returns correct template"""

        request = RequestFactory().get("demo-css/typography/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_typography(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Typography
    <small>Preview of Typography Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_widgets_view_returns_correct_template(self):
        """Test Demo CSS Widgets view returns correct template"""

        request = RequestFactory().get("demo-css/widgets/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_widgets(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Widgets
    <small>Preview of Widget Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_ui_general_view_returns_correct_template(self):
        """Test Demo CSS UI (General) view returns correct template"""

        request = RequestFactory().get("demo-css/ui/general/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_ui_general(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    General UI
    <small>Preview of UI Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_alerts_view_returns_correct_template(self):
        """Test Demo CSS Alerts view returns correct template"""

        request = RequestFactory().get("demo-css/ui/alerts")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_alerts(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Alerts and Callouts
    <small>Preview of Alert & Callout Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_buttons_basic_view_returns_correct_template(self):
        """Test Demo CSS Buttons (Basic) view returns correct template"""

        request = RequestFactory().get("demo-css/ui/buttons/basic/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_buttons_basic(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Buttons (Basic)
    <small>Preview of Button Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_buttons_specialized_view_returns_correct_template(self):
        """Test Demo CSS Buttons (Specialized) view returns correct template"""

        request = RequestFactory().get("demo-css/ui/buttons/specialized/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_buttons_specialized(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Buttons (Specialized)
    <small>Preview of Specialized Button Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_carousel_view_returns_correct_template(self):
        """Test Demo CSS Carousel view returns correct template"""

        request = RequestFactory().get("demo-css/ui/carousels/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_carousels(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Carousels
    <small>Preview of Carousel Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_labels_view_returns_correct_template(self):
        """Test Demo CSS Labels view returns correct template"""

        request = RequestFactory().get("demo-css/ui/labels/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_labels(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Labels & Tooltips
    <small>Preview of Label & Tooltip Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_modals_view_returns_correct_template(self):
        """Test Demo CSS  view returns correct template"""

        request = RequestFactory().get("demo-css/modals/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_modals(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Modals
    <small>Preview of Modal Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_boxes_standard_view_returns_correct_template(self):
        """Test Demo CSS Boxes (Solid) view returns correct template"""

        request = RequestFactory().get("demo-css/boxes/standard/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_boxes_standard(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Boxes
    <small>Preview of Box Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_boxes_solid_view_returns_correct_template(self):
        """Test Demo CSS Boxes (Solid) view returns correct template"""

        request = RequestFactory().get("demo-css/boxes/solid/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_boxes_solid(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Boxes
    <small>Preview of Solid Box Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    def test_demo_css_tables_view_returns_correct_template(self):
        """Test Demo CSS Tables view returns correct template"""

        request = RequestFactory().get("demo-css/tables/")
        request._messages = messages.storage.default_storage(request)
        request.user = self.test_user_w_perms
        request.site = MOCK_SITE
        response = views.demo_css_tables(request)
        self.assertEqual(response.status_code, 200)

        # Check for page title content.
        self.assertContains(
            response,
            """
  <h1>
    Demo CSS
    &nbsp; &#124; &nbsp;
    Tables
    <small>Preview of Table Elements</small>
  </h1>
            """.strip(),
        )

        # Check for expected page link elements.
        self.assertContains(response, "Demo CSS Home")
        self.assertContains(response, "Typography")
        self.assertContains(response, "Widgets")
        self.assertContains(response, "UI Elements")
        self.assertContains(response, "General")
        self.assertContains(response, "Alerts")
        self.assertContains(response, "Buttons | Basic")
        self.assertContains(response, "Buttons | Specialized")
        self.assertContains(response, "Carousels")
        self.assertContains(response, "Labels &amp; Tooltips")
        self.assertContains(response, "Modals")
        self.assertContains(response, "Boxes | Standard")
        self.assertContains(response, "Boxes | Solid")
        self.assertContains(response, "Tables")

    # endregion Demo CSS Views

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
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Visitors Report")

    def test_sample2_view_redirects_to_login_when_authenticated_with_incorrect_permissions(self):
        """Test sample2 view redirects to login when authenticated with incorrect permissions"""
        self.client.force_login(self.test_user_no_perms)
        response = self.client.get(reverse("adminlte2_pdq:sample2"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "This is the sample2 page!")
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Visitors Report")

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

    @override_settings(DEBUG=True)
    def test_404_view_works_when_triggered_and_followed_in_dev(self):
        """Test 404 view works when triggered"""

        self.client.force_login(self.test_user_no_perms)

        response = self.client.get("unknown/route/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AdminLtePdq Warning: The page you were looking for does not exist.")

    @override_settings(DEBUG=False)
    def test_404_view_works_when_triggered_and_followed_in_prod(self):
        """Test 404 view works when triggered"""

        self.client.force_login(self.test_user_no_perms)

        response = self.client.get("unknown/route/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            (
                "Could not access the requested page. "
                "If you believe this was an error, please contact the site administrator."
            ),
        )
