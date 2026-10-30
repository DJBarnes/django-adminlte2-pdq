"""
Base test case for the sidebar menu tests.
"""

# System Imports.

# Third-party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

# Internal Imports.


# Module Variables.
UserModel = get_user_model()


class SidebarMenuBaseTestCase(TestCase):
    """Base test case for testing the Template Tags Sidebar Menu.
    Used as a base for all below test classes.
    """

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
        group_instance = Group.objects.create(name="view_bar")
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

    def _setup_user(self, permissions=None, groups=None):
        """Set up basic user"""

        # Remove user if already exists.
        # Ensures no potential overlap between subtests.
        if self.user:
            self.user.delete()

        # Create basic user.
        self.user = UserModel()
        self.user.username = "test_user"
        self.user.save()

        # Handle if perms provided.
        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.user.user_permissions.add(perm_object)
                self.user.save()

        # Handle if groups provided.
        if groups:
            if isinstance(groups, str):
                groups = [groups]
            for group in groups:
                group_object = Group.objects.filter(
                    name=group,
                ).first()
                self.user.groups.add(group_object)
                self.user.save()

    def _setup_staff_user(self, permissions=None, groups=None):
        """Set up Staff user"""

        # Remove user if already exists.
        # Ensures no potential overlap between subtests.
        if self.staff_user:
            self.staff_user.delete()

        # Create basic staff user.
        self.staff_user = UserModel()
        self.staff_user.username = "test_staff_user"
        self.staff_user.is_staff = True
        self.staff_user.save()

        # Handle if perms provided.
        if permissions:
            if isinstance(permissions, str):
                permissions = [permissions]
            for permission in permissions:
                perm_object = Permission.objects.filter(
                    codename__exact=permission,
                ).first()
                self.staff_user.user_permissions.add(perm_object)
                self.staff_user.save()

        # Handle if groups provided.
        if groups:
            if isinstance(groups, str):
                groups = [groups]
            for group in groups:
                group_object = Group.objects.filter(
                    name=group,
                ).first()
                self.staff_user.groups.add(group_object)
                self.staff_user.save()

    def _setup_super_user(self):
        """Set up Superuser"""

        # Create basic superuser.
        self.super_user = UserModel()
        self.super_user.username = "test_super_user"
        self.super_user.is_superuser = True
        self.super_user.save()

    # endregion Setup
