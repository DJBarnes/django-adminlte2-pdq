"""Django AdminLte2Pdq package mixins."""

# Third-Party Imports.
from django.contrib.auth.mixins import (
    LoginRequiredMixin as DjangoLoginRequiredMixin,
    PermissionRequiredMixin as DjangoPermissionRequiredMixin,
)
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Internal Imports.
from .constants import HOME_ROUTE


class AllowAnonymousAccessMixin:
    """Mixin for strict mode, that defines a view can be accessed without login.

    General logic comes from the login_required project decorator.
    """

    # Pdq data processing dict.
    admin_pdq_data = {
        "decorator_name": "allow_anonymous_access",
        "allow_anonymous_access": True,
        "login_required": False,
        "allow_without_permissions": False,
    }

    subclasses = []

    def __init_subclass__(cls, **kwargs):
        """Hook to record all classes that inherit this mixin.

        Solution from: https://stackoverflow.com/a/50099920
        """
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls.__name__)


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    """Mixin for views that defines login is required."""

    # Pdq data processing dict.
    admin_pdq_data = {
        "decorator_name": "login_required",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": False,
    }

    subclasses = []

    def __init_subclass__(cls, **kwargs):
        """Hook to record all classes that inherit this mixin.

        Solution from: https://stackoverflow.com/a/50099920
        """
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls.__name__)


class AllowWithoutPermissionsMixin(DjangoLoginRequiredMixin):
    """Mixin for strict mode, that defines a view which requires login, but no permissions.

    General logic comes from the login_required project decorator.
    """

    # Pdq data processing dict.
    admin_pdq_data = {
        "decorator_name": "allow_without_permissions",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": True,
    }

    subclasses = []

    def __init_subclass__(cls, **kwargs):
        """Hook to record all classes that inherit this mixin.

        Solution from: https://stackoverflow.com/a/50099920
        """
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls.__name__)


class PermissionRequiredMixin(DjangoPermissionRequiredMixin):
    """Mixin for views that defines permissions are required."""

    # Values for user to override.
    permission_required_one = None  # Must have one, if any.
    permission_required = None  # Must have all, if any. Same as Django.

    # Pdq data processing dict.
    admin_pdq_data = {
        "decorator_name": "permission_required",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": False,
    }

    subclasses = []

    def __init_subclass__(cls, **kwargs):
        """Hook to record all classes that inherit this mixin.

        Solution from: https://stackoverflow.com/a/50099920
        """
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls.__name__)

    def dispatch(self, request, *args, **kwargs):
        # Override to always redirect to home in event of permission failure.
        # Default behavior is to redirect to login if unauthenticated, and
        # raise forbidden view otherwise.
        if not self.has_permission():
            # Failed permission checks. Redirect user.
            # Defaults to project "home" page for security.
            return redirect(reverse_lazy(HOME_ROUTE))
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        """Check request user matches permission criteria."""

        # Sanitize permission data and update class values.
        perms_all, perms_one = self.get_permission_required()

        # Instantly fail if not at least one defined.
        if not (perms_all or perms_one):
            return False

        # Otherwise, at least one is defined.
        # Default to the opposite of starting point.
        # That way if either is None, it's automatically passing.
        # Otherwise it needs to pass checks.
        passes_perms_one = not bool(perms_one)
        passes_perms_all = not bool(perms_all)

        if perms_one:
            # View is "one of permissions" format. Return on first found one.
            for perm in perms_one:
                if self.request.user.has_perm(perm):
                    passes_perms_one = True

        # Actually process permissions.
        if perms_all and self.request.user.has_perms(perms_all):
            # User has all permissions and view is "all permissions" format.
            passes_perms_all = True

        # Return combination of both checks. Must pass both to pass.
        return passes_perms_one and passes_perms_all

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

        # Set some defaults
        unknown_perms_one_type = False
        unknown_perms_all_type = False

        # Sanitize permission_required.
        if isinstance(self.permission_required, str):
            perms_all = (self.permission_required,)
        elif isinstance(self.permission_required, (list, tuple)):
            perms_all = tuple(self.permission_required)
        else:
            # Need to allow "other" in case user is provided permission_required_one.
            perms_all = tuple()
            unknown_perms_all_type = self.permission_required is not None

        # Sanitize permission_required_one.
        if isinstance(self.permission_required_one, str):
            perms_one = (self.permission_required_one,)
        elif isinstance(self.permission_required_one, (list, tuple)):
            perms_one = tuple(self.permission_required_one)
        else:
            # Need to allow "other" in case user is provided permission_required.
            perms_one = tuple()
            unknown_perms_one_type = self.permission_required_one is not None

        # If neither of the perms are set correctly, raise error
        if unknown_perms_all_type or unknown_perms_one_type:
            incorrect_type = self.permission_required or self.permission_required_one
            # Is other type. Raise error.
            raise TypeError(f"Unknown type ({type(incorrect_type)}) for permission. Expected list, tuple, or string.")

        return perms_all, perms_one


# Limit imports from this file.
__all__ = [
    "AllowAnonymousAccessMixin",
    "AllowWithoutPermissionsMixin",
    "LoginRequiredMixin",
    "PermissionRequiredMixin",
]
