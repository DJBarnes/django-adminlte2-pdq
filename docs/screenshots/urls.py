"""
URLs for the docs screenshots: the test project's URLs, plus the example pages from the templates docs.
"""

# Third-Party Imports.
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path("reports/monthly/", TemplateView.as_view(template_name="reports/monthly_report.html"), name="monthly_report"),
    # The user dropdown example links to a profile page.
    path("profile/", TemplateView.as_view(template_name="adminlte2/home.html"), name="profile"),
    path("", include("tests.django_adminlte2_pdq.django_test_project.urls")),
]
