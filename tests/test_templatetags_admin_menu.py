"""
Tests for Admin Menu Template Tags
"""

from django.contrib.auth import get_user_model
from django.template import Template, Context
from django.test import TestCase, RequestFactory, override_settings

from adminlte2_pdq.templatetags.admin.admin_menu import AdminMenu

UserModel = get_user_model()


class TemplateTagAdminMenuTestCase(TestCase):
    """
    Test Template Tags
    """

    # |-------------------------------------------------------------------------
    # | Test render_admin_menu
    # |-------------------------------------------------------------------------

    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=False)
    def test_render_admin_menu_works_for_superuser_with_default_settings(self):
        """Test render admin menu works for superuser with default settings"""

        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        context = Context(
            {
                'request': request,
                'user': user,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )

    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=False)
    @override_settings(ADMINLTE2_ADMIN_MENU_IN_TREE=True)
    def test_render_admin_menu_works_for_superuser_with_admin_menu_in_tree_settings(self):
        """Test render admin menu works for superuser with admin menu in tree settings"""

        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        context = Context(
            {
                'request': request,
                'user': user,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )

    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=True)
    def test_render_admin_menu_works_for_superuser_with_include_main_nav(self):
        """Test render admin menu works for superuser with include main name"""

        user = self.create_user()
        user.is_superuser = True
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        context = Context(
            {
                'request': request,
                'user': user,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )

    def test_render_admin_menu_works_for_staff_with_default_settings(self):
        """Test render admin menu works for staff with default settings"""

        user = self.create_user()
        user.is_staff = True
        user.pk = 1
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        context = Context(
            {
                'request': request,
                'user': user,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )

    def test_render_admin_works_for_superuser_with_defined_available_apps_in_context(self):
        """Test render admin works for superuser with defined available apps in context"""

        user = self.create_user()
        user.is_superuser = True
        user.pk = 1
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        available_apps = [
            {
                'app_label': 'AUTH',
                'name': 'Authentication',
                'models': [
                    {
                        'perms': {
                            'add_foo': True,
                            'update_foo': True,
                        },
                        'object_name': 'foo',
                        'change_url': '/foo',
                    },
                ]
            }
        ]

        context = Context(
            {
                'request': request,
                'user': user,
                'available_apps': available_apps,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )
        self.assertIn(
            '<span class="treeview-text" title="Authentication">Authentication</span>',
            rendered_template
        )
        self.assertIn(
            '<a href="/foo" class="node-link">',
            rendered_template
        )
        self.assertIn(
            '<span class="node-link-text" title="foo">foo</span>',
            rendered_template
        )

    def test_render_admin_removes_no_perm_urls_for_staff_with_defined_available_apps_in_context_and_no_associated_permissions(self):
        """Test render admin removes no perm urls for staff with defined
        available apps in context and no associated permissions"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        available_apps = [
            {
                'app_label': 'AUTH',
                'name': 'Authentication',
                'models': [
                    {
                        'perms': {
                            'add_foo': True,
                            'update_foo': False,
                        },
                        'object_name': 'foo',
                        'change_url': '/foo',
                    },
                ]
            }
        ]

        context = Context(
            {
                'request': request,
                'user': user,
                'available_apps': available_apps,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )
        self.assertNotIn(
            '<span class="treeview-text" title="Authentication">Authentication</span>',
            rendered_template
        )
        self.assertNotIn(
            '<a href="/foo">',
            rendered_template
        )
        self.assertNotIn(
            '<span>foo</span>',
            rendered_template
        )

    def test_render_admin_fails_for_staff_with_defined_available_apps_in_context_that_has_no_urls(self):
        """Test render admin fails for staff with defined available apps in
        context that has no urls"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        available_apps = [
            {
                'app_label': 'AUTH',
                'name': 'Authentication',
                'models': [
                    {
                        'perms': {
                            'add_foo': False,
                            'update_foo': False,
                        },
                        'object_name': 'foo',
                    },
                ]
            }
        ]

        context = Context(
            {
                'request': request,
                'user': user,
                'available_apps': available_apps,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="header">',
            rendered_template
        )
        self.assertNotIn(
            '<span class="treeview-text" title="Authentication">Authentication</span>',
            rendered_template
        )
        self.assertNotIn(
            '<a href="/foo">',
            rendered_template
        )
        self.assertNotIn(
            '<span>foo</span>',
            rendered_template
        )

    # |-------------------------------------------------------------------------
    # | Test render_admin_tree_icon
    # |-------------------------------------------------------------------------

    def test_render_admin_tree_icon_tag_renders_the_icon_when_it_is_the_default(self):
        """Test render admin tree icon tag renders the icon when it is the default"""

        request = RequestFactory().get('/rand')

        context = Context(
            {
                'request': request,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_tree_icon %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            'fa fa-superpowers',
            rendered_template
        )

    def test_render_admin_tree_icon_tag_renders_the_icon_after_it_has_been_changed(self):
        """Test render admin tree icon tag renders the icon after it has been changed"""

        request = RequestFactory().get('/rand')

        original_icon_text = AdminMenu.get_admin_icon()
        icon_text = 'fa fa-foo'
        AdminMenu.set_admin_icon(icon_text)

        context = Context(
            {
                'request': request,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_tree_icon %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            'fa fa-foo',
            rendered_template
        )

        AdminMenu.set_admin_icon(original_icon_text)

    # |-------------------------------------------------------------------------
    # | Test render_app_icon
    # |-------------------------------------------------------------------------

    def test_render_app_icon_tag_renders_the_icon_when_it_is_the_default(self):
        """Test render app icon tag renders the icon when it is the default"""

        request = RequestFactory().get('/rand')

        app = {
            'app_label': 'Foo',
            'name': 'FooBar',
            'models': [
                {
                    'perms': {
                        'add_foo': True,
                        'update_foo': False,
                    },
                    'object_name': 'foo',
                    'change_url': '/foo',
                },
            ]
        }

        context = Context(
            {
                'request': request,
                'app': app,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_app_icon %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            'fa fa-circle',
            rendered_template
        )

    def test_render_app_icon_tag_renders_the_icon_after_it_has_been_changed(self):
        """Test render app icon tag renders the icon after it has been changed"""

        request = RequestFactory().get('/rand')

        app = {
            'app_label': 'Foo',
            'name': 'FooBar',
            'models': [
                {
                    'perms': {
                        'add_foo': True,
                        'update_foo': False,
                    },
                    'object_name': 'foo',
                    'change_url': '/foo',
                },
            ]
        }

        original_icon_text = AdminMenu.get_app_icon(app['name'])
        icon_text = 'fa fa-foo'
        AdminMenu.set_app_icon(app['name'], icon_text)

        context = Context(
            {
                'app': app,
                'request': request,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_app_icon %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            'fa fa-foo',
            rendered_template
        )

        AdminMenu.set_app_icon(app['name'], original_icon_text)

    # |-------------------------------------------------------------------------
    # | Test render_model_icon
    # |-------------------------------------------------------------------------

    def test_render_model_icon_tag_renders_the_icon_when_it_is_the_default(self):
        """Test render model icon tag renders the icon when it is the default"""

        request = RequestFactory().get('/rand')

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        context = Context(
            {
                'request': request,
                'model': model,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_model_icon %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            'fa fa-circle-o',
            rendered_template
        )

    def test_render_model_icon_tag_renders_the_icon_after_it_has_been_changed(self):
        """Test render model icon tag renders the icon after it has been changed"""

        request = RequestFactory().get('/rand')

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        original_icon_text = AdminMenu.get_model_icon(model['object_name'])
        icon_text = 'fa fa-foo'
        AdminMenu.set_model_icon(model['object_name'], icon_text)

        context = Context(
            {
                'request': request,
                'model': model,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_model_icon %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            'fa fa-foo',
            rendered_template
        )

        AdminMenu.set_model_icon(model['object_name'], original_icon_text)

    # |-------------------------------------------------------------------------
    # | Test menu_group_separator
    # |-------------------------------------------------------------------------

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test_render_admin_renders_correctly_with_menu_group_separator_enabled_and_all_additional_menus(self):
        """Test render admin renders correctly with menu group separator
        enabled and all additional menus"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        context = Context(
            {
                'request': request,
                'model': model,
                'user': user,
                'ADMINLTE2_MENU_FIRST': [
                    {
                        'text': 'First',
                        'nodes': [
                            {
                                'route': '#',
                                'text': 'First',
                                'icon': 'fa fa-circle',
                            },
                        ]
                    },
                ],
                'ADMINLTE2_MENU_LAST': [
                    {
                        'text': 'Last',
                        'nodes': [
                            {
                                'route': '#',
                                'text': 'Last',
                                'icon': 'fa fa-circle',
                            },
                        ]
                    },
                ]
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="separator">',
            rendered_template
        )

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test_render_admin_renders_correctly_with_menu_group_separator_enabled_and_one_additional_menu(self):
        """Test render admin renders correctly with menu group separator
        enabled and one additional menu"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        context = Context(
            {
                'request': request,
                'model': model,
                'user': user,
                'ADMINLTE2_MENU_FIRST': [
                    {
                        'text': 'First',
                        'nodes': [
                            {
                                'route': '#',
                                'text': 'First',
                                'icon': 'fa fa-circle',
                            },
                        ]
                    },
                ],
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="separator">',
            rendered_template
        )

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    def test_render_admin_renders_correctly_with_menu_group_separator_enabled_and_no_additional_menus(self):
        """Test render admin renders correctly with menu group separator
        enabled and no additional menus"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        context = Context(
            {
                'request': request,
                'model': model,
                'user': user,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertIn(
            '<li class="separator">',
            rendered_template
        )

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=True)
    @override_settings(ADMINLTE2_INCLUDE_MAIN_NAV_ON_ADMIN_PAGES=False)
    def test_render_admin_renders_correctly_with_menu_group_separator_enabled_and_only_admin_menu(self):
        """Test render admin renders correctly with menu group separator
        enabled and only admin menu"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        context = Context(
            {
                'request': request,
                'model': model,
                'user': user,
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn(
            '<li class="separator">',
            rendered_template
        )

    @override_settings(ADMINLTE2_USE_MENU_GROUP_SEPARATOR=False)
    def test_render_admin_renders_correctly_with_menu_group_separator_disabled_and_one_additional_menu(self):
        """Test render admin renders correctly with menu group separator
        disabled and one additional menu"""

        user = self.create_user()
        user.is_staff = True
        user.is_superuser = False
        user.pk = 4
        request = RequestFactory().get('/rand')
        setattr(request, 'user', user)

        model = {
            'perms': {
                'add_foo': True,
                'update_foo': False,
            },
            'object_name': 'foo',
            'change_url': '/foo',
        }

        context = Context(
            {
                'request': request,
                'model': model,
                'user': user,
                'ADMINLTE2_MENU_FIRST': [
                    {
                        'text': 'First',
                        'nodes': [
                            {
                                'route': '#',
                                'text': 'First',
                                'icon': 'fa fa-circle',
                            },
                        ]
                    },
                ],
            }
        )
        template_to_render = Template(
            "{% load admin.admin_menu %}"
            "{% render_admin_menu %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertNotIn(
            '<li class="separator">',
            rendered_template
        )

    def create_user(self):
        """Create a dummy user for views to access."""
        user = UserModel()
        user.pk = 1

        return user
