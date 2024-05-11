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


class AllowAnonymousAccessMixin:
    """Mixin for strict mode, that defines a view can be accessed without login.

    General logic comes from the login_required project decorator.
    """

    decorator_name = 'allow_anonymous_access'
    login_required = False
    permission_required = None
    permission_required_one = None


class AllowWithoutPermissionsMixin(DjangoLoginRequiredMixin):
    """Mixin for strict mode, that defines a view which requires login, but no permissions.

    General logic comes from the login_required project decorator.
    """

    decorator_name = 'allow_without_permissions'
    login_required = True
    permission_required = None
    permission_required_one = None


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    """Mixin for views that defines login is required."""

    decorator_name = 'login_required'
    login_required = True  # Sets property that Sidebar Node can check.
    permission_required = None
    permission_required_one = None


class PermissionRequiredMixin(DjangoPermissionRequiredMixin):
    """Mixin for views that defines permissions are required."""

    decorator_name = 'permission_required'
    login_required = True
    permission_required = None  # Must have all, same as Django
    permission_required_one = None  # Must have one

    def dispatch(self, request, *args, **kwargs):
        # Override to always redirect to login in event of permission failure.
        # Default behavior is to redirect to login if unauthenticated, and
        # raise forbidden view otherwise.
        if not self.has_permission():
            # Failed permission checks. Redirect to login page.
            return redirect(LOGIN_URL + f'?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

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
        elif isinstance(self.permission_required, list) or isinstance(self.permission_required, tuple):
            perms_all = tuple(self.permission_required)
        else:
            perms_all = tuple()

        # Sanitize permission_required_one.
        if isinstance(self.permission_required_one, str):
            perms_one = (self.permission_required_one,)
        elif isinstance(self.permission_required_one, list) or isinstance(self.permission_required_one, tuple):
            perms_one = tuple(self.permission_required_one)
        else:
            perms_one = tuple()

        return perms_all, perms_one

    def has_permission(self):
        """Check request user matches permission criteria."""

        # Sanitize permission data and update class values.
        perms_all, perms_one = self.get_permission_required()

        # Actually process permissions.
        is_valid = False
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
