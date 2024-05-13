"""
Views for UnitTests.
"""

# Third-Party Imports.
from django.shortcuts import render
from django.views.generic import TemplateView

# Internal Imports.
from adminlte2_pdq.decorators import (
    allow_anonymous_access,
    allow_without_permissions,
    group_required_one,
    group_required,
    login_required,
    permission_required,
    permission_required_one,
)
from adminlte2_pdq.mixins import (
    AllowAnonymousAccessMixin,
    AllowWithoutPermissionsMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    GroupRequiredMixin,
)


# region Function Views


def standard_view(request):
    """Standard testing view. No decorators."""
    return render(request, 'standard_view.html')


@allow_anonymous_access
def allow_anonymous_access_view(request):
    """Testing view for STRICT mode, allowing full access."""
    return render(request, 'allow_anonymous_access_view.html')


@login_required
def login_required_view(request):
    """Testing view with login requirement."""
    return render(request, 'login_required_view.html')


@allow_without_permissions
def allow_without_permissions_view(request):
    """Testing view for STRICT mode, allowing login only requirement."""
    return render(request, 'allow_without_permissions_view.html')


@permission_required_one(['auth.add_foo', 'auth.change_foo'])
def one_permission_required_view(request):
    """Testing view with "one of permissions" requirement."""
    return render(request, 'one_permission_required_view.html')


@permission_required(['auth.add_foo', 'auth.change_foo'])
def full_permissions_required_view(request):
    """Testing view with permission requirement."""
    return render(request, 'full_permissions_required_view.html')


@group_required_one(['add_bar', 'change_bar'])
def one_group_required_view(request):
    """Testing view with "one of groups" requirement."""
    return render(request, 'one_group_required_view.html')


@group_required(['add_bar', 'change_bar'])
def full_groups_required_view(request):
    """Testing view with group requirement."""
    return render(request, 'full_groups_required_view.html')


# endregion Function Views


# region Class Views


class StandardView(TemplateView):
    """Standard testing view. No mixins."""

    template_name = "standard_view.html"


class AllowAnonymousAccessView(AllowAnonymousAccessMixin, TemplateView):
    """Testing view for STRICT mode, allowing full access."""

    template_name = "allow_anonymous_access_view.html"


class LoginRequiredView(LoginRequiredMixin, TemplateView):
    """Testing view for LOOSE mode, with login requirement."""

    template_name = "login_required_view.html"


class AllowWithoutPermissionsView(AllowWithoutPermissionsMixin, TemplateView):
    """Testing view for STRICT mode, allowing login only requirement."""

    template_name = "allow_without_permissions_view.html"


class OnePermissionRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    permission_required_one = ['auth.add_foo', 'auth.change_foo']

    template_name = "one_permission_required_view.html"


class FullPermissionsRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    permission_required = ['auth.add_foo', 'auth.change_foo']

    template_name = "full_permissions_required_view.html"


class OneGroupRequiredView(GroupRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    group_required_one = ['add_bar', 'change_bar']

    template_name = "one_group_required_view.html"


class FullGroupsRequiredView(GroupRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    group_required = ['add_bar', 'change_bar']

    template_name = "full_groups_required_view.html"


# endregion Class Views


# region Bleeding Class Views


class BleedingAnonymousWithPermissionsView(AllowAnonymousAccessMixin, TemplateView):
    """Testing "allow_anonymous_access" mixin bleeding view."""

    permission_required_one = ['auth.add_foo', 'auth.change_foo']
    permission_required = ['auth.add_foo', 'auth.change_foo']

    template_name = "allow_anonymous_access_view.html"


class BleedingLoginWithPermissionsView(LoginRequiredMixin, TemplateView):
    """Testing "login_required" mixin bleeding view."""

    permission_required_one = ['auth.add_foo', 'auth.change_foo']
    permission_required = ['auth.add_foo', 'auth.change_foo']

    template_name = "login_required_view.html"


class BleedingConflictingPermissionsView(AllowWithoutPermissionsMixin, TemplateView):
    """Testing "allow_without_permissions" mixin bleeding view."""

    permission_required_one = ['auth.add_foo', 'auth.change_foo']
    permission_required = ['auth.add_foo', 'auth.change_foo']

    template_name = "allow_without_permissions_view.html"


class BleedingOnePermissionMissingPermissionsView(PermissionRequiredMixin, TemplateView):
    """Testing "permission_required_one" mixin bleeding view."""

    permission_required_one = tuple()

    template_name = "one_permission_required_view.html"


class BleedingFullPermissionMissingPermissionsView(PermissionRequiredMixin, TemplateView):
    """Testing "permission_required" mixin bleeding view."""

    permission_required = tuple()

    template_name = "full_permissions_required_view.html"


# endregion Bleeding Class Views


# region Stacked Class Views


class StackedPermissionRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with both permission attributes set.

    By nature of having one Mixin for both attribute options, it implicitly means
    that they should be able to stack and do an either-or scenario.
    """

    # To access view, user should require at least one of these.
    permission_required_one = ['auth.add_foo', 'auth.change_foo']
    # Or else ALL of these.
    permission_required = ['auth.view_foo', 'auth.delete_foo']

    template_name = "full_permissions_required_view.html"


# endregion Stacked Class Views
