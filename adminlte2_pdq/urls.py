"""
Django AdminLTE2 Default URL Configuration
"""

# Third-Party Imports.
from django.conf import settings
from django.urls import include, path
from django.views.generic import RedirectView

# Internal Imports.
from . import views


app_name = "adminlte2_pdq"
urlpatterns = [
    # Sample pages.
    path("home/", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("sample_form/", views.sample_form, name="sample_form"),
    path("sample1/", views.sample1, name="sample1"),
    path("sample2/", views.sample2, name="sample2"),
    # Demo CSS pages.
    path(
        "demo-css/",
        include(
            [
                path("boxes/standard/", views.demo_css_boxes_standard, name="demo-css-boxes-standard"),
                path("boxes/solid/", views.demo_css_boxes_solid, name="demo-css-boxes-solid"),
                path("tables/", views.demo_css_tables, name="demo-css-tables"),
                path(
                    "ui/",
                    include(
                        [
                            path("general/", views.demo_css_ui_general, name="demo-css-ui-general"),
                            path("alerts/", views.demo_css_alerts, name="demo-css-alerts"),
                            path("buttons/basic/", views.demo_css_buttons_basic, name="demo-css-buttons-basic"),
                            path(
                                "buttons/specialized/",
                                views.demo_css_buttons_specialized,
                                name="demo-css-buttons-specialized",
                            ),
                            path("labels/", views.demo_css_labels, name="demo-css-labels"),
                            path("modals/", views.demo_css_modals, name="demo-css-modals"),
                        ]
                    ),
                ),
                path("widgets/", views.demo_css_widgets, name="demo-css-widgets"),
                path("", views.demo_css, name="demo-css"),
            ]
        ),
    ),
    # 404 view. Required to make some logic importing behave as expected.
    path("view-404/", views.view_404, name="view-404"),
    # Redirects to the home page.
    path(
        "",
        RedirectView.as_view(
            pattern_name=getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
            permanent=False,
        ),
    ),
]
