"""
Tests for Template Tags
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context
from django.test import TestCase, override_settings, RequestFactory
from django.urls import NoReverseMatch

# Internal Imports.
from adminlte2_pdq.templatetags import sidebar_menu


# Module Variables.
UserModel = get_user_model()


class TemplateTagSidebarMenuBaseTestCase(TestCase):
    # region Expected Test Messages

    node_error__key_error_message = (
        '"The route key must be provided for the node.'
        " If you do not have a valid route yet you can use '#' as a placeholder."
        " If you have Whitelisting turned on, be sure to"
        " add an entry for '#' to the whitelist."
        " Missing key was: 'route'\""
    )

    node_error__invalid_route_message = (
        "The node with the route 'foobar' is not a valid route."
        " If you do not have a valid route yet you can use '#' as a placeholder."
        " If you have Whitelisting turned on, be sure to"
        " add an entry for '#' to the whitelist."
        " Exception Message: Reverse for 'foobar' not found. 'foobar' is not a valid view function or pattern name."
    )

    # endregion Expected Test Messages

    def setUp(self):
        self.anonymous_user = None
        self.user = None
        self.staff_user = None
        self.super_user = None

        # Generate test permissions.
        self.permission_content_type = ContentType.objects.get_for_model(Permission)

        # First permission. Generally used anywhere at least one permission is required.
        add_foo = Permission.objects.create(
            name="add_foo",
            codename="add_foo",
            content_type=self.permission_content_type,
        )
        # Second permission. Generally used anywhere multiple permissions are required.
        change_foo = Permission.objects.create(
            name="change_foo",
            codename="change_foo",
            content_type=self.permission_content_type,
        )
        # Extra permissions used in some edge case tests.
        view_foo = Permission.objects.create(
            name="view_foo",
            codename="view_foo",
            content_type=self.permission_content_type,
        )
        delete_foo = Permission.objects.create(
            name="delete_foo",
            codename="delete_foo",
            content_type=self.permission_content_type,
        )
        # Final extra permission that's not explicitly used anywhere.
        # To verify permission logic still works with extra, unrelated permissions in the project.
        unused_foo = Permission.objects.create(
            name="unused_foo",
            codename="unused_foo",
            content_type=self.permission_content_type,
        )

        # Define various permission sets to test against.
        self.full_perms = Permission.objects.filter(codename__in=("add_foo", "change_foo"))
        self.partial_perms = Permission.objects.filter(codename="add_foo")

        # Generate test groups. To ensure that as Group logic is handled as expected as well.
        group_instance = Group.objects.create(name="add_bar")
        group_instance.permissions.add(add_foo)
        group_instance = Group.objects.create(name="change_bar")
        group_instance.permissions.add(change_foo)
        group_instance = Group.objects.create(name="view_foo")
        group_instance.permissions.add(view_foo)
        group_instance = Group.objects.create(name="delete_bar")
        group_instance.permissions.add(delete_foo)
        group_instance = Group.objects.create(name="unused_bar")
        group_instance.permissions.add(unused_foo)

        # Define various group sets to test against.
        self.full_groups = Group.objects.filter(name__in=("add_bar", "change_bar"))
        self.partial_groups = Group.objects.filter(name="add_bar")

    def _setup_anonymous_user(self):
        """Set up anonymous user"""
        self.anonymous_user = AnonymousUser()

    def _setup_user(self, permissions=None):
        """Set up basic user"""

        # Remove user if already exists.
        if self.user:
            self.user.delete()

        self.user = UserModel()
        self.user.username = "test_user"
        self.user.save()

        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.user.user_permissions.add(perm_object)

    def _setup_staff_user(self, permissions=None):
        """Set up Staff user"""

        # Remove user if already exists.
        if self.staff_user:
            self.staff_user.delete()

        self.staff_user = UserModel()
        self.staff_user.username = "test_staff_user"
        self.staff_user.is_staff = True
        self.staff_user.save()

        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.staff_user.user_permissions.add(perm_object)

    def _setup_super_user(self):
        """Set up Superuser"""
        self.super_user = UserModel()
        self.super_user.username = "test_super_user"
        self.super_user.is_superuser = True
        self.super_user.save()

    # endregion Setup


class TemplateTagSidebarMenuTestCase(TemplateTagSidebarMenuBaseTestCase):
    """
    Test Template Tags and Helper functions used in those template tags
    """

    # region Demo Url

    def test__default_routes_are_registered_function__works_when_routes_are_registered(self):
        """Test default routes are registered function works when routes are registered"""
        self.assertTrue(sidebar_menu._default_routes_are_registered())

    @override_settings(ROOT_URLCONF="tests.urls_empty")
    def test__default_routes_are_registered_function__fails_when_routes_are_not_registered(self):
        """Test default routes are registered function fails when routes are not registered"""
        self.assertFalse(sidebar_menu._default_routes_are_registered())

    # endregion Demo Url

    # region get_permissions_from_node() Function

    def test__get_permissions_from_node__errors(self):
        """Tests for various expected errors in get_permissions_from_node() function."""

        with self.subTest("Raises KeyError when route is missing."):
            # Define node with no route.
            node = {
                "text": "Sample1",
                "icon": "fa fa-group",
            }

            # Call function to test.
            with self.assertRaises(KeyError) as err:
                sidebar_menu.get_permissions_from_node(node)
            self.assertEqual(self.node_error__key_error_message, str(err.exception))

        with self.subTest("Propagates route reverse error"):
            # Define node with invalid route.
            node = {
                "route": "foobar",
                "text": "Sample1",
                "icon": "fa fa-group",
            }

            # Call function to test.
            with self.assertRaises(NoReverseMatch) as err:
                sidebar_menu.get_permissions_from_node(node)
            self.assertEqual(self.node_error__invalid_route_message, str(err.exception))

    def test__get_permissions_from_node__standard(self):
        """Tests for get_permissions_from_node() function when passing a basic node."""

        with self.subTest("Route is a hash"):
            # Define node with hash as route.
            # Used as placeholder when desired route url may not yet be fully defined.
            node = {
                "route": "#",
                "text": "Sample1",
                "icon": "fa fa-group",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Route was hash so should get empty lists.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

    def test__get_permissions_from_node__login_required(self):
        """Tests various node login_required attributes for get_permissions_from_node() function."""

        with self.subTest("Node returns false when login_required not set"):
            # Define node.
            node = {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Home",
                "icon": "fa fa-dashboard",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls login_required from direct assignment"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:demo-css",
                "text": "Demo CSS",
                "icon": "fa fa-file",
                "login_required": True,
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls login_required from view function"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:sample_form",
                "text": "Sample Form",
                "icon": "fa fa-file",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls login_required from node when both are set"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:sample_form",
                "text": "Sample Form",
                "icon": "fa fa-file",
                "login_required": False,
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls login_required from view with hash route and valid url"):
            # Define node.
            node = {
                "route": "#",
                "text": "Sample Form",
                "icon": "fa fa-building",
                "url": "/sample_form/",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls login_required from direct assignment with external url"):
            # Define node.
            node = {
                "route": "#",
                "text": "GitHub",
                "icon": "fa fa-github",
                "url": "https://github.com",
                "login_required": True,
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node returns false when node is for external resource"):
            # Define node.
            node = {
                "route": "#",
                "text": "External",
                "icon": "fa fa-github",
                "url": "https://github.com",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

    def test__get_permissions_from_node__one_of_permissions(self):
        """Tests various node one_of_permissions attributes for get_permissions_from_node() function."""

        with self.subTest("Node returns empty lists when permissions not set"):
            # Define node.
            node = {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Home",
                "icon": "fa fa-dashboard",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from direct assignment"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:demo-css",
                "text": "Demo CSS",
                "icon": "fa fa-file",
                "one_of_permissions": ["add_sample2", "update_sample2"],
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual(node["one_of_permissions"], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from view function"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertIn("auth.add_permission", one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from node when both are set"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
                "one_of_permissions": [],
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from view with hash route and valid url"):
            # Define node.
            node = {
                "route": "#",
                "text": "Sample2",
                "icon": "fa fa-building",
                "url": "/sample2/",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertIn("auth.add_permission", one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from direct assignment with external url"):
            # Define node.
            node = {
                "route": "#",
                "text": "GitHub",
                "icon": "fa fa-github",
                "url": "https://github.com",
                "one_of_permissions": ["add_sample2", "update_sample2"],
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual(node["one_of_permissions"], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node returns empty list when node is for external resource"):
            # Define node.
            node = {
                "route": "#",
                "text": "External",
                "icon": "fa fa-github",
                "url": "https://github.com",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

    def test__get_permissions_from_node__full_permissions(self):
        """Tests various node full_permissions attributes for get_permissions_from_node() function."""

        with self.subTest("Node returns empty lists when permissions not set"):
            # Define node.
            node = {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Home",
                "icon": "fa fa-dashboard",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from direct assignment"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:demo-css",
                "text": "Demo CSS",
                "icon": "fa fa-file",
                "permissions": ["add_sample1", "update_sample1"],
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual(node["permissions"], full_permissions)

        with self.subTest("Node pulls permissions from view function"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:sample1",
                "text": "Sample1",
                "icon": "fa fa-group",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertIn("auth.add_group", full_permissions)

        with self.subTest("Node pulls permissions from node when both are set"):
            # Define node.
            node = {
                "route": "adminlte2_pdq:sample1",
                "text": "Sample1",
                "icon": "fa fa-group",
                "permissions": [],
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node pulls permissions from view with hash route and valid url"):
            # Define node.
            node = {
                "route": "#",
                "text": "Sample1",
                "icon": "fa fa-building",
                "url": "/sample1/",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertTrue(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertIn("auth.add_group", full_permissions)

        with self.subTest("Node pulls permissions from direct assignment with external url"):
            # Define node.
            node = {
                "route": "#",
                "text": "GitHub",
                "icon": "fa fa-github",
                "url": "https://github.com",
                "permissions": ["add_sample1", "update_sample1"],
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual(node["permissions"], full_permissions)

        with self.subTest("Node returns empty list when node is for external resource"):
            # Define node.
            node = {
                "route": "#",
                "text": "External",
                "icon": "fa fa-github",
                "url": "https://github.com",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous = return_data["allow_anonymous"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

    # endregion get_permissions_from_node() Function

    # region ensure_node_has_url_property() Function

    def test__ensure_node_has_url_property__success(self):
        """"""

        with self.subTest("Works when node has url property defined"):
            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
                "url": "/foobar/",
            }

            sidebar_menu.ensure_node_has_url_property(node)

            self.assertEqual("/foobar/", node["url"])

        with self.subTest("Adds url property from valid route"):
            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            sidebar_menu.ensure_node_has_url_property(node)

            self.assertEqual("/sample2/", node["url"])

        with self.subTest("Sets url to hash when route is a hash"):
            node = {
                "route": "#",
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            sidebar_menu.ensure_node_has_url_property(node)

            self.assertEqual("#", node["url"])

    def test__ensure_node_has_url_property__failure(self):
        """"""

        with self.subTest("Raises KeyError when route field is missing"):
            node = {
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            with self.assertRaises(KeyError) as err:
                sidebar_menu.ensure_node_has_url_property(node)
            self.assertEqual(self.node_error__key_error_message, str(err.exception))

        with self.subTest("Propagates route reverse error"):
            node = {
                "route": "foobar",
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            with self.assertRaises(NoReverseMatch) as err:
                sidebar_menu.ensure_node_has_url_property(node)
            self.assertEqual(self.node_error__invalid_route_message, str(err.exception))

    # endregion ensure_node_has_url_property() Function

    # region check_for_login_whitelisted_node() Function

    def test__check_for_login_whitelisted_node__node_not_in_list(self):
        node = {
            "route": "foobar",
            "text": "Sample Form",
            "icon": "fa fa-file",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertFalse(is_whitelisted)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:sample_form"])
    def test__check_for_login_whitelisted_node__node_in_list(self):
        node = {
            "route": "adminlte2_pdq:sample_form",
            "text": "Sample Form",
            "icon": "fa fa-file",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertTrue(is_whitelisted)

    # endregion check_for_login_whitelisted_node() Function

    # region check_for_strict_whitelisted_node() Function

    def test__check_for_strict_whitelisted_node__node_not_in_list(self):
        node = {
            "route": "foobar",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertFalse(is_whitelisted)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:sample2"])
    def test__check_for_strict_whitelisted_node__node_in_list(self):
        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertTrue(is_whitelisted)

    # endregion check_for_strict_whitelisted_node() Function

    # region Permission Check Functions

    def test__check_for_one_permission(self):

        with self.subTest("As user with most permissions, except one required"):
            self._setup_staff_user()

            permissions = ["user_does_not_have_this_one"]

            allowed = sidebar_menu.check_for_one_permission(self.staff_user, permissions)

            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            self._setup_staff_user("add_group")

            permissions = ["auth.add_group", "auth.update_group"]

            allowed = sidebar_menu.check_for_one_permission(self.staff_user, permissions)

            self.assertTrue(allowed)

        with self.subTest("As user with full permissions, but none are passed"):
            self._setup_staff_user("add_group")

            permissions = []

            allowed = sidebar_menu.check_for_one_permission(self.staff_user, permissions)

            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            self._setup_super_user()

            permissions = ["does_not_matter_since_superuser"]

            allowed = sidebar_menu.check_for_one_permission(self.super_user, permissions)

            self.assertTrue(allowed)

    def test__check_for_all_permissions(self):

        with self.subTest("As user with most permissions, except the one required"):
            self._setup_staff_user()

            permissions = ["user_does_not_have_this_one"]

            allowed = sidebar_menu.check_for_all_permissions(self.staff_user, permissions)

            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            self._setup_staff_user("add_group")

            permissions = ["auth.add_group"]

            allowed = sidebar_menu.check_for_all_permissions(self.staff_user, permissions)

            self.assertTrue(allowed)

        with self.subTest("As user with full permissions, but none are passed"):
            self._setup_staff_user("add_group")

            permissions = []

            allowed = sidebar_menu.check_for_all_permissions(self.staff_user, permissions)

            self.assertFalse(allowed)

        with self.subTest("As superuser"):
            self._setup_super_user()

            permissions = ["does_not_matter_since_superuser"]

            allowed = sidebar_menu.check_for_all_permissions(self.super_user, permissions)

            self.assertTrue(allowed)

    # endregion Permission Check Functions

    def test__check_for_one_permission_in_node_list(self):

        with self.subTest("Returns true for superuser regardless of tree size"):
            self._setup_super_user()

            nodes = [
                {
                    "route": "adminlte2_pdq:sample2",
                    "text": "Sample2",
                    "icon": "fa fa-building",
                }
            ]

            nodetree = [
                {
                    "text": "Sample Tree",
                    "icon": "fa fa-leaf",
                    "nodes": [
                        {
                            "text": "Sample Sub Tree",
                            "icon": "fa fa-cube",
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

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.super_user, nodes)
            self.assertTrue(allowed)

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.super_user, nodetree)
            self.assertTrue(allowed)

        with self.subTest("Returns true for single node user can access"):
            self._setup_staff_user("add_permission")

            nodes = [
                {
                    "route": "adminlte2_pdq:sample2",
                    "text": "Sample2",
                    "icon": "fa fa-building",
                }
            ]

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staff_user, nodes)

            self.assertTrue(allowed)

        with self.subTest("Returns true for two nodes user can access"):
            self._setup_staff_user("add_permission")

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

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staff_user, nodes)
            self.assertTrue(allowed)

        with self.subTest("Returns true for three nodes user can access"):
            self._setup_staff_user("add_permission")

            nodes = [
                {
                    "text": "Sample Tree",
                    "icon": "fa fa-leaf",
                    "nodes": [
                        {
                            "text": "Sample Sub Tree",
                            "icon": "fa fa-cube",
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

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staff_user, nodes)
            self.assertTrue(allowed)

        with self.subTest("Returns false for single node user cannot access"):
            self._setup_staff_user("add_group")

            nodes = [
                {
                    "route": "adminlte2_pdq:sample2",
                    "text": "Sample2",
                    "icon": "fa fa-building",
                }
            ]

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staff_user, nodes)
            self.assertFalse(allowed)

        with self.subTest("Returns false for two nodes user cannot access"):
            self._setup_staff_user("add_group")

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

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staff_user, nodes)
            self.assertFalse(allowed)

        with self.subTest("Returns false for three nodes user cannot access"):
            self._setup_staff_user("add_group")

            nodes = [
                {
                    "text": "Sample Tree",
                    "icon": "fa fa-leaf",
                    "nodes": [
                        {
                            "text": "Sample Sub Tree",
                            "icon": "fa fa-cube",
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

            allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staff_user, nodes)
            self.assertFalse(allowed)

    def test__check_for_node_that_matches_request_path(self):

        with self.subTest("Returns false for no nodes"):
            nodes = []
            request = RequestFactory().get("/sample2/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertFalse(match)

        with self.subTest("Returns true for single node with match"):
            nodes = [
                {
                    "route": "adminlte2_pdq:sample2",
                    "text": "Sample2",
                    "icon": "fa fa-building",
                }
            ]
            request = RequestFactory().get("/sample2/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertTrue(match)

        with self.subTest("Returns true for two nodes with match"):
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
            request = RequestFactory().get("/sample2/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertTrue(match)

        with self.subTest("Returns true for three nodes with match"):
            nodes = [
                {
                    "text": "Sample Tree",
                    "icon": "fa fa-leaf",
                    "nodes": [
                        {
                            "text": "Sample Sub Tree",
                            "icon": "fa fa-cube",
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
            request = RequestFactory().get("/sample2/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertTrue(match)

        with self.subTest("Returns false for single node without match"):
            nodes = [
                {
                    "route": "adminlte2_pdq:sample2",
                    "text": "Sample2",
                    "icon": "fa fa-building",
                }
            ]
            request = RequestFactory().get("/sample1/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertFalse(match)

        with self.subTest("Returns false for two nodes without match"):
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
            request = RequestFactory().get("/sample1/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertFalse(match)

        with self.subTest("Returns false for three nodes without match"):
            nodes = [
                {
                    "text": "Sample Tree",
                    "icon": "fa fa-leaf",
                    "nodes": [
                        {
                            "text": "Sample Sub Tree",
                            "icon": "fa fa-cube",
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
            request = RequestFactory().get("/sample1/")
            match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

            self.assertFalse(match)


class TemplateTagSidebarMenu_RendertestCase(TemplateTagSidebarMenuBaseTestCase):

    def test__render_types(self):
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
            self.assertIn('<li class="treeview">', rendered_template)
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

            self.assertIn('<li class="treeview">', rendered_template)
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

            self.assertIn('<li class="treeview">', rendered_template)
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

            self.assertIn('<li class="treeview">', rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertNotIn("fa fa-leaf", rendered_template)
            self.assertIn("not-found", rendered_template)

        with self.subTest("Render link - Standard"):
            self._setup_staff_user("add_permission")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": {
                        "path": "/some/path",
                    },
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)

        with self.subTest("Render link - No icon provided"):
            self._setup_staff_user("add_permission")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": {
                        "path": "/some/path",
                    },
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertNotIn("fa fa-building", rendered_template)

        with self.subTest("Render link - Dynamic text via string"):
            self._setup_staff_user("add_permission")

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "hook": "tests.utils.valid_string_hook_function",
                "hook_args": ["foo"],
                "hook_kwargs": {"kwarg1": "bar"},
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": {
                        "path": "/some/path",
                    },
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

            node = {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "hook": "tests.utils.valid_tuple_hook_function",
                "hook_args": ["foo"],
                "hook_kwargs": {"kwarg1": "bar"},
            }

            context = Context(
                {
                    "user": self.staff_user,
                    "node": node,
                    "request": {
                        "path": "/some/path",
                    },
                }
            )

            template_to_render = Template("{% load sidebar_menu %}{% render_link node %}")

            rendered_template = template_to_render.render(context)

            self.assertIn('<span class="node-link-text" title="foo bar">foobar</span>', rendered_template)
            self.assertNotIn("fa fa-building", rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=False)
    def test__user_has_access_and_admin_include_is_off(self):
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
        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=True)
    def test__user_has_access_and_admin_include_is_on(self):

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
            self.assertIn('<li class="treeview">', rendered_template)
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
            self.assertIn('<li class="treeview">', rendered_template)
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
            self.assertIn('<li class="treeview">', rendered_template)
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
            self.assertIn('<li class="treeview">', rendered_template)
            self.assertIn('<span class="node-link-text" title="DemoCSS">DemoCSS</span>', rendered_template)
            self.assertIn("fa fa-building-o", rendered_template)
            self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
            self.assertIn("fa fa-building", rendered_template)
            self.assertIn('<li class="separator">', rendered_template)


class TemplateTagSidebarMenu_IsAllowedNodeTestCase(TemplateTagSidebarMenuBaseTestCase):
    """Tests for is_allowed_node() function in sidebar logic."""

    # region Loose Mode, Standard Settings

    def test__standard__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # def test__standard__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    def test__standard__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # def test__standard__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    def test__standard__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    def test__standard__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Loose Mode, Standard Settings

    # region LoginRequired Mode, No Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # def test__login_required__no_whitelists__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # def test__login_required__no_whitelists__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test__login_required__no_whitelists__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion LoginRequired Mode, No Whitelist

    # region LoginRequired Mode, Login Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__login_required__with_login_whitelist__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__login_required__with_login_whitelist__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         self._setup_super_user()
    #
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__login_required__with_login_whitelist__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion LoginRequired Mode, Login Whitelist

    # region Strict Mode, No Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # def test__strict__no_whitelists__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # def test__strict__no_whitelists__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test__strict__no_whitelists__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, No Whitelist

    # region Strict Mode, Login Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_login_whitelist__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_login_whitelist__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_login_whitelist__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_login_whitelist__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_login_whitelist__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Login Whitelist

    # region Strict Mode, Permission Whitelist

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_permission_whitelist__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_permission_whitelist__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertFalse(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_permission_whitelist__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Permission Whitelist

    # region Strict Mode, Both Whitelists

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_minimal(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_both_whitelists__node_allow_anonymous(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_anonymous": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_login_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    # @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    # def test__strict__with_both_whitelists__node_allow_without_permissions(self):
    #     """"""
    #
    #     # Node used for all subtests.
    #     node = {
    #         "route": "adminlte2_pdq:demo-css",
    #         "text": "Demo CSS",
    #         "icon": "fa fa-file",
    #         "allow_without_permissions": True,
    #     }
    #
    #     with self.subTest("As anonymous user"):
    #         # Get user to run subtest on.
    #         self._setup_anonymous_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with no permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with partial permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As staff user with full permissions"):
    #         # Get user to run subtest on.
    #         self._setup_staff_user(["add_foo", "change_foo"])
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
    #         self.assertTrue(allowed)
    #
    #     with self.subTest("As user with one group"):
    #         pass
    #
    #     with self.subTest("As user with full group"):
    #         pass
    #
    #     with self.subTest("As superuser"):
    #         # Get user to run subtest on.
    #         self._setup_super_user()
    #
    #         # Test sidebar logic.
    #         allowed = sidebar_menu.is_allowed_node(self.super_user, node)
    #         self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_one_permission_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test__strict__with_both_whitelists__node_full_permissions_required(self):
        """"""

        # Node used for all subtests.
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_foo", "auth.change_foo"],
        }

        with self.subTest("As anonymous user"):
            # Get user to run subtest on.
            self._setup_anonymous_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.anonymous_user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with no permissions"):
            # Get user to run subtest on.
            self._setup_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertFalse(allowed)

        with self.subTest("As user with partial permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with full permissions"):
            # Get user to run subtest on.
            self._setup_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with no permissions"):
            # Get user to run subtest on.
            self._setup_staff_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertFalse(allowed)

        with self.subTest("As staff user with partial permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As staff user with full permissions"):
            # Get user to run subtest on.
            self._setup_staff_user(["add_foo", "change_foo"])

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.staff_user, node)
            self.assertTrue(allowed)

        with self.subTest("As user with one group"):
            pass

        with self.subTest("As user with full group"):
            pass

        with self.subTest("As superuser"):
            # Get user to run subtest on.
            self._setup_super_user()

            # Test sidebar logic.
            allowed = sidebar_menu.is_allowed_node(self.super_user, node)
            self.assertTrue(allowed)

    # endregion Strict Mode, Both Whitelists
