"""Django AdminLTE2 Decorators"""

from functools import wraps
from django.contrib.auth.decorators import (
    login_required as django_login_required,
    permission_required as django_permission_required,
    user_passes_test,
)
from django.core.exceptions import PermissionDenied

from .utlis import debug_print


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

        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms, login_url=login_url)


def login_required(function=None, redirect_field_name='next', login_url=None):
    """Decorator for views that defines that login is required.

    Also adds the login required as a property to that view function.
    The property added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.

    Does NOT do anything if project is in "strict" mode.
    For strict mode, see one of the following decorators:
    * allow_anonymous_access
    * allow_without_permissions
    """

    def decorator(function):

        function.login_required = True

        @wraps(function)
        @django_login_required(redirect_field_name=redirect_field_name, login_url=login_url)
        def wrap(request, *args, **kwargs):

            return function(request, *args, **kwargs)

        return wrap

    if function:
        return decorator(function)
    return decorator


def permission_required(permission, login_url=None, raise_exception=False):
    """Decorator for views that defines a full set of permissions that are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    def decorator(function):

        if isinstance(permission, list) or isinstance(permission, tuple):
            # Is iterable type. Convert to consistent format.
            permissions = tuple(permission)
        elif isinstance(permission, str):
            # Is str type. Assume is a single permission.
            permissions = (permission,)
        else:
            # Is other type. Raise error.
            raise TypeError(f'Unknown type ({type(permission)}) for permission. Expected list, tuple, or string.')

        debug_print('\n\n\n\n')
        debug_print('function: {0}'.format(function))
        debug_print('permissions: {0}'.format(permissions))
        debug_print('\n')

        function.permissions = permissions

        @wraps(function)
        @django_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            debug_print('\n')
            debug_print('and again....')
            debug_print('function: {0}'.format(function))
            debug_print('permissions: {0}'.format(permission))
            debug_print('\n\n\n\n')

            return function(request, *args, **kwargs)

        return wrap

    return decorator


def permission_required_one(permission, login_url=None, raise_exception=False):
    """Decorator for views that defines that only one of the indicated permissions are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    def decorator(function):

        if isinstance(permission, str):
            permissions = (permission,)
        else:
            permissions = permission

        function.one_of_permissions = permissions

        @wraps(function)
        @_one_of_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            return function(request, *args, **kwargs)

        return wrap

    return decorator


def allow_anonymous_access():
    """Decorator for strict mode, that defines a view can be accessed without login.

    Also adds the required logic to render the view on the sidebar template.
    """

    def decorator(function):
        pass

    return decorator


def allow_without_permissions():
    """Decorator for strict mode, that defines a view which requires login, but no permissions.

    Also adds the required logic to render the view on the sidebar template.
    """

    def decorator(function):
        pass

    return decorator
