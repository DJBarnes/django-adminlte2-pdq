"""
Tests for Views
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
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

    def test_sample_views_link_to_the_adminlte_demo_and_demo_css(self):
        """The home and sample pages link to the official AdminLTE demo and the Demo CSS pages"""
        for view in (views.home, views.sample_form, views.sample1, views.sample2):
            with self.subTest(view.__name__):
                request = RequestFactory().get("/")
                request.user = self.test_user_w_perms
                request.site = MOCK_SITE
                response = view(request)
                self.assertContains(response, 'href="https://adminlte.io/themes/AdminLTE/index2.html"')
                self.assertContains(response, f'href="{reverse("adminlte2_pdq:demo-css")}"')

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

    @override_settings(DEBUG=True)
    @patch("adminlte2_pdq.middleware.RESPONSE_404_DEBUG_MESSAGE", "")
    def test_404_view_works_when_triggered_and_followed_in_dev_and_no_message_set(self):
        """Test 404 view works when triggered in dev with no message set"""

        self.client.force_login(self.test_user_no_perms)

        response = self.client.get("unknown/route/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "AdminLtePdq Warning: The page you were looking for does not exist.")

    @override_settings(DEBUG=False)
    def test_404_view_works_when_triggered_and_followed_in_prod(self):
        """Test 404 view works when triggered"""

        self.client.force_login(self.test_user_no_perms)

        response = self.client.get("unknown/route/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            (
                "Unable to locate the requested page. "
                "If you believe this was an error, please contact the site administrator."
            ),
        )

    @override_settings(DEBUG=False)
    @patch("adminlte2_pdq.middleware.RESPONSE_404_PRODUCTION_MESSAGE", "")
    def test_404_view_works_when_triggered_and_followed_in_prod_and_no_message_set(self):
        """Test 404 view works when triggered"""

        self.client.force_login(self.test_user_no_perms)

        response = self.client.get("unknown/route/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            (
                "Unable to locate the requested page. "
                "If you believe this was an error, please contact the site administrator."
            ),
        )


# Demo CSS pages: (URL name, template, text that only appears on that page).
DEMO_CSS_PAGES = [
    ("demo-css", "adminlte2_demo_css/home.html", '<h3 class="box-title">Welcome!</h3>'),
    ("demo-css-typography", "adminlte2_demo_css/typography.html", "Preview of Typography Elements"),
    ("demo-css-widgets", "adminlte2_demo_css/widgets.html", "Widgets"),
    ("demo-css-ui-general", "adminlte2_demo_css/ui_general.html", "color-palette-box"),
    ("demo-css-alerts", "adminlte2_demo_css/alerts.html", "This is a debug message via the messages framework."),
    ("demo-css-buttons-basic", "adminlte2_demo_css/buttons_basic.html", "Buttons"),
    ("demo-css-buttons-specialized", "adminlte2_demo_css/buttons_specialized.html", "btn-app"),
    ("demo-css-carousels", "adminlte2_demo_css/carousels.html", "carousel-indicators"),
    ("demo-css-labels", "adminlte2_demo_css/labels.html", "data-tooltip-color"),
    ("demo-css-modals", "adminlte2_demo_css/modals.html", "modal-dialog"),
    ("demo-css-boxes-standard", "adminlte2_demo_css/boxes_standard.html", "box-header"),
    ("demo-css-boxes-solid", "adminlte2_demo_css/boxes_solid.html", "box-solid"),
    ("demo-css-tables", "adminlte2_demo_css/tables.html", "table-border-"),
    ("demo-css-forms", "adminlte2_demo_css/forms.html", "<form"),
    ("demo-css-full-span-links", "adminlte2_demo_css/full_span_links.html", "full-span-link"),
]

# Sidebar entries every demo page shows.
DEMO_CSS_MENU_TEXT = [
    "Demo CSS Home",
    "Typography",
    "Widgets",
    "UI Elements",
    "Buttons | Basic",
    "Buttons | Specialized",
    "Labels &amp; Tooltips",
    "Full-Span Links",
    "Boxes | Standard",
    "Boxes | Solid",
    "Tables",
    "Forms",
]


class DemoCssViewsTestCase(TestCase):
    """Tests for the demo CSS pages."""

    def test__pages_render(self):
        """Each demo page renders its template, its content, and the demo menu."""
        for url_name, template_name, page_text in DEMO_CSS_PAGES:
            with self.subTest(url_name):
                response = self.client.get(reverse(f"adminlte2_pdq:{url_name}"))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self.assertContains(response, page_text)
                for menu_text in DEMO_CSS_MENU_TEXT:
                    self.assertContains(response, menu_text)
                # The default menu's sections are included when their routes exist.
                self.assertContains(response, "Change Password")

    def test__breadcrumbs_link_back_to_the_demo_home(self):
        """Each demo page's breadcrumbs link to the demo home and end with the page's name."""
        demo_home_link = f'<a href="{reverse("adminlte2_pdq:demo-css")}">Demo CSS</a>'
        for url_name, _template_name, _page_text in DEMO_CSS_PAGES:
            with self.subTest(url_name):
                response = self.client.get(reverse(f"adminlte2_pdq:{url_name}"))
                breadcrumbs = response.content.decode().split('<ol class="breadcrumb">', 1)[1].split("</ol>", 1)[0]

                if url_name == "demo-css":
                    self.assertNotIn(demo_home_link, breadcrumbs)
                    self.assertIn('<li class="active">', breadcrumbs)
                else:
                    self.assertIn(demo_home_link, breadcrumbs)
                    page_name = breadcrumbs.split('<li class="active">', 1)[1].split("</li>", 1)[0].strip()
                    self.assertTrue(page_name)

    def test__colors_are_listed(self):
        """Pages show every color from ADMINLTE2_DEMO_CSS_COLORS."""
        response = self.client.get(reverse("adminlte2_pdq:demo-css-ui-general"))

        # Bootstrap's contextual colors use AdminLTE's `bg-*` names.
        for bg_name in ("light-blue", "aqua", "navy", "indigo", "black"):
            self.assertContains(response, f"bg-{bg_name} color-palette")
        self.assertContains(response, "#0073b7")

    @override_settings(ROOT_URLCONF="tests.django_adminlte2_pdq.django_test_project.urls_without_auth")
    def test__pages_render_without_password_change_url(self):
        """Without the password change URL, demo pages render and leave out the default menu's sections."""
        for url_name, _template_name, _page_text in DEMO_CSS_PAGES:
            with self.subTest(url_name):
                response = self.client.get(reverse(f"adminlte2_pdq:{url_name}"))

                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "Change Password")
