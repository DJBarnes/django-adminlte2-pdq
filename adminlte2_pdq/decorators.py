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
from django.utils.itercompat import is_iterable

# Internal Imports.
from .utlis import debug_print


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


def _group_required(group, login_url=None, raise_exception=False, require_all=True):
    """
    Decorator for views that checks whether a user has at least one particular
    permission enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_groups(user):
        if isinstance(group, str):
            expected_group_list = (group,)
        elif not is_iterable(group):
            raise ValueError("group_list must be an iterable of groups.")
        else:
            expected_group_list = tuple(group)

        # Check that authenticated.
        if not user.is_active or not user.is_authenticated:
            return PermissionDenied

        if require_all:
            # Require all groups provided.
            if _has_group(user, expected_group_list, require='All'):
                # User pass check and had all required groups.
                return True

        else:
            # Require at least one of groups provided.
            if _has_group(user, expected_group_list, require='Any'):
                # User passed check and had at least one group.
                return True

        # If we made it this far, user failed checks.
        # In case the 403 handler should be called raise the exception.
        if raise_exception:
            raise PermissionDenied

        # As the last resort, show the login form.
        return False

    return user_passes_test(check_groups, login_url=login_url)


def _has_group(user, expected_group_list, require=None):
    """Verifies user matches expected groups in list."""

    required_arg_error = 'The "require" arg must be one of [any, all].'

    # Sanitize "require" value.
    if require not in ['Any', 'All']:
        raise ValueError(required_arg_error)

    # Return True for any users with superuser status.
    if user.is_active and user.is_superuser:
        return True

    # Get all groups user is in.
    user_group_list = user.groups.all().values_list('name', flat=True)

    print('\n\n\n\n')
    print('expected_group_list: {0}'.format(expected_group_list))
    print('user_group_list: {0}'.format(user_group_list))
    print('require: {0}'.format(require))
    print('has all: {0}'.format(all(expected_group in user_group_list for expected_group in expected_group_list)))
    print('has any: {0}'.format(any(expected_group in user_group_list for expected_group in expected_group_list)))
    print('\n\n\n\n')

    # Check if user has group, based on mode.
    if require == 'All':
        # Check if user has all expected groups.
        return all(expected_group in user_group_list for expected_group in expected_group_list)
    elif require == 'Any':
        # Check if user has at least one of expected groups.
        return any(expected_group in user_group_list for expected_group in expected_group_list)
    else:
        raise ValueError(required_arg_error)


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
        raise TypeError(f'Unknown type ({type(permission)}) for permission. Expected list, tuple, or string.')

    return permissions


# endregion Utility Functions


def allow_anonymous_access(function=None):
    """Decorator for strict mode, that defines a view can be accessed without login.

    Also adds the required logic to render the view on the sidebar template.
    """

    def decorator(function):
        # Save values to view fetch function for middleware handling + potential debugging.
        function.decorator_name = 'allow_anonymous_access'
        function.login_required = False
        function.one_of_permissions = None
        function.permissions = None

        @wraps(function)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'allow_anonymous_access'
            function_view.login_required = False
            function_view.one_of_permissions = None
            function_view.permissions = None

            return function_view

        return wrap

    if function:
        return decorator(function)

    # Save values to view fetch function for middleware handling + potential debugging.
    decorator.decorator_name = 'allow_anonymous_access'
    decorator.login_required = False
    decorator.one_of_permissions = None
    decorator.permissions = None

    return decorator


def login_required(function=None, redirect_field_name='next', login_url=None):
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

    def decorator(function):

        # Save values to view fetch function for middleware handling + potential debugging.
        function.decorator_name = 'login_required'
        function.login_required = True
        function.one_of_permissions = None
        function.permissions = None

        @wraps(function)
        @django_login_required(redirect_field_name=redirect_field_name, login_url=login_url)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'login_required'
            function_view.login_required = True
            function_view.one_of_permissions = None
            function_view.permissions = None

            return function_view

        return wrap

    if function:
        return decorator(function)
    return decorator


def allow_without_permissions(function=None, redirect_field_name='next', login_url=None):
    """Decorator for strict mode, that defines a view which requires login, but no permissions.

    Also adds the required logic to render the view on the sidebar template.
    """

    def decorator(function):
        # Save values to view fetch function for middleware handling + potential debugging.
        function.decorator_name = 'allow_without_permissions'
        function.login_required = True
        function.one_of_permissions = None
        function.permissions = None

        @wraps(function)
        @django_login_required(redirect_field_name=redirect_field_name, login_url=login_url)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'allow_without_permissions'
            function_view.login_required = True
            function_view.one_of_permissions = None
            function_view.permissions = None

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

    # Ensure consistent permission format.
    permissions = _sanitize_permissions(permission)

    def decorator(function):

        # Save values to view fetch function for middleware handling +  potential debugging.
        function.decorator_name = 'permission_required_one'
        function.login_required = True
        function.one_of_permissions = permissions
        function.permissions = None

        @wraps(function)
        @_one_of_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'permission_required_one'
            function_view.login_required = True
            function_view.one_of_permissions = permissions
            function_view.permissions = None

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

    # Ensure consistent permission format.
    permissions = _sanitize_permissions(permission)

    def decorator(function):

        debug_print('\n\n\n\n')
        debug_print('function: {0}'.format(function))
        debug_print('permissions: {0}'.format(permissions))
        debug_print('\n')

        # Save values to view fetch function for middleware handling + potential debugging.
        function.decorator_name = 'permission_required'
        function.login_required = True
        function.one_of_permissions = None
        function.permissions = permissions

        @wraps(function)
        @django_permission_required(permission, login_url, raise_exception)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'permission_required'
            function_view.login_required = True
            function_view.one_of_permissions = None
            function_view.permissions = permissions

            return function_view

        wrapped_function = wrap
        wrapped_function.permissions = permissions
        return wrapped_function

    return decorator


def group_required_one(group, login_url=None, raise_exception=False):
    """Decorator for views that defines that only one of the indicated permissions are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    # Ensure consistent permission format.
    groups = _sanitize_permissions(group)

    def decorator(function):

        # Save values to view fetch function for middleware handling +  potential debugging.
        function.decorator_name = 'group_required_one'
        function.login_required = True
        function.one_of_permissions = None
        function.permissions = None
        function.one_of_groups = groups
        function.groups = None

        @wraps(function)
        @_group_required(group, login_url=login_url, raise_exception=raise_exception, require_all=False)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'group_required_one'
            function_view.login_required = True
            function_view.one_of_permissions = None
            function_view.permissions = None
            function_view.one_of_groups = groups
            function_view.groups = None

            return function_view

        return wrap

    return decorator


def group_required(group, login_url=None, raise_exception=False):
    """Decorator for views that defines that only one of the indicated permissions are required.

    Also adds the required permissions as a property to that view function.
    The permissions added to the view function can then be used by the sidebar
    template to know whether to render the sidebar menu item that links to that
    view function.
    """

    # Ensure consistent permission format.
    groups = _sanitize_permissions(group)

    def decorator(function):

        # Save values to view fetch function for middleware handling +  potential debugging.
        function.decorator_name = 'group_required'
        function.login_required = True
        function.one_of_permissions = None
        function.permissions = None
        function.one_of_groups = None
        function.groups = groups

        @wraps(function)
        @_group_required(group, login_url=login_url, raise_exception=raise_exception, require_all=True)
        def wrap(request, *args, **kwargs):

            # Get our view response object.
            function_view = function(request, *args, **kwargs)

            # Save values to fully qualified view for middleware handling +  potential debugging.
            function_view.decorator_name = 'group_required'
            function_view.login_required = True
            function_view.one_of_permissions = None
            function_view.permissions = None
            function_view.one_of_groups = None
            function_view.groups = groups

            return function_view

        return wrap

    return decorator


# Limit imports from this file.
__all__ = [
    'allow_anonymous_access',
    'login_required',
    'allow_without_permissions',
    'permission_required',
    'permission_required_one',
    'group_required_one',
    'group_required',
]
