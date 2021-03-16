"""Django AdminLTE2 Decorators"""
from functools import wraps
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.core.exceptions import PermissionDenied


def _one_of_permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has at least one particular
    permission enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(perm, str):
            perm_list = (perm, )
        else:
            perm_list = perm

        # Return if the user has any of the permissions in the perm_list
        if any(user.has_perm(perm) for perm in perm_list):
            return True

        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)


def requires_all_permissions(permission, login_url=None, raise_exception=False):
    """
    Decorator for views that defines what permissions are required, and also
    adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function
    """
    def decorator(function):

        if isinstance(permission, str):
            permissions = (permission, )
        else:
            permissions = permission

        function.permissions = permissions

        @wraps(function)
        @permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            return function(request, *args, **kwargs)
        return wrap
    return decorator


def requires_one_permission(permission, login_url=None, raise_exception=False):
    """
    Decorator for views that defines that one of the permissions are required,
    and also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function
    """
    def decorator(function):

        if isinstance(permission, str):
            permissions = (permission, )
        else:
            permissions = permission

        function.one_of_permissions = permissions

        @wraps(function)
        @_one_of_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            return function(request, *args, **kwargs)
        return wrap
    return decorator
