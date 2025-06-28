"""
Tests for Admin Menu Template Tags.
"""

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.template import Template, Context
from django.test import TestCase, RequestFactory, override_settings

# Internal Imports.
from adminlte2_pdq.templatetags.admin.admin_menu import AdminMenu


# Module Variables.
UserModel = get_user_model()


class TemplateTagAdminMenuTestCase(TestCase):
    """Test for admin menu template tags."""

    def create_user(self):
        """Create a dummy user for views to access."""
        user = UserModel()
        user.pk = 1

        return user

    def normalize_html(self, html_string):
        """Normalize HTML string to remove newlines and extra whitespace"""
        return (
            " ".join(html_string.replace("\n", "").split())
            .replace(
                " >",
                ">",
                # TODO: Consider also adding the following to remove whitespace between tags.
                # ).replace(
                #     "> ", ">"
                # ).replace(
                #     " <", "<"
            )
            .replace('" "', '""')
        )

    # region render_admin_menu() Function

    def test__render_admin_menu(self):
        """Test render admin menu works with various settings."""

        with self.subTest("As staff - Default settings"):
            user = self.create_user()
            user.is_staff = True
            user.pk = 1
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            context = Context(
                {
                    "request": request,
                    "user": user,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="header">', rendered_template)

        with self.subTest("As superuser - Default settings"):
            user = self.create_user()
            user.is_superuser = True
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            context = Context(
                {
                    "request": request,
                    "user": user,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="header">', rendered_template)

        with self.subTest("As staff - Defined available apps in context, no permissions"):
            user = self.create_user()
            user.is_staff = True
            user.is_superuser = False
            user.pk = 4
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            available_apps = [
                {
                    "app_label": "AUTH",
                    "name": "Authentication",
                    "models": [
                        {
                            "perms": {
                                "add_foo": True,
                                "update_foo": False,
                            },
                            "object_name": "foo",
                            "change_url": "/foo",
                        },
                    ],
                }
            ]

            context = Context(
                {
                    "request": request,
                    "user": user,
                    "available_apps": available_apps,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="header">', rendered_template)
            self.assertNotIn(
                '<span class="treeview-text" title="Authentication">Authentication</span>',
                rendered_template,
            )
            self.assertNotIn('<a href="/foo">', rendered_template)
            self.assertNotIn("<span>foo</span>", rendered_template)

        with self.subTest("As staff - Defined available apps in context, no urls"):
            user = self.create_user()
            user.is_staff = True
            user.is_superuser = False
            user.pk = 4
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            available_apps = [
                {
                    "app_label": "AUTH",
                    "name": "Authentication",
                    "models": [
                        {
                            "perms": {
                                "add_foo": False,
                                "update_foo": False,
                            },
                            "object_name": "foo",
                        },
                    ],
                }
            ]

            context = Context(
                {
                    "request": request,
                    "user": user,
                    "available_apps": available_apps,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="header">', rendered_template)
            self.assertNotIn(
                '<span class="treeview-text" title="Authentication">Authentication</span>',
                rendered_template,
            )
            self.assertNotIn('<a href="/foo">', rendered_template)
            self.assertNotIn("<span>foo</span>", rendered_template)

        with self.subTest("As superuser - Defined available apps in context"):
            user = self.create_user()
            user.is_superuser = True
            user.pk = 1
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            available_apps = [
                {
                    "app_label": "AUTH",
                    "name": "Authentication",
                    "models": [
                        {
                            "perms": {
                                "add_foo": True,
                                "update_foo": True,
                            },
                            "object_name": "foo",
                            "change_url": "/foo",
                        },
                    ],
                }
            ]

            context = Context(
                {
                    "request": request,
                    "user": user,
                    "available_apps": available_apps,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="header">', rendered_template)
            self.assertIn(
                '<span class="treeview-text" title="Authentication">Authentication</span>',
                rendered_template,
            )
            self.assertIn('<a href="/foo" class="node-link">', rendered_template)
            self.assertIn('<span class="node-link-text" title="foo">foo</span>', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_MENU_IN_TREE=True)
    def test__render_admin_menu__admin_menu_in_tree(self):
        """Test render admin menu works for superuser with admin menu in tree settings"""

        user = self.create_user()
        # user.is_superuser = True
        request = RequestFactory().get("/rand")
        setattr(request, "user", user)

        context = Context(
            {
                "request": request,
                "user": user,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn('<li class="header">', rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=True)
    def test__render_admin_menu__include_main_nav(self):
        """Test render admin menu works for superuser with include main name"""

        user = self.create_user()
        # user.is_superuser = True
        request = RequestFactory().get("/rand")
        setattr(request, "user", user)

        context = Context(
            {
                "request": request,
                "user": user,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn('<li class="header">', rendered_template)

    # endregion render_admin_menu() Function

    def test__render_admin_tree_icon(self):
        """Test render_admin_tree_icon() tag renders in different scenarios."""

        with self.subTest("When icon is the default"):
            request = RequestFactory().get("/rand")

            context = Context(
                {
                    "request": request,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_tree_icon %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn("fa fa-superpowers", rendered_template)

        with self.subTest("When icon has been changed"):
            request = RequestFactory().get("/rand")

            original_icon_text = AdminMenu.get_admin_icon()
            icon_text = "fa fa-foo"
            AdminMenu.set_admin_icon(icon_text)

            context = Context(
                {
                    "request": request,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_tree_icon %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn("fa fa-foo", rendered_template)

            AdminMenu.set_admin_icon(original_icon_text)

    def test__render_app_icon(self):
        """Test render_app_icon() renders in different scenarios."""

        with self.subTest("When icon is the default"):
            request = RequestFactory().get("/rand")

            app = {
                "app_label": "Foo",
                "name": "FooBar",
                "models": [
                    {
                        "perms": {
                            "add_foo": True,
                            "update_foo": False,
                        },
                        "object_name": "foo",
                        "change_url": "/foo",
                    },
                ],
            }

            context = Context(
                {
                    "request": request,
                    "app": app,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_app_icon %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn("fa fa-circle", rendered_template)

        with self.subTest("When icon has been changed"):
            request = RequestFactory().get("/rand")

            app = {
                "app_label": "Foo",
                "name": "FooBar",
                "models": [
                    {
                        "perms": {
                            "add_foo": True,
                            "update_foo": False,
                        },
                        "object_name": "foo",
                        "change_url": "/foo",
                    },
                ],
            }

            original_icon_text = AdminMenu.get_app_icon(app["name"])
            icon_text = "fa fa-foo"
            AdminMenu.set_app_icon(app["name"], icon_text)

            context = Context(
                {
                    "app": app,
                    "request": request,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_app_icon %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn("fa fa-foo", rendered_template)

            AdminMenu.set_app_icon(app["name"], original_icon_text)

    def test__render_model_icon(self):
        """Test render_model_icon() renders in different scenarios."""

        with self.subTest("When icon is the default"):
            request = RequestFactory().get("/rand")

            model = {
                "perms": {
                    "add_foo": True,
                    "update_foo": False,
                },
                "object_name": "foo",
                "change_url": "/foo",
            }

            context = Context(
                {
                    "request": request,
                    "model": model,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_model_icon %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn("fa fa-circle-o", rendered_template)

        with self.subTest("When icon has been changed"):
            request = RequestFactory().get("/rand")

            model = {
                "perms": {
                    "add_foo": True,
                    "update_foo": False,
                },
                "object_name": "foo",
                "change_url": "/foo",
            }

            original_icon_text = AdminMenu.get_model_icon(model["object_name"])
            icon_text = "fa fa-foo"
            AdminMenu.set_model_icon(model["object_name"], icon_text)

            context = Context(
                {
                    "request": request,
                    "model": model,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_model_icon %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn("fa fa-foo", rendered_template)

            AdminMenu.set_model_icon(model["object_name"], original_icon_text)

    # region menu_group_separator() Function

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test__menu_group_separator__enabled(self):
        """Test menu group separator enabled."""

        with self.subTest("No additional menus"):
            user = self.create_user()
            user.is_staff = True
            user.is_superuser = False
            user.pk = 4
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            model = {
                "perms": {
                    "add_foo": True,
                    "update_foo": False,
                },
                "object_name": "foo",
                "change_url": "/foo",
            }

            context = Context(
                {
                    "request": request,
                    "model": model,
                    "user": user,
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="separator">', rendered_template)

        with self.subTest("One additional menu"):
            user = self.create_user()
            user.is_staff = True
            user.is_superuser = False
            user.pk = 4
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            model = {
                "perms": {
                    "add_foo": True,
                    "update_foo": False,
                },
                "object_name": "foo",
                "change_url": "/foo",
            }

            context = Context(
                {
                    "request": request,
                    "model": model,
                    "user": user,
                    "ADMINLTE2_MENU_FIRST": [
                        {
                            "text": "First",
                            "nodes": [
                                {
                                    "route": "#",
                                    "text": "First",
                                    "icon": "fa fa-circle",
                                },
                            ],
                        },
                    ],
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="separator">', rendered_template)

        with self.subTest("All additional menus"):
            user = self.create_user()
            user.is_staff = True
            user.is_superuser = False
            user.pk = 4
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            model = {
                "perms": {
                    "add_foo": True,
                    "update_foo": False,
                },
                "object_name": "foo",
                "change_url": "/foo",
            }

            context = Context(
                {
                    "request": request,
                    "model": model,
                    "user": user,
                    "ADMINLTE2_MENU_FIRST": [
                        {
                            "text": "First",
                            "nodes": [
                                {
                                    "route": "#",
                                    "text": "First",
                                    "icon": "fa fa-circle",
                                },
                            ],
                        },
                    ],
                    "ADMINLTE2_MENU_LAST": [
                        {
                            "text": "Last",
                            "nodes": [
                                {
                                    "route": "#",
                                    "text": "Last",
                                    "icon": "fa fa-circle",
                                },
                            ],
                        },
                    ],
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertIn('<li class="separator">', rendered_template)

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=False)
    def test__menu_group_separator__only_admin(self):
        """Test menu group separator only admin."""
        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand")
        setattr(request, "user", user)

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo",
        }

        context = Context(
            {
                "request": request,
                "model": model,
                "user": user,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertNotIn('<li class="separator">', rendered_template)

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=False)
    def test__menu_group_separator__disabled(self):
        """Test menu group separator disabled."""

        with self.subTest("One additional menu"):
            user = self.create_user()
            user.is_staff = True
            user.is_superuser = False
            user.pk = 4
            request = RequestFactory().get("/rand")
            setattr(request, "user", user)

            model = {
                "perms": {
                    "add_foo": True,
                    "update_foo": False,
                },
                "object_name": "foo",
                "change_url": "/foo",
            }

            context = Context(
                {
                    "request": request,
                    "model": model,
                    "user": user,
                    "ADMINLTE2_MENU_FIRST": [
                        {
                            "text": "First",
                            "nodes": [
                                {
                                    "route": "#",
                                    "text": "First",
                                    "icon": "fa fa-circle",
                                },
                            ],
                        },
                    ],
                }
            )
            template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

            rendered_template = self.normalize_html(template_to_render.render(context))

            self.assertNotIn('<li class="separator">', rendered_template)

    # endregion menu_group_separator() Function
