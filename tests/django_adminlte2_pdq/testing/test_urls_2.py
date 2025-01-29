"""
Project testing views.
These urls exist to reliably test the two settings:
 * ADMINLTE2_APP_WIDE_LOGIN_EXEMPT_WHITELIST
 * ADMINLTE2_APP_WIDE_STRICT_POLICY_WHITELIST
without having potential side-effects on other existing tests.
"""

# Third-Party Imports.
from django.urls import include, path

# Internal Imports.
from . import views


app_name = "adminlte2_pdq_tests_2"
urlpatterns = [
    path("standard-1/", views.standard_view, name="standard-1"),
    path("standard-2/", views.standard_view, name="standard-2"),
    path("standard-3/", views.standard_view, name="standard-3"),
]
