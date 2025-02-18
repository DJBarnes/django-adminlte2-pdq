"""Django AdminLTE2 default Sidebar menu."""

# Third-Party Imports.
from django.conf import settings


# Default Menu
# NOTE: If this default menu is updated to include new routes,
# there is code in 'sidebar_menu.py' file that also needs to be updated.
MENU = [
    {
        "text": "Home",
        "nodes": [
            {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Dashboard",
                "icon": "fa fa-dashboard",
            },
            {
                "route": "adminlte2_pdq:demo-css",
                "text": "Demo CSS",
                "icon": "fa fa-file",
            },
        ],
    },
    {
        "text": "Profile",
        "nodes": [
            {
                "route": "password_change",
                "text": "Change Password",
                "icon": "fa fa-lock",
            }
        ],
    },
    {
        "text": "Samples",
        "nodes": [
            {
                "route": "adminlte2_pdq:sample_form",
                "text": "Sample Form",
                "icon": "fa fa-list-alt",
            },
            {
                "route": "adminlte2_pdq:sample1",
                "text": "Sample1",
                "icon": "fa fa-group",
            },
            {
                "text": "Sample Tree",
                "icon": "fa fa-leaf",
                "nodes": [
                    {
                        "route": "adminlte2_pdq:sample2",
                        "text": "Sample2",
                        "icon": "fa fa-building",
                    },
                ],
            },
        ],
    },
]


# Used only on the demo-css pages.
CSS_MENU = [
    {
        "text": "Home",
        "nodes": [
            {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Dashboard",
                "icon": "fa fa-dashboard",
            },
            {
                "text": "Demo CSS",
                "nodes": [
                    {
                        "text": "Original / Old",
                        "nodes": [
                            {
                                "route": "adminlte2_pdq:demo-css",
                                "text": "Demo CSS | Home",
                                "icon": "fa fa-home",
                            },
                            {
                                "route": "adminlte2_pdq:demo-css-boxes",
                                "text": "Demo CSS | Boxes",
                                "icon": "fa fa-square",
                            },
                        ],
                    },
                    {
                        "route": "adminlte2_pdq:demo-css",
                        "text": "Demo CSS Home",
                        "icon": "fa fa-home",
                    },
                    {
                        "route": "adminlte2_pdq:demo-css-widgets",
                        "text": "Widgets",
                        "icon": "fa fa-th",
                    },
                    {
                        "text": "UI Elements",
                        "nodes": [
                            {
                                "route": "adminlte2_pdq:demo-css-ui-general",
                                "text": "General",
                                "icon": "fa fa-circle-o",
                            },
                            {
                                "route": "adminlte2_pdq:demo-css-alerts",
                                "text": "Alerts",
                                "icon": "fa fa-circle-o",
                            },
                            {
                                "route": "adminlte2_pdq:demo-css-buttons-basic",
                                "text": "Buttons | Basic",
                                "icon": "fa fa-circle-o",
                            },
                            {
                                "route": "adminlte2_pdq:demo-css-buttons-specialized",
                                "text": "Buttons | Specialized",
                                "icon": "fa fa-circle-o",
                            },
                            {
                                "route": "adminlte2_pdq:demo-css-labels",
                                "text": "Labels & Tooltips",
                                "icon": "fa fa-circle-o",
                            },
                            {
                                "route": "adminlte2_pdq:demo-css-modals",
                                "text": "Modals",
                                "icon": "fa fa-circle-o",
                            },
                        ],
                        "icon": "fa fa-laptop",
                    },
                    {
                        "route": "adminlte2_pdq:demo-css-tables",
                        "text": "Tables",
                        "icon": "fa fa-table",
                    },
                ],
            },
        ],
    },
    {
        "text": "Profile",
        "nodes": [
            {
                "route": "password_change",
                "text": "Change Password",
                "icon": "fa fa-lock",
            }
        ],
    },
    {
        "text": "Samples",
        "nodes": [
            {
                "route": "adminlte2_pdq:sample_form",
                "text": "Sample Form",
                "icon": "fa fa-list-alt",
            },
            {
                "route": "adminlte2_pdq:sample1",
                "text": "Sample1",
                "icon": "fa fa-group",
            },
            {
                "text": "Sample Tree",
                "icon": "fa fa-leaf",
                "nodes": [
                    {
                        "route": "adminlte2_pdq:sample2",
                        "text": "Sample2",
                        "icon": "fa fa-building",
                    },
                ],
            },
        ],
    },
]
