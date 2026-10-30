"""
Tests for rendering the sidebar menu.
"""

# System Imports.

# Third-party Imports.
from django.template import Template, Context
from django.test import override_settings, RequestFactory
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from tests.django_adminlte2_pdq.tests.core.menu.base_test_case import SidebarMenuBaseTestCase


# Module Variables.


class SidebarRenderTestCase(SidebarMenuBaseTestCase):
    """Tests for expected rendering of the Template Tag Sidebar Menu."""

    def test__render_types(self):
        """Test render types"""
        with self.subTest("Render section - standard"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            section = {
                "text": "Samples",
                "nodes": [
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
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "section": section,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_section section %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<li class="header">', rendered_template)
            self.assertIn("Samples", rendered_template)
            self.assertIn('<li class="treeview active">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)

        with self.subTest("Render nodes - Standard"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            nodes = [
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
            ]

            context = Context(
                {
                    "user": self.staff_user,
                    "nodes": nodes,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_nodes nodes %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<li class="treeview active">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)

        with self.subTest("Render tree - Standard"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            node = {
                "text": "Sample Tree",
                "icon": "fa fa-leaf",
                "nodes": [
                    {
                        "route": "adminlte2_pdq:sample2",
                        "text": "Sample2",
                        "icon": "fa fa-building",
                    },
                ],
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_tree node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<li class="treeview active">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)

        with self.subTest("Render tree - Node lacks icon"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            node = {
                "text": "Sample Tree",
                "nodes": [
                    {
                        "route": "adminlte2_pdq:sample2",
                        "text": "Sample2",
                        "icon": "fa fa-building",
                    },
                ],
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_tree node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<li class="treeview active">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertNotIn("fa fa-leaf", rendered_template)
            self.assertIn("not-found", rendered_template)

        with self.subTest("Render tree - Root has a route"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            node = {
                "route": "adminlte2_pdq:sample1",
                "text": "Sample Tree",
                "icon": "fa fa-leaf",
                "nodes": [
                    {
                        "route": "adminlte2_pdq:sample2",
                        "text": "Sample2",
                        "icon": "fa fa-building",
                    },
                ],
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_tree node %}")

            rendered_template = " ".join(template_to_render.render(context).split())

            # The root is a plain link, and the toggle is a separate element right before the menu,
            # which is the element AdminLTE's tree code toggles.
            self.assertIn('<li class="treeview treeview-split active">', rendered_template)
            self.assertIn('<a href="/sample1/" class="node-link" >', rendered_template)
            self.assertIn('class="treeview-toggle"', rendered_template)
            self.assertRegex(rendered_template, r'class="treeview-toggle".*?</a> <ul class="treeview-menu"')
            self.assertNotIn("pull-right-container", rendered_template.split('class="treeview-toggle"')[0])

        with self.subTest("Render tree - Root without a route has no separate toggle"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            node = {
                "text": "Sample Tree",
                "icon": "fa fa-leaf",
                "nodes": [
                    {
                        "route": "adminlte2_pdq:sample2",
                        "text": "Sample2",
                        "icon": "fa fa-building",
                    },
                ],
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_tree node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<li class="treeview active">', rendered_template)
            self.assertNotIn("treeview-toggle", rendered_template)

        with self.subTest("Render tree - Nested tree lacks route"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            node = {
                "text": "Outer Tree",
                "icon": "fa fa-leaf",
                "nodes": [
                    {
                        "text": "Inner Tree",
                        "icon": "fa fa-tree",
                        "nodes": [
                            {
                                "route": "adminlte2_pdq:sample2",
                                "text": "Sample2",
                                "icon": "fa fa-building",
                            },
                        ],
                    },
                ],
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_tree node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-tree", rendered_template)
            self.assertEqual(node["nodes"][0]["url"], "#")

        with self.subTest("Render link - Standard"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/some/path/")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)

        with self.subTest("Render link - No icon provided"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/some/path/")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertNotIn("fa fa-building", rendered_template)

        with self.subTest("Render link - Dynamic text via string"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/some/path/")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "hook": "tests.django_adminlte2_pdq.django_test_project.utils.valid_string_hook_function",
                "hook_args": ["foo"],
                "hook_kwargs": {"kwarg1": "bar"},
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn(
                '<span class="node-link-text" title="foobar foo bar">foobar foo bar</span>', rendered_template
            )
            self.assertNotIn("fa fa-building", rendered_template)

        with self.subTest("Render link - Dynamic text via tuple"):
            self._setup_staff_user("add_permission")

            request = RequestFactory().get("/some/path/")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "hook": "tests.django_adminlte2_pdq.django_test_project.utils.valid_tuple_hook_function",
                "hook_args": ["foo"],
                "hook_kwargs": {"kwarg1": "bar"},
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="foo bar">foobar</span>', rendered_template)
            self.assertNotIn("fa fa-building", rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=False)
    def test__user_has_access_and_admin_include_is_off(self):
        """Test user has access to admin include is off"""
        self._setup_staff_user(
            [
                "add_permission",
                "change_permission",
                "delete_permission",
                "add_user",
                "change_user",
                "delete_user",
            ]
        )

        request = RequestFactory().get("/sample2/")
        request.user = self.staff_user

        menu = [
            {
                "text": "Samples",
                "nodes": [
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
            }
        ]

        context = Context(
            {
                "user": self.staff_user,
                "ADMINLTE2_MENU": menu,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}{% render_menu %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("Authentication", rendered_template)
        self.assertNotIn("<span>User</span>", rendered_template)
        self.assertIn('<li class="header">', rendered_template)
        self.assertIn("Samples", rendered_template)
        self.assertIn('<li class="treeview active">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=True)
    def test__user_has_access_and_admin_include_is_on(self):
        """Test user has access and admin include is on"""

        with self.subTest("With menu not first"):
            self._setup_staff_user(
                [
                    "add_permission",
                    "change_permission",
                    "delete_permission",
                    "add_user",
                    "change_user",
                    "delete_user",
                ]
            )

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            menu = [
                {
                    "text": "Samples",
                    "nodes": [
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
                }
            ]

            context = Context(
                {
                    "user": self.staff_user,
                    "ADMINLTE2_MENU": menu,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_menu %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Authentication", rendered_template)
            self.assertIn('<span class="node-link-text" title="User">User</span>', rendered_template)
            self.assertIn("Home", rendered_template)
            self.assertIn('<li class="header">', rendered_template)
            self.assertIn("Samples", rendered_template)
            self.assertIn('<li class="treeview treeview-split">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)

        with self.subTest("With menu first"):
            self._setup_staff_user(
                [
                    "add_permission",
                    "change_permission",
                    "delete_permission",
                    "add_user",
                    "change_user",
                    "delete_user",
                ]
            )

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            menu = [
                {
                    "text": "Samples",
                    "nodes": [
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
                }
            ]

            menu_first = [
                {
                    "text": "First",
                    "nodes": [
                        {
                            "route": "adminlte2_pdq:sample1",
                            "text": "Sample1",
                            "icon": "fa fa-building",
                        }
                    ],
                }
            ]

            context = Context(
                {
                    "user": self.staff_user,
                    "ADMINLTE2_MENU": menu,
                    "ADMINLTE2_MENU_FIRST": menu_first,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_menu %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Authentication", rendered_template)
            self.assertIn('<span class="node-link-text" title="User">User</span>', rendered_template)
            self.assertIn("Home", rendered_template)
            self.assertIn('<li class="header">', rendered_template)
            self.assertIn("Samples", rendered_template)
            self.assertIn('<li class="treeview treeview-split">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)
            self.assertIn('<li class="separator">', rendered_template)

        with self.subTest("With menu last"):
            self._setup_staff_user(
                [
                    "add_permission",
                    "change_permission",
                    "delete_permission",
                    "add_user",
                    "change_user",
                    "delete_user",
                ]
            )

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            menu = [
                {
                    "text": "Samples",
                    "nodes": [
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
                }
            ]

            menu_last = [
                {
                    "text": "Last",
                    "nodes": [
                        {
                            "route": "adminlte2_pdq:sample1",
                            "text": "Sample1",
                            "icon": "fa fa-building",
                        }
                    ],
                }
            ]

            context = Context(
                {
                    "user": self.staff_user,
                    "ADMINLTE2_MENU": menu,
                    "ADMINLTE2_MENU_LAST": menu_last,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_menu %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Authentication", rendered_template)
            self.assertIn('<span class="node-link-text" title="User">User</span>', rendered_template)
            self.assertIn("Home", rendered_template)
            self.assertIn('<li class="header">', rendered_template)
            self.assertIn("Samples", rendered_template)
            self.assertIn('<li class="treeview treeview-split">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)
            self.assertIn('<li class="separator">', rendered_template)

        with self.subTest("With menu first and last"):
            self._setup_staff_user(
                [
                    "add_permission",
                    "change_permission",
                    "delete_permission",
                    "add_user",
                    "change_user",
                    "delete_user",
                ]
            )

            request = RequestFactory().get("/sample2/")
            request.user = self.staff_user

            menu = [
                {
                    "text": "Samples",
                    "nodes": [
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
                }
            ]

            menu_first = [
                {
                    "text": "First",
                    "nodes": [
                        {
                            "route": "adminlte2_pdq:demo-css",
                            "text": "DemoCSS",
                            "icon": "fa fa-building-o",
                        }
                    ],
                }
            ]

            menu_last = [
                {
                    "text": "Last",
                    "nodes": [
                        {
                            "route": "adminlte2_pdq:sample1",
                            "text": "Sample1",
                            "icon": "fa fa-building",
                        }
                    ],
                }
            ]

            context = Context(
                {
                    "user": self.staff_user,
                    "ADMINLTE2_MENU": menu,
                    "ADMINLTE2_MENU_FIRST": menu_first,
                    "ADMINLTE2_MENU_LAST": menu_last,
                    "request": request,
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_menu %}")

            rendered_template = template_to_render.render(context)

            self.assertIn("Authentication", rendered_template)
            self.assertIn('<span class="node-link-text" title="User">User</span>', rendered_template)
            self.assertIn("Home", rendered_template)
            self.assertIn('<li class="header">', rendered_template)
            self.assertIn("Samples", rendered_template)
            self.assertIn('<li class="treeview treeview-split">', rendered_template)
            self.assertIn('<span class="node-link-text" title="DemoCSS">DemoCSS</span>', rendered_template)
            self.assertIn("fa fa-building-o", rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)
            self.assertIn('<li class="separator">', rendered_template)


class SidebarFullStackRenderTestCase(
    IntegrationTestCase,
    SidebarMenuBaseTestCase,
):
    """Tests for expected rendering of the Template Tag Sidebar Menu."""

    def test__dynamic_menu_does_not_duplicate(self):
        """There was a bug where dynamically created menus would cause duplication
        if the following conditions were met:

        1) The`ADMINLTE2_MENU_FIRST` variable was defined and used to create dynamic menus within a class-based view.
        2) The value passed to ADMINLTE2_MENU_FIRST was defined in a separate file, and imported into the file
           containing the class-based view.
        3) The view in question was accessed multiple times in a row (such as a page refresh).
        """

        # Access view first time. Should display as expected.
        self.assertGetResponse(
            "adminlte2_pdq_tests:class-standard",
            expected_header="Django AdminLtePdq | Standard View Header",
            expected_content=[
                # "First" sidebar menu definition.
                '<li class="header"> Custom Menu - First </li>',
                '<span class="node-link-text" title="[First] Custom Url 1">[First] Custom Url 1</span>',
                # "Standard" sidebar menu definition.
                '<li class="header"> Custom Menu - Standard </li>',
                '<span class="node-link-text" title="[Standard] Custom Url 1">[Standard] Custom Url 1</span>',
                # "Last" sidebar menu definition.
                '<li class="header"> Custom Menu - Last </li>',
                '<span class="node-link-text" title="[Last] Custom Url 1">[Last] Custom Url 1</span>',
            ],
        )

        # Access view second+ time. This is where the bug could occur.
        # To test this, we verify that the test fails when we check for any repeat values.

        # Test for duplicate "first" sidebar values.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    # "First" sidebar menu definition.
                    '<li class="header"> Custom Menu - First </li>',
                    '<span class="node-link-text" title="[First] Custom Url 1">[First] Custom Url 1</span>',
                    # "Standard" sidebar menu definition.
                    '<li class="header"> Custom Menu - Standard </li>',
                    '<span class="node-link-text" title="[Standard] Custom Url 1">[Standard] Custom Url 1</span>',
                    # "Last" sidebar menu definition.
                    '<li class="header"> Custom Menu - Last </li>',
                    '<span class="node-link-text" title="[Last] Custom Url 1">[Last] Custom Url 1</span>',
                    #
                    # Now check for repeats. Should fail here.
                    # "First" sidebar menu definition.
                    '<li class="header"> Custom Menu - First </li>',
                    '<span class="node-link-text" title="[First] Custom Url 1">[First] Custom Url 1</span>',
                ],
            )

        # Test for duplicate "standard" sidebar values.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    # "First" sidebar menu definition.
                    '<li class="header"> Custom Menu - First </li>',
                    '<span class="node-link-text" title="[First] Custom Url 1">[First] Custom Url 1</span>',
                    # "Standard" sidebar menu definition.
                    '<li class="header"> Custom Menu - Standard </li>',
                    '<span class="node-link-text" title="[Standard] Custom Url 1">[Standard] Custom Url 1</span>',
                    # "Last" sidebar menu definition.
                    '<li class="header"> Custom Menu - Last </li>',
                    '<span class="node-link-text" title="[Last] Custom Url 1">[Last] Custom Url 1</span>',
                    #
                    # Now check for repeats. Should fail here.
                    # "Standard" sidebar menu definition.
                    '<li class="header"> Custom Menu - Standard </li>',
                    '<span class="node-link-text" title="[Standard] Custom Url 1">[Standard] Custom Url 1</span>',
                ],
            )

        # Test for duplicate "last" sidebar values.
        with self.assertRaises(AssertionError):
            self.assertGetResponse(
                "adminlte2_pdq_tests:class-standard",
                expected_header="Django AdminLtePdq | Standard View Header",
                expected_content=[
                    # "First" sidebar menu definition.
                    '<li class="header"> Custom Menu - First </li>',
                    '<span class="node-link-text" title="[First] Custom Url 1">[First] Custom Url 1</span>',
                    # "Standard" sidebar menu definition.
                    '<li class="header"> Custom Menu - Standard </li>',
                    '<span class="node-link-text" title="[Standard] Custom Url 1">[Standard] Custom Url 1</span>',
                    # "Last" sidebar menu definition.
                    '<li class="header"> Custom Menu - Last </li>',
                    '<span class="node-link-text" title="[Last] Custom Url 1">[Last] Custom Url 1</span>',
                    #
                    # Now check for repeats. Should fail here.
                    # "Last" sidebar menu definition.
                    '<li class="header"> Custom Menu - Last </li>',
                    '<span class="node-link-text" title="[Last] Custom Url 1">[Last] Custom Url 1</span>',
                ],
            )
