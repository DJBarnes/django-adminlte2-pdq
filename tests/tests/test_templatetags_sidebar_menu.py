"""
Tests for Template Tags
"""

# System Imports.
from unittest.mock import patch

# Third-party Imports.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.template import Template, Context
from django.test import TestCase, override_settings, RequestFactory
from django.urls import NoReverseMatch

# Internal Imports.
from adminlte2_pdq.templatetags import sidebar_menu


# Module Variables.
UserModel = get_user_model()


class TemplateTagSidebarMenuTestCase(TestCase):
    """
    Test Template Tags and Helper Methods used in those template tags
    """

    # |-------------------------------------------------------------------------
    # | Setup
    # |-------------------------------------------------------------------------

    def setUp(self):
        self.anonymoususer = None
        self.superuser = None
        self.staffuser = None

    def _setup_anonymoususer(self):
        """Set up Anonymoususer"""
        self.anonymoususer = AnonymousUser()

    def _setup_superuser(self):
        """Set up Superuser"""
        self.superuser = UserModel()
        self.superuser.username = "testsuperuser"
        self.superuser.is_superuser = True
        self.superuser.save()

    def _setup_staffuser(self, permissions=None):
        """Set up Staff user"""
        self.staffuser = UserModel()
        self.staffuser.username = "teststaffuser"
        self.staffuser.is_staff = True
        self.staffuser.save()

        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.staffuser.user_permissions.add(perm_object)

    # |-------------------------------------------------------------------------
    # | Test that check for demo urls works
    # |-------------------------------------------------------------------------

    def test_default_routes_are_registered_method_works_when_routes_are_registered(self):
        """Test default routes are registered method works when routes are registered"""
        self.assertTrue(sidebar_menu._default_routes_are_registered())

    @override_settings(ROOT_URLCONF="tests.urls_empty")
    def test_default_routes_are_registered_method_fails_when_routes_are_not_registered(self):
        """Test default routes are registered method fails when routes are not registered"""
        self.assertFalse(sidebar_menu._default_routes_are_registered())

    # |-------------------------------------------------------------------------
    # | Test get_permissions_from_node for general errors
    # |-------------------------------------------------------------------------

    def test_get_permissions_from_node_raises_keyerror_when_route_is_missing(self):
        """Test get permissions from node raises KeyError when route is missing"""
        node = {
            "text": "Sample1",
            "icon": "fa fa-group",
        }

        with self.assertRaises(KeyError):

            sidebar_menu.get_permissions_from_node(node)

    def test_get_permissions_from_node_returns_empty_list_when_no_reverse_error_and_route_is_a_hash(self):
        """Test get permissions from node returns empty list when no reverse
        error and route is a hash"""
        node = {
            "route": "#",
            "text": "Sample1",
            "icon": "fa fa-group",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_raises_error_when_route_causes_a_reverse_error(self):
        """Test get permissions from node raises error when route causes a reverse error"""
        node = {
            "route": "foobar",
            "text": "Sample1",
            "icon": "fa fa-group",
        }

        with self.assertRaises(NoReverseMatch):
            sidebar_menu.get_permissions_from_node(node)

    # |-------------------------------------------------------------------------
    # | Test get_permissions_from_node for login_required
    # |-------------------------------------------------------------------------

    def test_get_permissions_from_node_pulls_login_required_from_direct_assignment(self):
        """Test get permissions from node pulls login_required from direct assignment"""
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_login_required_from_view_function(self):
        """Test get permissions from node pulls login_required from view function"""
        node = {
            "route": "adminlte2_pdq:sample_form",
            "text": "Sample Form",
            "icon": "fa fa-file",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_login_required_value_from_node_over_view_function_when_both_set(self):
        """Test get permissions from node pulls login required value from node over view function when both set"""
        node = {
            "route": "adminlte2_pdq:sample_form",
            "text": "Sample Form",
            "icon": "fa fa-file",
            "login_required": False,
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_login_required_from_view_with_hash_route_and_valid_url(self):
        """Test get permissions from node pull login_required from view with hash route and valid url"""
        node = {
            "route": "#",
            "text": "Sample Form",
            "icon": "fa fa-building",
            "url": "/sample_form/",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_returns_false_when_not_set_on_the_node(self):
        """Test get permissions from node returns false when not set on the node"""
        node = {
            "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
            "text": "Home",
            "icon": "fa fa-dashboard",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_pulls_login_required_from_direct_assignment_when_external_url(self):
        """Test get permissions from node pulls login_required from direct assignment_when_external_url"""
        node = {
            "route": "#",
            "text": "GitHub",
            "icon": "fa fa-github",
            "url": "https://github.com",
            "login_required": True,
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_returns_false_when_the_node_is_for_an_external_resource(self):
        """Test get permissions from node returns false when the node is for an external resource"""
        node = {
            "route": "#",
            "text": "External",
            "icon": "fa fa-github",
            "url": "https://github.com",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    # |-------------------------------------------------------------------------
    # | Test get_permissions_from_node for permissions
    # |-------------------------------------------------------------------------

    def test_get_permissions_from_node_pulls_permissions_from_direct_assigned_permissions(self):
        """Test get permissions from node pulls permissions from direct assigned permissions"""
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["add_sample1", "update_sample1"],
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual(node["permissions"], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_pulls_permissions_from_view_function(self):
        """Test get permissions from node pulls permissions from view function"""
        node = {
            "route": "adminlte2_pdq:sample1",
            "text": "Sample1",
            "icon": "fa fa-group",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertIn("auth.add_group", permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_permissions_from_node_over_view_function_when_both_set(self):
        """Test get permissions from node pulls permissions from node over view function when both set"""
        node = {
            "route": "adminlte2_pdq:sample1",
            "text": "Sample1",
            "icon": "fa fa-group",
            "permissions": [],
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_permissions_from_view_with_hash_route_and_valid_url(self):
        """Test get permissions from node pull permission from view with hash route and valid url"""
        node = {
            "route": "#",
            "text": "Sample1",
            "icon": "fa fa-building",
            "url": "/sample1/",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertIn("auth.add_group", permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_returns_permissions_empty_list_when_there_are_no_defined_permissions_on_the_node(
        self,
    ):
        """Test get permissions from node returns permissions empty list when there are no defined permissions on the node"""
        node = {
            "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
            "text": "Home",
            "icon": "fa fa-dashboard",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_pulls_permissions_from_direct_assigned_permissions_when_external_url(self):
        """Test get permissions from node pulls permissions from direct assigned permissions_when_external_url"""
        node = {
            "route": "#",
            "text": "GitHub",
            "icon": "fa fa-github",
            "url": "https://github.com",
            "permissions": ["add_sample1", "update_sample1"],
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual(node["permissions"], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_returns_permissions_empty_list_when_the_node_is_for_an_external_resource(self):
        """Test get permissions from node returns permissions empty list when the node is for an external resource"""
        node = {
            "route": "#",
            "text": "External",
            "icon": "fa fa-github",
            "url": "https://github.com",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    # |-------------------------------------------------------------------------
    # | Test get_permissions_from_node for one_of_permissions
    # |-------------------------------------------------------------------------

    def test_get_permissions_from_node_pulls_one_of_permissions_from_direct_assigned_permissions(self):
        """Test get permissions from node pulls one of permissions from direct assigned permissions"""
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["add_sample2", "update_sample2"],
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual(node["one_of_permissions"], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_pulls_one_of_permissions_from_view_function(self):
        """Test get permissions from node pulls one of permissions from view function"""
        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertIn("auth.add_permission", one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_one_of_permissions_from_node_over_view_function_when_both_set(self):
        """Test get permissions from node pulls one of permissions from node over view function when both set"""
        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "icon": "fa fa-building",
            "one_of_permissions": [],
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_pulls_one_of_permissions_from_view_with_hash_route_and_valid_url(self):
        """Test get permissions from node pull one of permissions from view with hash route and valid url"""
        node = {
            "route": "#",
            "text": "Sample2",
            "icon": "fa fa-building",
            "url": "/sample2/",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertIn("auth.add_permission", one_of_permissions)
        self.assertTrue(login_required)

    def test_get_permissions_from_node_returns_one_of_permission_empty_list_when_there_are_no_defined_permissions_on_the_node(
        self,
    ):
        """Test get permissions from node returns one of permission empty list when there are no defined permissions on the node"""
        node = {
            "route": getattr(settings, "ADMINLTE2_HOME_ROUTE", "adminlte2_pdq:home"),
            "text": "Home",
            "icon": "fa fa-dashboard",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_pulls_one_of_permissions_from_direct_assigned_one_of_permissions_when_external_url(
        self,
    ):
        """Test get permissions from node pulls one of permissions from direct assigned one of permissions_when_external_url"""
        node = {
            "route": "#",
            "text": "GitHub",
            "icon": "fa fa-github",
            "url": "https://github.com",
            "one_of_permissions": ["add_sample2", "update_sample2"],
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual(node["one_of_permissions"], one_of_permissions)
        self.assertFalse(login_required)

    def test_get_permissions_from_node_returns_one_of_permissions_empty_list_when_the_node_is_for_an_external_resource(
        self,
    ):
        """Test get permissions from node returns one of permissions empty list when the node is for an external resource"""
        node = {
            "route": "#",
            "text": "External",
            "icon": "fa fa-github",
            "url": "https://github.com",
        }

        permissions, one_of_permissions, login_required = sidebar_menu.get_permissions_from_node(node)

        self.assertEqual([], permissions)
        self.assertEqual([], one_of_permissions)
        self.assertFalse(login_required)

    # |-------------------------------------------------------------------------
    # | Test ensure_node_has_url_property
    # |-------------------------------------------------------------------------

    def test_ensure_node_has_url_property_works_when_node_has_url_property_defined(self):
        """Test ensure node has url property works when node has url property defined"""
        node = {"route": "adminlte2_pdq:sample2", "text": "Sample2", "icon": "fa fa-building", "url": "/foobar/"}

        sidebar_menu.ensure_node_has_url_property(node)

        self.assertEqual("/foobar/", node["url"])

    def test_ensure_node_has_url_property_adds_url_property_from_valid_route(self):
        """Test ensure node has url property adds url property from valid route"""
        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        sidebar_menu.ensure_node_has_url_property(node)

        self.assertEqual("/sample2/", node["url"])

    def test_ensure_node_has_url_property_sets_url_to_a_hash_when_route_is_a_hash(self):
        """Test ensure node has url property sets url to a hash when route is a hash"""
        node = {
            "route": "#",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        sidebar_menu.ensure_node_has_url_property(node)

        self.assertEqual("#", node["url"])

    def test_ensure_node_has_url_property_raises_key_error_when_route_field_missing(self):
        """Test ensure node has url property raises KeyError when route field missing"""
        node = {
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        with self.assertRaises(KeyError):
            sidebar_menu.ensure_node_has_url_property(node)

    def test_ensure_node_has_url_property_raises_reverse_error_when_route_is_not_valid(self):
        """Test ensure node has url property raises reverse error when route is not valid"""
        node = {
            "route": "foobar",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        with self.assertRaises(NoReverseMatch):
            sidebar_menu.ensure_node_has_url_property(node)

    # |-------------------------------------------------------------------------
    # | Test check_for_login_whitelisted_node
    # |-------------------------------------------------------------------------

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:sample_form"])
    def test_check_for_login_whitelisted_node_returns_true_when_node_in_list(self):
        """Test check for strict whitelisted node returns true when node in list"""
        node = {
            "route": "adminlte2_pdq:sample_form",
            "text": "Sample Form",
            "icon": "fa fa-file",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertTrue(is_whitelisted)

    def test_check_for_login_whitelisted_node_returns_false_when_node_not_in_list(self):
        """Test check for strict whitelisted node returns false when node not in list"""
        node = {
            "route": "foobar",
            "text": "Sample Form",
            "icon": "fa fa-file",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertFalse(is_whitelisted)

    # |-------------------------------------------------------------------------
    # | Test check_for_strict_whitelisted_node
    # |-------------------------------------------------------------------------

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:sample2"])
    def test_check_for_strict_whitelisted_node_returns_true_when_node_in_list(self):
        """Test check for strict whitelisted node returns true when node in list"""
        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertTrue(is_whitelisted)

    def test_check_for_strict_whitelisted_node_returns_false_when_node_not_in_list(self):
        """Test check for strict whitelisted node returns false when node not in list"""
        node = {
            "route": "foobar",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        is_whitelisted = sidebar_menu.check_for_strict_whitelisted_node(node)

        self.assertFalse(is_whitelisted)

    # |-------------------------------------------------------------------------
    # | Test check_for_all_permissions
    # |-------------------------------------------------------------------------

    def test_check_for_all_permissions_returns_true_when_user_is_superuser(self):
        """Test check for all permissions returns true when user is superuser"""
        self._setup_superuser()

        permissions = ["does_not_matter_since_superuser"]

        allowed = sidebar_menu.check_for_all_permissions(self.superuser, permissions)

        self.assertTrue(allowed)

    def test_check_for_all_permissions_returns_true_when_user_is_not_su_but_has_perms(self):
        """Test check for all permissions returns true when user is not su but has perms"""
        self._setup_staffuser("add_group")

        permissions = ["auth.add_group"]

        allowed = sidebar_menu.check_for_all_permissions(self.staffuser, permissions)

        self.assertTrue(allowed)

    def test_check_for_all_permissions_returns_false_when_permissions_is_empty_list(self):
        """Test check for all permissions returns false when permissions is empty list"""
        self._setup_staffuser("add_group")

        permissions = []

        allowed = sidebar_menu.check_for_all_permissions(self.staffuser, permissions)

        self.assertFalse(allowed)

    def test_check_for_all_permissions_returns_false_when_user_does_not_have_perms(self):
        """Test check for all permissions returns false when user does not have perms"""
        self._setup_staffuser()

        permissions = ["user_does_not_have_this_one"]

        allowed = sidebar_menu.check_for_all_permissions(self.staffuser, permissions)

        self.assertFalse(allowed)

    # |-------------------------------------------------------------------------
    # | Test check_for_one_permission
    # |-------------------------------------------------------------------------

    def test_check_for_one_permission_returns_true_when_user_is_superuser(self):
        """Test check for one permission returns true when user is superuser"""
        self._setup_superuser()

        permissions = ["does_not_matter_since_superuser"]

        allowed = sidebar_menu.check_for_one_permission(self.superuser, permissions)

        self.assertTrue(allowed)

    def test_check_for_one_permission_returns_true_when_user_is_not_su_but_has_perms(self):
        """Test check for one permission returns true when user is not su but has perms"""
        self._setup_staffuser("add_group")

        permissions = ["auth.add_group", "auth.update_group"]

        allowed = sidebar_menu.check_for_one_permission(self.staffuser, permissions)

        self.assertTrue(allowed)

    def test_check_for_one_permission_returns_false_when_permissions_is_empty_list(self):
        """Test check for one permission returns false when permissions is empty list"""
        self._setup_staffuser("add_group")

        permissions = []

        allowed = sidebar_menu.check_for_one_permission(self.staffuser, permissions)

        self.assertFalse(allowed)

    def test_check_for_one_permission_returns_false_when_user_does_not_have_perms(self):
        """Test check for one permission returns false when suer does not have perms"""
        self._setup_staffuser()

        permissions = ["user_does_not_have_this_one"]

        allowed = sidebar_menu.check_for_one_permission(self.staffuser, permissions)

        self.assertFalse(allowed)

    # |-------------------------------------------------------------------------
    # | Test is_allowed_node
    # |-------------------------------------------------------------------------

    # NOTE: We only need to test the login_required / permissions on the node as
    # we have other tests to verify that it is possible to get the
    # login_required and permissions from the view associated with the node.
    # Those tests also ensure that node permissions take precedence over view ones.

    # Test format is as follows:
    # def test_is_allowed_node_{result}_{user}_{login}_{strict}_{node}_{login_WL}_{strict_WL}

    # Additional details
    # {login} means that the LOGIN_REQUIRED middleware is active.
    # {strict} means that the STRICT_POLICY middleware is active.
    # {node} means what the node requirements are. Options are: off, login, perm, one_perm.
    # {login_WL} means that the node's route is listed in the LOGIN_EXEMPT_WHITELIST - omitted means it isn't.
    # {strict_WL} means that the node's route is listed in the STRICT_POLICY_WHITELIST - omitted means it isn't.

    # The tests do not test a combination of node options.
    # EX: no test for login required and required perms as requiring perms implicitly means user logged in.

    # **************************************************************************
    # Anonymous User
    # **************************************************************************

    # Anonymous - login off - strict off

    def test_is_allowed_node_is_true_when_user_anonymous_login_off_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_off_strict_off_node_off"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_off_node_login(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_off_node_login"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_off_node_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_off_node_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_off_node_one_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login on - strict off

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_off(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_off"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_login(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_login"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_one_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login on - strict off - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_off_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_off_node_off_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_off_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_off_node_login_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login off - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_off(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_off"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_login(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_login"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_one_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login off - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_anonymous_login_off_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_off_strict_on_node_off_strict_wl_on"""

        # TODO: Failing test. I honestly don't get what this one is trying to do.
        #       It's strict mode but an anonymous user should be allowed to view node?
        #       That makes no sense.

        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_login_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_perm_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_off_strict_on_node_one_perm_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login on - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_off(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_off"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_login(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_login"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login on - strict on - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_on_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_on_node_off_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_on_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_on_node_login_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm_login_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login on - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_off_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_login_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # Anonymous - login on - strict on - login whitelist on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_on_node_off_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_anonymous_login_on_strict_on_node_off_login_wl_on_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_login_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_login_login_wl_on_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_perm_login_wl_on_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on(
        self,
    ):
        """test_is_allowed_node_is_false_when_user_anonymous_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on"""
        self._setup_anonymoususer()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.anonymoususer, node)

        self.assertFalse(allowed)

    # **************************************************************************
    # Staff User - No Perms
    # **************************************************************************

    # Logged In No Perm - login off - strict off

    def test_is_allowed_node_is_true_when_user_staff_login_off_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_staff_login_off_strict_off_node_off"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_staff_login_off_strict_off_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_login_off_strict_off_node_login"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_off_node_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_off_node_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_off_node_one_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login on - strict off

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_off"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_login"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_one_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login on - strict off - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_off_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_off_node_login_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login off - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_off(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_off"""

        # TODO: Once again, this test doesn't make sense.
        #       To be precise, the actual test itself seems to maybe be correct but fixing
        #       it seems to cause major unexpected problems.
        #
        #       It's strict mode and no permissions defined so no one should be able to access.
        #       This test is easily fixed by changing sidebar_menu.py line 346 to
        #       include a check of `if STRICT_POLICY or full_permissions or one_of_permissions`
        #       However doing so makes nearly all other tests in this file fail.
        #
        #       Aka this test itself kinda checks out but clearly overall test logic is wonky.
        #       Needs discussion, leaving as-is for now.

        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_login_off_strict_on_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_login_off_strict_on_node_login"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_one_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login off - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_off_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_off_strict_on_node_off_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_off_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_off_strict_on_node_login_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_perm_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_off_strict_on_node_one_perm_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login on - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login on - strict on - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm_login_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login on - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # Logged In No Perm - login on - strict on - login whitelist on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_off_login_wl_on_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_login_on_strict_on_node_login_login_wl_on_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_perm_login_wl_on_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_false_when_user_staff_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on"""
        self._setup_staffuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    # **************************************************************************
    # Staff User - All Perms
    # **************************************************************************

    # Logged In All Perm - login off - strict off

    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_off"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_login"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_off_node_one_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login on - strict off

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_off"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_login"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_one_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login on - strict off - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_off_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_login_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login off - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_false_when_user_staff_perm_login_off_strict_on_node_off(self):
        """test_is_allowed_node_is_false_when_user_staff_perm_login_off_strict_on_node_off"""

        # TODO: Similar to above failing TODO, this one doesn't make sense either.

        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertFalse(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_login"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_one_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login off - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_off_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_login_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_perm_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_off_strict_on_node_one_perm_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login on - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login on - strict on - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm_login_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login on - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # Logged In All Perm - login on - strict on - login whitelist on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_off_login_wl_on_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_login_login_wl_on_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_perm_login_wl_on_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on(
        self,
    ):
        """test_is_allowed_node_is_true_when_user_staff_perm_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on"""
        self._setup_staffuser(["add_group"])
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.staffuser, node)

        self.assertTrue(allowed)

    # **************************************************************************
    # Superuser
    # **************************************************************************

    # Superuser - login off - strict off

    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_off"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_login(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_login"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_off_node_one_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login on - strict off

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_off(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_off"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_login(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_login"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_one_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login on - strict off - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_off_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_login_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_off_node_perm_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login off - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_off(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_off"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_login(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_login"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_one_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login off - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_off_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_login_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_perm_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_off_strict_on_node_one_perm_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login on - strict on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login on - strict on - login whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm_login_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm_login_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login on - strict on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # Superuser - login on - strict on - login whitelist on - strict whitelist on

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_off_login_wl_on_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_login_login_wl_on_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "login_required": True,
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm_login_wl_on_strict_wl_on(self):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_perm_login_wl_on_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_REQUIRED", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.LOGIN_EXEMPT_WHITELIST", ["adminlte2_pdq:demo-css"])
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)
    @patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY_WHITELIST", ["adminlte2_pdq:demo-css"])
    def test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on(
        self,
    ):
        """test_is_allowed_node_is_true_when_user_superuser_login_on_strict_on_node_one_perm_login_wl_on_strict_wl_on"""
        self._setup_superuser()
        node = {
            "route": "adminlte2_pdq:demo-css",
            "text": "Demo CSS",
            "icon": "fa fa-file",
            "one_of_permissions": ["auth.add_group"],
        }

        allowed = sidebar_menu.is_allowed_node(self.superuser, node)

        self.assertTrue(allowed)

    # |-------------------------------------------------------------------------
    # | Test check_for_one_permission_in_node_list
    # |-------------------------------------------------------------------------

    def test_check_for_one_permission_in_node_list_returns_true_for_superuser_regardless_of_tree_size(self):
        """Test check for one permission in node list returns true for superuser
        regardless of tree size"""
        self._setup_superuser()

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

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.superuser, nodes)

        self.assertTrue(allowed)

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.superuser, nodetree)

        self.assertTrue(allowed)

    def test_check_for_one_permission_in_node_list_returns_true_for_single_node_user_can_access(self):
        """Test check for one permission in node list returns true for single
        node user can access"""
        self._setup_staffuser("add_permission")

        nodes = [
            {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
            }
        ]

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staffuser, nodes)

        self.assertTrue(allowed)

    def test_check_for_one_permission_in_node_list_returns_true_for_tree_of_two_nodes_user_can_access(self):
        """Test check for one permission in node list returns true for tree of
        two nodes user can access"""
        self._setup_staffuser("add_permission")

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

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staffuser, nodes)

        self.assertTrue(allowed)

    def test_check_for_one_permission_in_node_list_returns_true_for_tree_of_three_nodes_user_can_access(self):
        """Test check for one permission in node list returns true for three of
        three nodes user can access"""
        self._setup_staffuser("add_permission")

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

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staffuser, nodes)

        self.assertTrue(allowed)

    def test_check_for_one_permission_in_node_list_returns_false_for_single_node_user_can_not_access(self):
        """Test check for one permission in node list returns false for single
        node user can not access"""
        self._setup_staffuser("add_group")

        nodes = [
            {
                "route": "adminlte2_pdq:sample2",
                "text": "Sample2",
                "icon": "fa fa-building",
            }
        ]

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staffuser, nodes)

        self.assertFalse(allowed)

    def test_check_for_one_permission_in_node_list_returns_false_for_tree_of_two_nodes_user_can_not_access(self):
        """Test check for one permission in node list returns false for tree of
        two nodes user can not access"""
        self._setup_staffuser("add_group")

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

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staffuser, nodes)

        self.assertFalse(allowed)

    def test_check_for_one_permission_in_node_list_returns_false_for_tree_of_three_nodes_user_can_not_access(self):
        """Test check for one permission in node list returns false for tree of
        three nodes user can not access"""
        self._setup_staffuser("add_group")

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

        allowed = sidebar_menu.check_for_one_permission_in_node_list(self.staffuser, nodes)

        self.assertFalse(allowed)

    # |-------------------------------------------------------------------------
    # | Test check_for_node_that_matches_request_path
    # |-------------------------------------------------------------------------

    def test_check_for_node_that_matches_request_path_returns_false_for_no_nodes(self):
        """Test check for node that matches request path returns false for no nodes"""
        nodes = []

        request = RequestFactory().get("/sample2/")

        match = sidebar_menu.check_for_node_that_matches_request_path(request, nodes)

        self.assertFalse(match)

    def test_check_for_node_that_matches_request_path_returns_true_for_single_node_with_a_match(self):
        """Test check for node that matches request path returns true for single
        node with a match"""
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

    def test_check_for_node_that_matches_request_path_returns_true_for_tree_of_two_nodes_with_a_match(self):
        """Test check for node that matches request path returns true for tree
        of two nodes with a match"""
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

    def test_check_for_node_that_matches_request_path_returns_true_for_tree_of_three_nodes_with_a_match(self):
        """Test check for node that matches request path returns true for tree
        of three nodes with a match"""
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

    def test_check_for_node_that_matches_request_path_returns_false_for_single_node_without_a_match(self):
        """Test check for node that matches request path returns false for single
        node without a match"""
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

    def test_check_for_node_that_matches_request_path_returns_false_for_tree_of_two_nodes_without_a_match(self):
        """Test check for node that matches request path returns false for tree
        of two nodes without a match"""
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

    def test_check_for_node_that_matches_request_path_returns_false_for_tree_of_three_nodes_without_a_match(self):
        """Test check for node that matches request path returns false for tree
        of three nodes without a match"""
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

    # |-------------------------------------------------------------------------
    # | Test render_XXXX template tags
    # |-------------------------------------------------------------------------

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=False)
    def test_render_menu_renders_when_user_has_access_but_excludes_admin_when_include_admin_off(self):
        """Test render menu renders when user has access but excludes admin when
        include admin off"""
        self._setup_staffuser(
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
        request.user = self.staffuser

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
                "user": self.staffuser,
                "ADMINLTE2_MENU": menu,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_menu %}")

        rendered_template = template_to_render.render(context)

        self.assertNotIn("Authentication", rendered_template)
        self.assertNotIn("<span>User</span>", rendered_template)
        self.assertIn('<li class="header">', rendered_template)
        self.assertIn("Samples", rendered_template)
        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=True)
    def test_render_menu_renders_when_user_has_access_and_includes_admin_when_include_admin_on(self):
        """Test render menu renders when user has access and includes admin when include admin on"""
        self._setup_staffuser(
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
        request.user = self.staffuser

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
                "user": self.staffuser,
                "ADMINLTE2_MENU": menu,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_menu %}")

        rendered_template = template_to_render.render(context)

        self.assertIn("Authentication", rendered_template)
        self.assertIn('<span class="node-link-text" title="User">User</span>', rendered_template)
        self.assertIn("Home", rendered_template)
        self.assertIn('<li class="header">', rendered_template)
        self.assertIn("Samples", rendered_template)
        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=True)
    def test_render_menu_renders_when_user_has_access_and_includes_admin_and_menu_first_when_include_admin_on(self):
        """Test render menu renders when user has access and includes admin and
        menu first when include admin on"""
        self._setup_staffuser(
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
        request.user = self.staffuser

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
                "user": self.staffuser,
                "ADMINLTE2_MENU": menu,
                "ADMINLTE2_MENU_FIRST": menu_first,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_menu %}")

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

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=True)
    def test_render_menu_renders_when_user_has_access_and_includes_admin_and_menu_last_when_include_admin_on(self):
        """Test render menu renders when user has access and includes admin and
        menu last when include admin on"""
        self._setup_staffuser(
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
        request.user = self.staffuser

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
                "user": self.staffuser,
                "ADMINLTE2_MENU": menu,
                "ADMINLTE2_MENU_LAST": menu_last,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_menu %}")

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

    @override_settings(ADMINLTE2_INCLUDE_ADMIN_NAV_ON_MAIN_PAGES=True)
    def test_render_menu_renders_when_user_has_access_and_includes_admin_and_menu_first_and_menu_last_when_include_admin_on(
        self,
    ):
        """Test render menu renders when user has access and includes admin and
        menu first and menu last when include admin on"""
        self._setup_staffuser(
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
        request.user = self.staffuser

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
                "user": self.staffuser,
                "ADMINLTE2_MENU": menu,
                "ADMINLTE2_MENU_FIRST": menu_first,
                "ADMINLTE2_MENU_LAST": menu_last,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_menu %}")

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

    def test_render_section_renders_when_user_has_access(self):
        """Test render section renders when user has access"""
        self._setup_staffuser("add_permission")

        request = RequestFactory().get("/sample2/")
        request.user = self.staffuser

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
                "user": self.staffuser,
                "section": section,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_section section %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<li class="header">', rendered_template)
        self.assertIn("Samples", rendered_template)
        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    def test_render_nodes_renders_when_user_has_access(self):
        """Test render nodes renders when user has access"""
        self._setup_staffuser("add_permission")

        request = RequestFactory().get("/sample2/")
        request.user = self.staffuser

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
                "user": self.staffuser,
                "nodes": nodes,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_nodes nodes %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    def test_render_tree_renders_when_user_has_access(self):
        """Test render tree renders when user has access"""
        self._setup_staffuser("add_permission")

        request = RequestFactory().get("/sample2/")
        request.user = self.staffuser

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
                "user": self.staffuser,
                "node": node,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_tree node %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    def test_render_tree_renders_with_default_icon_when_user_has_access_and_node_lacks_icon(self):
        """Test render tree renders with default icon when user has access and
        node lacks icon"""
        self._setup_staffuser("add_permission")

        request = RequestFactory().get("/sample2/")
        request.user = self.staffuser

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
                "user": self.staffuser,
                "node": node,
                "request": request,
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_tree node %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<li class="treeview">', rendered_template)
        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertNotIn("fa fa-leaf", rendered_template)
        self.assertIn("not-found", rendered_template)

    def test_render_link_renders_when_user_has_access(self):
        """Test render link renders when user has access"""
        self._setup_staffuser("add_permission")

        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "icon": "fa fa-building",
        }

        context = Context(
            {
                "user": self.staffuser,
                "node": node,
                "request": {
                    "path": "/some/path",
                },
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_link node %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertIn("fa fa-building", rendered_template)

    def test_render_link_renders_with_no_icon_when_not_specified_and_when_user_has_access(self):
        """Test render link renders with no icon when not specified and when user has access"""
        self._setup_staffuser("add_permission")

        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
        }

        context = Context(
            {
                "user": self.staffuser,
                "node": node,
                "request": {
                    "path": "/some/path",
                },
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_link node %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<span class="node-link-text" title="Sample2">Sample2</span>', rendered_template)
        self.assertNotIn("fa fa-building", rendered_template)

    def test_render_link_renders_dynamic_text_via_string_returning_hook_when_user_has_access(self):
        """Test render renders dynamic text via hook when user has access"""
        self._setup_staffuser("add_permission")

        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "hook": "tests.utils.valid_string_hook_function",
            "hook_args": ["foo"],
            "hook_kwargs": {"kwarg1": "bar"},
        }

        context = Context(
            {
                "user": self.staffuser,
                "node": node,
                "request": {
                    "path": "/some/path",
                },
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_link node %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<span class="node-link-text" title="foobar foo bar">foobar foo bar</span>', rendered_template)
        self.assertNotIn("fa fa-building", rendered_template)

    def test_render_link_renders_dynamic_text_via_tuple_returning_hook_when_user_has_access(self):
        """Test render link renders dynamic text via tuple returning hook when user has access"""
        self._setup_staffuser("add_permission")

        node = {
            "route": "adminlte2_pdq:sample2",
            "text": "Sample2",
            "hook": "tests.utils.valid_tuple_hook_function",
            "hook_args": ["foo"],
            "hook_kwargs": {"kwarg1": "bar"},
        }

        context = Context(
            {
                "user": self.staffuser,
                "node": node,
                "request": {
                    "path": "/some/path",
                },
            }
        )

        template_to_render = Template("{% load sidebar_menu %}" "{% render_link node %}")

        rendered_template = template_to_render.render(context)

        self.assertIn('<span class="node-link-text" title="foo bar">foobar</span>', rendered_template)
        self.assertNotIn("fa fa-building", rendered_template)
