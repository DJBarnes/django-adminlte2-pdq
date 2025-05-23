"""Django AdminLte2Pdq package decorators."""

# System Imports.
from functools import wraps

# Third-Party Imports.
from django.contrib.auth.decorators import (
    login_required as django_login_required,
    permission_required as django_permission_required,
    user_passes_test,
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

# Internal Imports.
from .constants import HOME_ROUTE


# region Utility Functions


def _one_of_permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has at least one particular
    permission enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        if isinstance(perm, str):
            perm_list = (perm,)
        else:
            perm_list = perm

        # Return if the user has any of the permissions in the perm_list
        if any(user.has_perm(perm) for perm in perm_list):
            return True

        # In case the 403 handler should be called raise the exception.
        if raise_exception:
            raise PermissionDenied

        # As the last resort, show the login form.
        return False

    return user_passes_test(check_perms, login_url=login_url)


def _sanitize_permissions(permission):
    """Sanitized permission values based on type."""

    if isinstance(permission, (list, tuple)):
        # Is iterable type. Convert to consistent format.
        permissions = tuple(permission)
    elif isinstance(permission, str):
        # Is str type. Assume is a single permission.
        permissions = (permission,)
    else:
        # Is other type. Raise error.
        raise TypeError(f"Unknown type ({type(permission)}) for permission. Expected list, tuple, or string.")

    return permissions


# endregion Utility Functions


def allow_anonymous_access(function=None):
    """Decorator for strict mode, that defines a view can be accessed without login.

    Also adds the required logic to render the view on the sidebar template.
    """

    admin_pdq_data = {
        "decorator_name": "allow_anonymous_access",
        "allow_anonymous_access": True,
        "login_required": False,
        "allow_without_permissions": False,
    }

    def decorator(function):
        # Save values to view fetch function for middleware handling + potential debugging.
        function.admin_pdq_data = admin_pdq_data

        @wraps(function)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            return function_view

        return wrap

    if function:
        return decorator(function)

    # Save values to view fetch function for middleware handling + potential debugging.
    decorator.decorator_name = "allow_anonymous_access"
    decorator.login_required = False
    decorator.one_of_permissions = None
    decorator.permissions = None

    return decorator


def login_required(function=None, redirect_field_name="next", login_url=None):
    """Decorator for views that defines login is required.

    Also adds the login required as a property to that view function.
    The property added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.

    Does NOT do anything if project is in "strict" mode.
    For strict mode, see one of the following decorators:
    * allow_anonymous_access
    * allow_without_permissions
    """

    admin_pdq_data = {
        "decorator_name": "login_required",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": False,
    }

    def decorator(function):

        # Save values to view fetch function for middleware handling + potential debugging.
        function.admin_pdq_data = admin_pdq_data

        @wraps(function)
        @django_login_required(redirect_field_name=redirect_field_name, login_url=login_url)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            return function_view

        return wrap

    if function:
        return decorator(function)
    return decorator


def allow_without_permissions(function=None, redirect_field_name="next", login_url=None):
    """Decorator for strict mode, that defines a view which requires login, but no permissions.

    Also adds the required logic to render the view on the sidebar template.
    """

    admin_pdq_data = {
        "decorator_name": "allow_without_permissions",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": True,
    }

    def decorator(function):
        # Save values to view fetch function for middleware handling + potential debugging.
        function.admin_pdq_data = admin_pdq_data

        @wraps(function)
        @django_login_required(redirect_field_name=redirect_field_name, login_url=login_url)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            return function_view

        return wrap

    if function:
        return decorator(function)
    return decorator


def permission_required_one(permission, login_url=None, raise_exception=False):
    """Decorator for views that defines that only one of the indicated permissions are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    # Set url if none is provided.
    # Defaults to project "home" page for security.
    if login_url is None:
        login_url = reverse_lazy(HOME_ROUTE)

    # Ensure consistent permission format.
    permissions = _sanitize_permissions(permission)

    admin_pdq_data = {
        "decorator_name": "permission_required",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": False,
    }

    def decorator(function):

        # Save values to view fetch function for middleware handling +  potential debugging.
        function.admin_pdq_data = admin_pdq_data
        function.permission_required_one = permissions  # Must have one, if any.
        function.permission_required = None  # Must have all, if any. Same as Django.

        @wraps(function)
        @_one_of_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            return function_view

        return wrap

    return decorator


def permission_required(permission, login_url=None, raise_exception=False):
    """Decorator for views that defines a full set of permissions that are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    # Set url if none is provided.
    # Defaults to project "home" page for security.
    if login_url is None:
        login_url = reverse_lazy(HOME_ROUTE)

    # Ensure consistent permission format.
    permissions = _sanitize_permissions(permission)

    admin_pdq_data = {
        "decorator_name": "permission_required",
        "allow_anonymous_access": False,
        "login_required": True,
        "allow_without_permissions": False,
    }

    def decorator(function):

        # Save values to view fetch function for middleware handling + potential debugging.
        function.admin_pdq_data = admin_pdq_data
        function.permission_required_one = None  # Must have one, if any.
        function.permission_required = permissions  # Must have all, if any. Same as Django.

        @wraps(function)
        @django_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            return function_view

        return wrap

    return decorator


# Limit imports from this file.
__all__ = [
    "allow_anonymous_access",
    "login_required",
    "allow_without_permissions",
    "permission_required",
    "permission_required_one",
]
