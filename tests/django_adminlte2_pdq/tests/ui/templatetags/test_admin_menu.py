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
            .replace(" >", ">")
            .replace("> ", ">")
            .replace(" <", "<")
            .replace('" "', '""')
        )

    # region render_admin_menu() Function

    def test__render_admin_menu__staff(self):
        """Renders the admin menu for a staff user, with the default settings."""
        user = self.create_user()
        user.is_staff = True
        user.pk = 1
        request = RequestFactory().get("/rand/")
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

    def test__render_admin_menu__superuser(self):
        """Renders the admin menu for a superuser, with the default settings."""
        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get("/rand/")
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

    def test__render_admin_menu__staff_without_model_permissions(self):
        """Hides models the staff user has none of the enabled admin permissions for."""
        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand/")
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
                        "change_url": "/foo/",
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
        self.assertNotIn('<a href="/foo/">', rendered_template)
        self.assertNotIn("<span>foo</span>", rendered_template)

    def test__render_admin_menu__staff_without_model_urls(self):
        """Hides apps whose models have no urls."""
        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand/")
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
        self.assertNotIn('<a href="/foo/">', rendered_template)
        self.assertNotIn("<span>foo</span>", rendered_template)

    def test__render_admin_menu__superuser_with_apps(self):
        """Shows the apps in the context to a superuser."""
        user = self.create_user()
        user.is_superuser = True
        user.pk = 1
        request = RequestFactory().get("/rand/")
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
                        "change_url": "/foo/",
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
        self.assertIn('<a href="/foo/" class="node-link">', rendered_template)
        self.assertIn('<span class="node-link-text" title="foo">foo</span>', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_MENU_IN_TREE=True)
    def test__render_admin_menu__admin_menu_in_tree_with_apps(self):
        """Test render admin menu works for superuser with admin menu in tree settings with apps"""

        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get("/rand/")
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
                        "change_url": "/foo/",
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

        self.assertIn('<li class="treeview">', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_MENU_IN_TREE=True)
    def test__render_admin_menu__admin_menu_in_tree_no_apps(self):
        """Test render admin menu works for superuser with admin menu in tree settings and no apps"""

        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get("/rand/")
        setattr(request, "user", user)

        context = Context(
            {
                "request": request,
                "user": user,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn('<li class="treeview">', rendered_template)

    @override_settings(ADMINLTE2_ADMIN_MENU_IN_TREE=True)
    def test__render_admin_menu__admin_menu_in_tree_no_apps_with_match(self):
        """Test render admin menu works for superuser with admin menu in tree settings and no apps and url match"""

        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get("/admin/")
        setattr(request, "user", user)

        context = Context(
            {
                "request": request,
                "user": user,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_menu %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn('<li class="treeview active">', rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=True)
    def test__render_admin_menu__include_main_nav(self):
        """Test render admin menu works for superuser with include main name"""

        user = self.create_user()
        # user.is_superuser = True
        request = RequestFactory().get("/rand/")
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
        """When icon is the default."""
        request = RequestFactory().get("/rand/")

        context = Context(
            {
                "request": request,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_tree_icon %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn("fa fa-superpowers", rendered_template)

    def test__render_admin_tree_icon__changed(self):
        """Renders the admin tree icon set with AdminMenu.set_admin_icon()."""
        request = RequestFactory().get("/rand/")

        original_icon_text = AdminMenu.get_admin_icon()
        icon_text = "fa fa-foo"
        AdminMenu.set_admin_icon(icon_text)
        self.addCleanup(AdminMenu.set_admin_icon, original_icon_text)

        context = Context(
            {
                "request": request,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_admin_tree_icon %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn("fa fa-foo", rendered_template)

    def test__render_app_icon(self):
        """When icon is the default."""
        request = RequestFactory().get("/rand/")

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
                    "change_url": "/foo/",
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

    def test__render_app_icon__changed(self):
        """Renders the app icon set with AdminMenu.set_app_icon()."""
        request = RequestFactory().get("/rand/")

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
                    "change_url": "/foo/",
                },
            ],
        }

        original_icon_text = AdminMenu.get_app_icon(app["name"])
        icon_text = "fa fa-foo"
        AdminMenu.set_app_icon(app["name"], icon_text)
        self.addCleanup(AdminMenu.set_app_icon, app["name"], original_icon_text)

        context = Context(
            {
                "app": app,
                "request": request,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_app_icon %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn("fa fa-foo", rendered_template)

    def test__render_model_icon(self):
        """When icon is the default."""
        request = RequestFactory().get("/rand/")

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
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

    def test__render_model_icon__changed(self):
        """Renders the model icon set with AdminMenu.set_model_icon()."""
        request = RequestFactory().get("/rand/")

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
        }

        original_icon_text = AdminMenu.get_model_icon(model["object_name"])
        icon_text = "fa fa-foo"
        AdminMenu.set_model_icon(model["object_name"], icon_text)
        self.addCleanup(AdminMenu.set_model_icon, model["object_name"], original_icon_text)

        context = Context(
            {
                "request": request,
                "model": model,
            }
        )
        template_to_render = Template("{% load admin.admin_menu %}{% render_model_icon %}")

        rendered_template = self.normalize_html(template_to_render.render(context))

        self.assertIn("fa fa-foo", rendered_template)

    # region menu_group_separator() Function

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test__menu_group_separator__enabled(self):
        """Renders a separator with no extra menus."""
        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand/")
        setattr(request, "user", user)

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
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

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test__menu_group_separator__enabled__one_extra_menu(self):
        """Renders a separator with one extra menu."""
        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand/")
        setattr(request, "user", user)

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
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

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test__menu_group_separator__enabled__all_extra_menus(self):
        """Renders separators with all extra menus."""
        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand/")
        setattr(request, "user", user)

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
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
        request = RequestFactory().get("/rand/")
        setattr(request, "user", user)

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
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
        """Renders no separator with an extra menu when the setting is off."""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get("/rand/")
        setattr(request, "user", user)

        model = {
            "perms": {
                "add_foo": True,
                "update_foo": False,
            },
            "object_name": "foo",
            "change_url": "/foo/",
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
