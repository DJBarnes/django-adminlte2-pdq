"""Django AdminLte2Pdq package mixins."""

# Third-Party Imports.
from django.contrib.auth.mixins import (
    LoginRequiredMixin as DjangoLoginRequiredMixin,
    PermissionRequiredMixin as DjangoPermissionRequiredMixin,
)
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect

# Internal Imports.
from .constants import LOGIN_URL
from .decorators import _has_group


class AllowAnonymousAccessMixin:
    """Mixin for strict mode, that defines a view can be accessed without login.

    General logic comes from the login_required project decorator.
    """

    # Pdq data processing dict.
    admin_pdq_data = {
        'decorator_name': 'allow_anonymous_access',
        'login_required': False,
        'one_of_permissions': None,
        'full_permissions': None,
        'one_of_groups': None,
        'full_groups': None,
    }


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    """Mixin for views that defines login is required."""

    # Pdq data processing dict.
    admin_pdq_data = {
        'decorator_name': 'login_required',
        'login_required': True,  # Sets property that Sidebar Node can check.
        'one_of_permissions': None,
        'full_permissions': None,
        'one_of_groups': None,
        'full_groups': None,
    }


class AllowWithoutPermissionsMixin(DjangoLoginRequiredMixin):
    """Mixin for strict mode, that defines a view which requires login, but no permissions.

    General logic comes from the login_required project decorator.
    """

    # Pdq data processing dict.
    admin_pdq_data = {
        'decorator_name': 'allow_without_permissions',
        'login_required': True,
        'one_of_permissions': None,
        'full_permissions': None,
        'one_of_groups': None,
        'full_groups': None,
    }


class PermissionRequiredMixin(DjangoPermissionRequiredMixin):
    """Mixin for views that defines permissions are required."""

    # Values for user to override.
    permission_required_one = None  # Must have one, if any.
    permission_required = None  # Must have all, if any. Same as Django.

    # Pdq data processing dict.
    admin_pdq_data = {
        'decorator_name': 'permission_required',
        'login_required': True,
        'one_of_permissions': permission_required_one,
        'full_permissions': permission_required,
        'one_of_groups': None,
        'full_groups': None,
    }

    def dispatch(self, request, *args, **kwargs):
        # Override to always redirect to login in event of permission failure.
        # Default behavior is to redirect to login if unauthenticated, and
        # raise forbidden view otherwise.
        if not self.has_permission():
            # Failed permission checks. Redirect to login page.
            return redirect(LOGIN_URL + f'?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        """Check request user matches permission criteria."""

        # Sanitize permission data and update class values.
        perms_all, perms_one = self.get_permission_required()

        # Actually process permissions.
        if perms_all and self.request.user.has_perms(perms_all):
            # User has all permissions and view is "all permissions" format.
            return True

        if perms_one:
            # View is "one of permissions" format. Return on first found one.
            for perm in perms_one:
                if self.request.user.has_perm(perm):
                    return True

        # If we made it this far, then all permission checks failed.
        return False

    def get_permission_required(self):
        """Override this method to override permission attributes.
        Must return a tuple of two iterables: (perms_all, perms_one)
        """

        # Raise error if neither of expected attributes defined.
        if self.permission_required is None and self.permission_required_one is None:
            error_message = (
                "{class_name} uses the PermissionRequiredMixin mixin but is missing permission "
                "permission attributes. To fix this, define either the "
                "{class_name}.permission_required or "
                "{class_name}.permission_required_one attributes. Or override "
                "{class_name}.get_permission_required() to change how the mixin functions."
            ).format(
                class_name=self.__class__.__name__,
            )
            raise ImproperlyConfigured(error_message)

        # Sanitize permission_required.
        if isinstance(self.permission_required, str):
            perms_all = (self.permission_required,)
        elif isinstance(self.permission_required, (list, tuple)):
            perms_all = tuple(self.permission_required)
        else:
            # Need to allow "other" in case user is provided permission_required_one.
            perms_all = tuple()

        # Sanitize permission_required_one.
        if isinstance(self.permission_required_one, str):
            perms_one = (self.permission_required_one,)
        elif isinstance(self.permission_required_one, (list, tuple)):
            perms_one = tuple(self.permission_required_one)
        else:
            # Need to allow "other" in case user is provided permission_required.
            perms_one = tuple()

        return perms_all, perms_one


class GroupRequiredMixin(DjangoPermissionRequiredMixin):
    """Mixin for views that defines groups are required."""

    # Values for user to override.
    group_required_one = None  # Must have one, if any.
    group_required = None  # Must have all, if any. Same as Django.

    # Pdq data processing dict.
    admin_pdq_data = {
        'decorator_name': 'group_required',
        'login_required': True,
        'one_of_permissions': None,
        'full_permissions': None,
        'one_of_groups': group_required_one,
        'full_groups': group_required,
    }

    def __init__(self, *args, **kwargs):

        # Call parent logic.
        super().__init__(*args, **kwargs)

        # Override default Django message.
        self.permission_denied_message = (
            "{class_name} uses the GroupRequiredMixin mixin but is missing group "
            "definition attributes. To fix this, define either the "
            "{class_name}.group_required or "
            "{class_name}.group_required_one attributes. Or override "
            "{class_name}.get_group_required() to change how the mixin functions."
        ).format(
            class_name=self.__class__.__name__,
        )

    def dispatch(self, request, *args, **kwargs):
        # Override to always redirect to login in event of group failure.
        # Default behavior is to redirect to login if unauthenticated, and
        # raise forbidden view otherwise.
        if not self.has_group():
            # Failed group checks. Redirect to login page.
            return redirect(LOGIN_URL + f'?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

    def has_group(self):
        """Check request user matches group criteria."""

        # Sanitize group data and update class values.
        groups_all, groups_one = self.get_group_required()

        print('groups_all: {0}'.format(groups_all))
        print('groups_one: {0}'.format(groups_one))

        # Actually process groups.
        if groups_all and _has_group(self.request.user, groups_all, require='All'):
            # User has all groups and view is "all groups" format.
            return True

        if groups_one and _has_group(self.request.user, groups_one, require='Any'):
            # View is "one of groups" format. Return on first found one.
            return True

        # If we made it this far, then all group checks failed.
        return False

    def get_group_required(self):
        """Override this method to override group attributes.
        Must return a tuple of two iterables: (perms_all, perms_one)
        """

        # Raise error if neither of expected attributes defined.
        if self.group_required is None and self.group_required_one is None:
            raise ImproperlyConfigured(self.permission_denied_message)

        print('self.group_required: {0}'.format(self.group_required))
        print('self.group_required_one: {0}'.format(self.group_required_one))

        # Sanitize group_required.
        if isinstance(self.group_required, str):
            groups_all = (self.group_required,)
        elif isinstance(self.group_required, (list, tuple)):
            groups_all = tuple(self.group_required)
        else:
            # Need to allow "other" in case user is provided group_required_one.
            groups_all = tuple()

        # Sanitize group_required_one.
        if isinstance(self.group_required_one, str):
            groups_one = (self.group_required_one,)
        elif isinstance(self.group_required_one, (list, tuple)):
            groups_one = tuple(self.group_required_one)
        else:
            # Need to allow "other" in case user is provided group_required.
            groups_one = tuple()

        print('groups_all: {0}'.format(groups_all))
        print('groups_one: {0}'.format(groups_one))

        return groups_all, groups_one

    def has_permission(self):
        """Override default Mixin logic to use Group logic."""
        return self.has_group()

    def get_permission_required(self):
        """Override default Mixin logic to use Group logic."""
        try:
            self.get_group_required()
        except ImproperlyConfigured:
            raise ImproperlyConfigured(self.permission_denied_message)


# Limit imports from this file.
__all__ = [
    'AllowAnonymousAccessMixin',
    'AllowWithoutPermissionsMixin',
    'LoginRequiredMixin',
    'PermissionRequiredMixin',
    'GroupRequiredMixin',
]
