"""Django Admin LTE 2 View Mixins"""
from django.contrib.auth.mixins import PermissionRequiredMixin as DjangoPermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured


class PermissionRequiredMixin(DjangoPermissionRequiredMixin):
    """Verify that the current user has all or some required permissions."""
    permission_required = None  # Must have all, same as Django
    permission_required_one = None  # Must have one

    def get_permission_required(self):
        """Override this method to override permission attributes.
        Must return a tuple of two iterables: (perms_all, perms_one)"""
        perms_all = []
        perms_one = []

        if self.permission_required is None and self.permission_required_one is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attributes. '
                'Define {0}.permission_required, or {0}.permission_required_one, '
                ' or override {0}.get_permission_required().'.format(
                    self.__class__.__name__
                )
            )
        if isinstance(self.permission_required, str):
            perms_all = (self.permission_required,)
        else:
            perms_all = self.permission_required

        if isinstance(self.permission_required_one, str):
            perms_one = (self.permission_required_one,)
        else:
            perms_one = self.permission_required_one

        return perms_all, perms_one

    def has_permission(self):
        """Check request user has permission"""
        perms_all, perms_one = self.get_permission_required()
        if perms_all and not self.request.user.has_perms(perms_all):
            return False
        if perms_one:
            for perm in perms_one:
                if self.request.user.has_perm(perm):
                    return True
            return False
        return True
