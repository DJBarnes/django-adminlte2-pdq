"""Django AdminLte2Pdq package decorators."""

# System Imports.
from functools import wraps

# Third-Party Imports.
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy

# Internal Imports.
from .constants import HOME_ROUTE, LOGIN_URL, USE_LOGIN_NEXT


# region Utility Functions


def _user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """Django's user_passes_test, except that the redirect has no "next" when ADMINLTE2_USE_LOGIN_NEXT is False.

    The setting is read when the view is called, not when it is decorated.
    """

    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            field_name = redirect_field_name if USE_LOGIN_NEXT else None
            check = user_passes_test(test_func, login_url=login_url, redirect_field_name=field_name)
            return check(function)(request, *args, **kwargs)

        return wrap

    return decorator


def _permissions_required(check_perms, login_url, raise_exception):
    """Decorator for views that checks the user's permissions with check_perms(user).

    A user who fails the check is handled as by the middleware: an anonymous user goes to the login page, with the
    requested url as "next" unless ADMINLTE2_USE_LOGIN_NEXT is False, since they may have the permissions once logged
    in. A logged-in user goes to login_url, without "next". With raise_exception, both get PermissionDenied instead.
    """

    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if check_perms(request.user):
                return function(request, *args, **kwargs)
            if raise_exception:
                raise PermissionDenied
            if not request.user.is_authenticated:
                redirect_field_name = REDIRECT_FIELD_NAME if USE_LOGIN_NEXT else None
                return redirect_to_login(request.get_full_path(), LOGIN_URL, redirect_field_name)
            return redirect(login_url)

        return wrap

    return decorator


def _one_of_permission_required(perm, login_url, raise_exception=False):
    """Decorator for views that checks whether a user has at least one of the permissions."""
    perm_list = (perm,) if isinstance(perm, str) else perm
    return _permissions_required(
        lambda user: any(user.has_perm(one_perm) for one_perm in perm_list), login_url, raise_exception
    )


def _all_permissions_required(perm, login_url, raise_exception=False):
    """Decorator for views that checks whether a user has all of the permissions. Same as Django's
    permission_required decorator, except for where a user without them is redirected."""
    perm_list = (perm,) if isinstance(perm, str) else perm
    return _permissions_required(lambda user: user.has_perms(perm_list), login_url, raise_exception)


def _is_authenticated(user):
    """The test for the login_required and allow_without_permissions decorators."""
    return user.is_authenticated


def _sanitize_permissions(permission):
    """Sanitized permission values based on type."""

    if isinstance(permission, str):
        # Is str type. Assume is a single permission.
        permissions = (permission,)
    elif isinstance(permission, (list, tuple)):
        # Is iterable type. Convert to consistent format.
        permissions = tuple(permission)
    else:
        # Is other type. Raise error.
        raise TypeError(f"Unknown type ({type(permission)}) for permission. Expected list, tuple, or string.")

    return permissions


def _record_permissions(function, one_of_permissions=None, full_permissions=None):
    """Record a permission decorator's permissions on the view function, for the middleware and the sidebar.

    Permission decorators can be stacked, and the view requires all of their permissions. So each one adds to the
    permissions recorded by the decorators below it. Two permission_required_one decorators can't be recorded as one
    "one of" list, so they raise ImproperlyConfigured. Use one permission_required_one with a single list instead.
    """
    recorded_one_of = getattr(function, "permission_required_one", None)
    recorded_full = getattr(function, "permission_required", None)

    if one_of_permissions and recorded_one_of:
        raise ImproperlyConfigured(
            f"The view '{function.__qualname__}' has more than one permission_required_one decorator. "
            "Use a single permission_required_one decorator with all of the permissions."
        )

    # Must have one, if any.
    function.permission_required_one = one_of_permissions or recorded_one_of
    # Must have all, if any. Same as Django.
    combined_full = tuple(dict.fromkeys((recorded_full or ()) + (full_permissions or ())))
    function.permission_required = combined_full or None


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

    return decorator(function) if function else decorator


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
        @_user_passes_test(_is_authenticated, login_url=login_url, redirect_field_name=redirect_field_name)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            return function_view

        return wrap

    return decorator(function) if function else decorator


def allow_without_permissions(function=None, redirect_field_name="next", login_url=None):
    """Decorator for strict mode, that defines a view which requires login, but no permissions.

    A view that is also in a login whitelist doesn't require login, so anyone can access it.
    The middleware tells the view whether it is login whitelisted.

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

        login_required_function = _user_passes_test(
            _is_authenticated, login_url=login_url, redirect_field_name=redirect_field_name
        )(function)

        @wraps(function)
        def wrap(request, *args, **kwargs):

            # Skip the login check for login whitelisted views.
            if getattr(request, "admin_pdq_login_whitelisted", False):
                return function(request, *args, **kwargs)

            # Get our view response object.
            function_view = login_required_function(request, *args, **kwargs)

            return function_view

        return wrap

    return decorator(function) if function else decorator


def permission_required_one(permission, login_url=None, raise_exception=False):
    """Decorator for views that defines that only one of the indicated permissions are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    # Set url if none is provided.
    # Defaults to project "home" page for security.
    login_url = login_url or reverse_lazy(HOME_ROUTE)

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
        _record_permissions(function, one_of_permissions=permissions)

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
    login_url = login_url or reverse_lazy(HOME_ROUTE)

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
        _record_permissions(function, full_permissions=permissions)

        @wraps(function)
        @_all_permissions_required(permission, login_url, raise_exception)
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
