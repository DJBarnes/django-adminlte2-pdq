"""
Tests for the sidebar menu's node helpers: permissions, urls, whitelists, and active state.
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.test import override_settings, RequestFactory
from django.urls import NoReverseMatch

# Internal Imports.
from adminlte2_pdq.templatetags import sidebar_menu
from tests.django_adminlte2_pdq.tests.core.menu.base_test_case import SidebarMenuBaseTestCase


# Module Variables.


class SidebarMenuHelpersTestCase(SidebarMenuBaseTestCase):
    """
    Tests basic logic for sidebar Template Tags and Helper functions used in those template tags.
    """

    # region Demo Url

    def test__default_routes_are_registered_function__works_when_routes_are_registered(self):
        """Test default routes are registered function works when routes are registered"""
        # pylint:disable=protected-access
        self.assertTrue(sidebar_menu._default_routes_are_registered())

    @override_settings(ROOT_URLCONF="tests.django_adminlte2_pdq.django_test_project.urls_empty")
    def test__default_routes_are_registered_function__fails_when_routes_are_not_registered(self):
        """Test default routes are registered function fails when routes are not registered"""
        # pylint:disable=protected-access
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

        with self.subTest("Raises Improperly Configured node when both anonymous and login required"):
            # Define node that will trigger improperly configured error
            node = {
                "route": "foobar",
                "text": "Sample1",
                "icon": "fa fa-group",
                "allow_anonymous_access": True,
                "login_required": True,
            }

            # Call function to test.
            with self.assertRaises(ImproperlyConfigured) as err:
                sidebar_menu.get_permissions_from_node(node)

        with self.subTest("Raises Improperly Configured node when both no perms and permission required"):
            # Define node that will trigger improperly configured error
            node = {
                "route": "foobar",
                "text": "Sample1",
                "icon": "fa fa-group",
                "allow_without_permissions": True,
                "permissions": ["foobar"],
            }

            # Call function to test.
            with self.assertRaises(ImproperlyConfigured) as err:
                sidebar_menu.get_permissions_from_node(node)

        with self.subTest("Raises Improperly Configured node when both anonymous and permission required"):
            # Define node that will trigger improperly configured error
            node = {
                "route": "foobar",
                "text": "Sample1",
                "icon": "fa fa-group",
                "allow_anonymous_access": True,
                "permissions": ["foobar"],
            }

            # Call function to test.
            with self.assertRaises(ImproperlyConfigured) as err:
                sidebar_menu.get_permissions_from_node(node)

        with self.subTest("Raises Improperly Configured view when both anonymous and login required"):
            # Define a valid node.
            node = {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Sample1",
                "icon": "fa fa-group",
            }
            # Patch the "get_permissions_from_view" method to return data that
            # would reflect a view that is improperly configured. Then attempt
            # to get the permissions from the node, which will ultimately pull
            # from the patched view method and cause the improperly configured
            with patch("adminlte2_pdq.templatetags.sidebar_menu.get_permissions_from_view") as get_perm_from_view:
                get_perm_from_view.return_value = {
                    "allow_anonymous_access": True,
                    "login_required": True,
                    "allow_without_permissions": False,
                    "one_of_permissions": None,
                    "full_permissions": None,
                }
                with self.assertRaises(ImproperlyConfigured) as err:
                    sidebar_menu.get_permissions_from_node(node)

        with self.subTest("Raises Improperly Configured view when both no perms and permission required"):
            # Define a valid node.
            node = {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Sample1",
                "icon": "fa fa-group",
            }
            # Patch the "get_permissions_from_view" method to return data that
            # would reflect a view that is improperly configured. Then attempt
            # to get the permissions from the node, which will ultimately pull
            # from the patched view method and cause the improperly configured
            with patch("adminlte2_pdq.templatetags.sidebar_menu.get_permissions_from_view") as get_perm_from_view:
                get_perm_from_view.return_value = {
                    "allow_anonymous_access": False,
                    "login_required": False,
                    "allow_without_permissions": True,
                    "one_of_permissions": ["foobar"],
                    "full_permissions": None,
                }
                with self.assertRaises(ImproperlyConfigured) as err:
                    sidebar_menu.get_permissions_from_node(node)

        with self.subTest("Raises Improperly Configured view when both anonymous and permission required"):
            # Define a valid node.
            node = {
                "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
                "text": "Sample1",
                "icon": "fa fa-group",
            }
            # Patch the "get_permissions_from_view" method to return data that
            # would reflect a view that is improperly configured. Then attempt
            # to get the permissions from the node, which will ultimately pull
            # from the patched view method and cause the improperly configured
            with patch("adminlte2_pdq.templatetags.sidebar_menu.get_permissions_from_view") as get_perm_from_view:
                get_perm_from_view.return_value = {
                    "allow_anonymous_access": True,
                    "login_required": False,
                    "allow_without_permissions": False,
                    "one_of_permissions": ["foobar"],
                    "full_permissions": None,
                }
                with self.assertRaises(ImproperlyConfigured) as err:
                    sidebar_menu.get_permissions_from_node(node)

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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Route was hash so should get empty lists.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node permissions set as string"):
            # Should succeed, and permission is converted to iterable of size 1.

            # Define node.
            node = {
                "route": "adminlte2_pdq:demo-css",
                "text": "Demo CSS",
                "icon": "fa fa-file",
                "one_of_permissions": "add_sample2",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual((node["one_of_permissions"],), one_of_permissions)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
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
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual([], full_permissions)

        with self.subTest("Node permissions set as string"):
            # Should succeed, and permission is converted to iterable of size 1.

            # Define node.
            node = {
                "route": "adminlte2_pdq:demo-css",
                "text": "Demo CSS",
                "icon": "fa fa-file",
                "permissions": "add_sample1",
            }

            # Call function to test.
            return_data = sidebar_menu.get_permissions_from_node(node)
            allow_anonymous_access = return_data["allow_anonymous_access"]
            login_required = return_data["login_required"]
            allow_without_permissions = return_data["allow_without_permissions"]
            one_of_permissions = return_data["one_of_permissions"]
            full_permissions = return_data["full_permissions"]

            # Verify returned data.
            self.assertFalse(allow_anonymous_access)
            self.assertFalse(login_required)
            self.assertFalse(allow_without_permissions)
            self.assertEqual([], one_of_permissions)
            self.assertEqual((node["permissions"],), full_permissions)

    # endregion get_permissions_from_node() Function

    # region ensure_node_has_url_property() Function

    def test__ensure_node_has_url_property__success(self):
        """Test ensure node has url property success"""

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
        """Test ensure node has url property failure"""

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
        """Test check for login whitelisted node where node not in list"""
        node = {
            "route": "foobar",
            "text": "Sample Form",
            "icon": "fa fa-file",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertFalse(is_whitelisted)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:sample_form"])
    def test__check_for_login_whitelisted_node__node_in_list(self):
        """Test check for login whitelisted node where node is in list"""
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
        """Test check for strict whitelisted node where node not in list."""
        node = {
            "route": "foobar",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertFalse(is_whitelisted)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:sample2"])
    def test__check_for_strict_whitelisted_node__node_in_list(self):
        """Test check for strict whitelisted node where node is in list."""
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
        """Test check for one permission."""

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
        """Test check for all permissions"""

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
        """Test check for one permission in node list"""

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
        """Test check for node that matches request path."""

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

    def test__determine_node_active_status(self):
        """Test the the active status for a node is set properly"""
        # pylint:disable=protected-access

        # Setup a basic node used for the tests
        node = {
            "url": "/home/",
            "text": "Sample1",
            "icon": "fa fa-group",
        }
        # Setup a fake request object to use with testing
        request = HttpRequest()
        request.path = "/home/"

        with self.subTest("Active True when exact match"):
            request.path = "/home/"
            active = sidebar_menu._determine_node_active_status(node, request)
            self.assertTrue(active)

        with self.subTest("Active True when starts with match"):
            request.path = "/home/some/sub/url/"
            active = sidebar_menu._determine_node_active_status(node, request)
            self.assertTrue(active)

        with self.subTest("Active False when no match"):
            request.path = "/homey_da_clown/"
            active = sidebar_menu._determine_node_active_status(node, request)
            self.assertFalse(active)

        with self.subTest("Active True when exact match and exact required"):
            node["active_requires_exact_url_match"] = True
            request.path = "/home/"
            active = sidebar_menu._determine_node_active_status(node, request)
            self.assertTrue(active)

        with self.subTest("Active False when not exact match and exact required"):
            node["active_requires_exact_url_match"] = True
            request.path = "/home/some/sub/url/"
            active = sidebar_menu._determine_node_active_status(node, request)
            self.assertFalse(active)
