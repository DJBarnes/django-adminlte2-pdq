"""
Tests for Mixins
"""

# System Imports.

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST


# Module Variables.
UserModel = get_user_model()
WHITELIST_VIEWS = [
    "adminlte2_pdq_tests:class-standard",
    "adminlte2_pdq_tests:class-allow-anonymous-access",
    "adminlte2_pdq_tests:class-login-required",
    "adminlte2_pdq_tests:class-allow-without-permissions",
    "adminlte2_pdq_tests:class-one-permission-required",
    "adminlte2_pdq_tests:class-full-permissions-required",
]
LOGIN_WHITELIST_VIEWS = LOGIN_EXEMPT_WHITELIST + WHITELIST_VIEWS
PERM_WHITELIST_VIEWS = STRICT_POLICY_WHITELIST + WHITELIST_VIEWS


class BaseMixinTextCase(IntegrationTestCase):
    """Base class for Mixin tests."""

    # region Expected Test Messages

    pdq__user_failed_perm_check = (
        "AdminLtePdq Warning: Attempted to access class-based view '{view_name}' which "
        "requires permissions, and user permission requirements were not met. "
        "Redirected to project home instead. \n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/"
    )

    # BUG: Some instances of accessing a Mixin reads as a decorator instead.
    #   Possibly resolved: Might have just been poorly organized testing urls. Double check later.
    pdq_loose__allow_anonymous_access_decorator_message = (
        "AdminLtePdq Error: The 'allow_anonymous_access' decorator is not supported in AdminLtePdq "
        "LOOSE mode. This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_without_permissions_decorator_message = (
        "AdminLtePdq Error: The 'allow_without_permissions' decorator is not supported in AdminLtePdq "
        "LOOSE mode. This decorator only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_anonymous_access_mixin_message = (
        "AdminLtePdq Error: The 'AllowAnonymousAccess' mixin is not supported in AdminLtePdq "
        "LOOSE mode. This mixin only exists for clarity of permission access in STRICT mode."
    )
    pdq_loose__allow_without_permissions_mixin_message = (
        "AdminLtePdq Error: The 'AllowWithoutPermissions' mixin is not supported in AdminLtePdq "
        "LOOSE mode. This mixin only exists for clarity of permission access in STRICT mode."
    )

    pdq_login__allow_anonymous_access_whitelist_overlap_message = (
        "AdminLtePdq Warning: The class-based view 'AllowAnonymousAccessView' has an 'AllowAnonymousAccess' "
        "mixin, but is also in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST. These two effectively "
        "achieve the same functionality."
    )
    pdq_login__login_required_mixin_message = (
        "AdminLtePdq Error: The 'LoginRequired' mixin is not supported in AdminLtePdq LOGIN REQUIRED mode. "
        "Having LOGIN REQUIRED mode on implicitly assumes login is required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the 'AllowAnonymousAccess' mixin."
    )
    pdq_loose__login_required_mixin_login_whitelist_message = (
        "AdminLtePdq Error: The class-based view 'LoginRequiredView' has a 'LoginRequired' "
        "mixin, but is in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST setting. Please remove one."
    )
    pdq_login__allow_without_permissions_mixin_message = (
        "AdminLtePdq Error: The 'AllowWithoutPermissions' mixin is not supported in AdminLtePdq "
        "LOGIN REQUIRED mode. This mixin only exists for clarity of permission access in STRICT mode."
    )

    pdq_strict__no_mixin_message = (
        "AdminLtePdq Warning: The class-based view 'StandardView' has permission "
        "requirements, but does not have any permissions set. "
        "This means that this view is inaccessible until permissions "
        "are set for the view.\n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )
    pdq_strict__login_required_mixin_message = (
        "AdminLtePdq Error: The 'LoginRequired' mixin is not supported in AdminLtePdq STRICT mode. "
        "Having STRICT mode on implicitly assumes login and permissions are required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the 'AllowAnonymousAccess' or 'AllowWithoutPermissions' mixins."
    )
    pdq_strict__allow_without_permissions_whitelist_overlap_message = (
        "AdminLtePdq Warning: The class-based view 'AllowWithoutPermissionsView' has an "
        "'AllowWithoutPermissions' mixin, but is also in the ADMINLTE2_STRICT_POLICY_WHITELIST. "
        "These two effectively achieve the same functionality."
    )
    pdq_strict__one_permission_required_whitelist_overlap_message = (
        "AdminLtePdq Error: The class-based view 'OnePermissionRequiredView' has a permission "
        "mixin, but is in the ADMINLTE2_STRICT_POLICY_WHITELIST setting. Please remove one."
    )
    pdq_strict__full_permission_required_whitelist_overlap_message = (
        "AdminLtePdq Error: The class-based view 'FullPermissionsRequiredView' has a permission "
        "mixin, but is in the ADMINLTE2_STRICT_POLICY_WHITELIST setting. Please remove one."
    )
    pdq_strict__ineffective_login_whitelist_message = (
        "AdminLtePdq Warning: The class-based view '{view_name}' is login whitelisted, "
        "but the view still requires permissions. A user must login to have permissions, so the login whitelist is "
        "redundant and probably not achieving the desired effect. Correct this by adding the view to "
        "the permission whitelist setting (ADMINLTE2_STRICT_POLICY_WHITELIST), or by adding the "
        "'AllowWithoutPermissions' mixin."
    )
    pdq_strict__ineffective_login_whitelist_message__no_mixin = pdq_strict__ineffective_login_whitelist_message.format(
        view_name="StandardView"
    )
    pdq_strict__ineffective_login_whitelist_message__anonymous_access = (
        pdq_strict__ineffective_login_whitelist_message.format(view_name="AllowAnonymousAccessView")
    )
    pdq__ineffective_login_whitelist_message__one_of_perms = pdq_strict__ineffective_login_whitelist_message.format(
        view_name="OnePermissionRequiredView"
    )
    pdq__ineffective_login_whitelist_message__full_perms = pdq_strict__ineffective_login_whitelist_message.format(
        view_name="FullPermissionsRequiredView"
    )

    pdq__allow_without_permissions__conflicting_message = (
        "AdminLtePdq Warning: The class-based view 'BleedingConflictingPermissionsView' is permission exempt, "
        "but has some permission requirements set. "
        "This means that this view is accessible to anyone authenticated, and the "
        "permissions are ineffective.\n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )
    pdq__no_permissions_one__message = (
        "AdminLtePdq Warning: The class-based view 'BleedingOnePermissionMissingPermissionsView' "
        "has permission requirements, but does not have any permissions set. "
        "This means that this view is inaccessible until permissions are set for the view.\n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )
    pdq__no_permissions_full__message = (
        "AdminLtePdq Warning: The class-based view 'BleedingFullPermissionMissingPermissionsView' "
        "has permission requirements, but does not have any permissions set. "
        "This means that this view is inaccessible until permissions are set for the view.\n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    )

    # endregion Expected Test Messages

    def setUp(self, *args, **kwargs):

        # Call parent logic.
        super().setUp(*args, **kwargs)

        self.permission_content_type = ContentType.objects.get_for_model(Permission)
        self.factory = RequestFactory()

        # Generate test permissions.

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
        group_instance = Group.objects.create(name="view_bar")
        group_instance.permissions.add(view_foo)
        group_instance = Group.objects.create(name="delete_bar")
        group_instance.permissions.add(delete_foo)
        group_instance = Group.objects.create(name="unused_bar")
        group_instance.permissions.add(unused_foo)

        # Define various group sets to test against.
        self.full_groups = Group.objects.filter(name__in=("add_bar", "change_bar"))
        self.partial_groups = Group.objects.filter(name="add_bar")

        # Define our actual users to test against.

        # Easy access to anonymous user.
        self.anonymous_user = AnonymousUser()

        # Add inactive user.
        self.inactive_user = self.get_user("inactive_jacob")
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # Add no permissions/groups to none_user.
        self.none_user = self.get_user("joe_none")

        # Add permission auth.add_foo to partial_perm_user.
        self.partial_perm_user = self.get_user("jane_partial")
        self.add_user_permission("add_foo", user=self.partial_perm_user)

        # Add permissions auth.add_foo and auth.change_foo to full_perm_user.
        self.full_perm_user = self.get_user("john_full")
        self.add_user_permission("add_foo", user=self.full_perm_user)
        self.add_user_permission("change_foo", user=self.full_perm_user)

        # Add no permissions/groups to staff none_user.
        self.none_staff_user = self.get_user("jacob_staff_none")

        # Add permission auth.add_foo to staff partial_perm_user.
        self.partial_perm_staff_user = self.get_user("jack_staff_partial")
        self.add_user_permission("add_foo", user=self.partial_perm_staff_user)

        # Add permissions auth.add_foo and auth.change_foo to staff full_perm_user.
        self.full_perm_staff_user = self.get_user("jessie_staff_full")
        self.add_user_permission("add_foo", user=self.full_perm_staff_user)
        self.add_user_permission("change_foo", user=self.full_perm_staff_user)

        # Add only "unused" permission to this incorrect_group_user.
        self.incorrect_group_user = self.get_user("johnny_wrong")
        self.add_user_group("unused_bar", user=self.incorrect_group_user)

        # Add add_barr and change_bar groups to partial_group_user.
        self.partial_group_user = self.get_user("jimmy_partial")
        self.add_user_group("add_bar", user=self.partial_group_user)

        # Add add_barr and change_bar groups to full_group_user.
        self.full_group_user = self.get_user("jenny_full")
        self.add_user_group("add_bar", user=self.full_group_user)
        self.add_user_group("change_bar", user=self.full_group_user)

        # Add super user.
        self.super_user = self.get_user("super_jessica")
        self.super_user.is_superuser = True
        self.super_user.save()

        # Define user list for tests where all user types should behave the same.
        # List of all anonymous/unauthenticated users.
        self.user_list__unauthenticated = (
            [self.anonymous_user, "anonymous user"],
            [self.inactive_user, "inactive user"],
        )
        # List of all authenticated users without any permissions.
        self.user_list__no_permissions = (
            [self.none_user, "user with no permissions"],
            [self.none_staff_user, "staff user with no permissions"],
            [self.incorrect_group_user, "user with incorrect groups"],
        )
        # List of all authenticated users with some (but not all) permissions.
        self.user_list__partial_permissions = (
            [self.partial_perm_user, "user with one permission"],
            [self.partial_perm_staff_user, "staff user with one permission"],
            [self.partial_group_user, "user with one group"],
        )
        # List of all authenticated users will all permissions.
        self.user_list__full_permissions = (
            [self.full_perm_user, "user with full permissions"],
            [self.full_perm_staff_user, "staff user with full permissions"],
            [self.full_group_user, "user with full groups"],
            [self.super_user, "superuser"],
        )
        # List of all logged in/authenticated users.
        self.user_list__authenticated = (
            *self.user_list__no_permissions,
            *self.user_list__partial_permissions,
            *self.user_list__full_permissions,
        )
        # List of all possible user types.
        self.user_list__full = [
            *self.user_list__unauthenticated,
            *self.user_list__authenticated,
        ]

    def assertAdminPdqData(  # pylint:disable=invalid-name
        self,
        response,
        is_empty=False,
        decorator_name=None,
        allow_anonymous_access=False,
        login_required=False,
        allow_without_permissions=False,
        one_of_permissions=None,
        full_permissions=None,
    ):
        """Custom assertion to verify the state of the data after AdminLtePdq processing.

        :param response: Page response to parse data from for testing.
        :param is_empty: Bool indicating if AdminLteData in response should be empty. If so, no further tests are run.
        :param decorator_name: Expected decorator name value in AdminLteData response data.
        :param allow_anonymous_access: Expected allow_anonymous_access value in AdminLteData response data.
        :param login_required: Expected login_required value in AdminLteData response data.
        :param allow_without_permissions: Expected allow_without_permissions value in AdminLteData response data.
        :param one_of_permissions: Expected one_of_permissions value in AdminLteData response data.
        :param full_permissions: Expected full_permissions value in AdminLteData response data.
        """

        # Check if data is empty.
        # Should be the case in views without decorators/mixins, or such as for login redirects.
        if is_empty:
            self.assertFalse(hasattr(response, "admin_pdq_data"))

            # No AdminLteData so no further checks needed. Exit here.
            return

        # If we made it this far, then AdminLteData is expected. Do full checks.

        # First verify data is, in fact, present.
        self.assertTrue(hasattr(response, "admin_pdq_data"))
        data_dict = response.admin_pdq_data

        # Data acquired. Verify each expected item within.

        # Verify decorator name.
        self.assertEqual(decorator_name, data_dict["decorator_name"])

        # Verify allow_anonymous_access state.
        self.assertIn("allow_anonymous_access", data_dict)
        if bool(allow_anonymous_access):
            self.assertTrue(data_dict["allow_anonymous_access"])
        else:
            self.assertFalse(data_dict["allow_anonymous_access"])

        # Verify login_required state.
        self.assertIn("login_required", data_dict)
        if bool(login_required):
            self.assertTrue(data_dict["login_required"])
        else:
            self.assertFalse(data_dict["login_required"])

        # Verify allow_anonymous_access state.
        self.assertIn("allow_without_permissions", data_dict)
        if bool(allow_without_permissions):
            self.assertTrue(data_dict["allow_without_permissions"])
        else:
            self.assertFalse(data_dict["allow_without_permissions"])

        # Verify one_of_permissions state.
        self.assertIn("one_of_permissions", data_dict)
        if bool(one_of_permissions):
            self.assertEqual(
                one_of_permissions,
                tuple(data_dict["one_of_permissions"]),
            )
        else:
            self.assertIsNone(data_dict["one_of_permissions"])

        # Verify permissions_required (aka full_permissions) state.
        self.assertIn("full_permissions", data_dict)
        if bool(full_permissions):
            self.assertEqual(
                full_permissions,
                tuple(data_dict["full_permissions"]),
            )
        else:
            self.assertIsNone(data_dict["full_permissions"])
