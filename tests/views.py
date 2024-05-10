"""
Views for UnitTests.
"""

# System Imports.

# Third-Party Imports.
from django.shortcuts import render
from django.views.generic import TemplateView

# Internal Imports.
from adminlte2_pdq.decorators import (
    allow_anonymous_access,
    allow_without_permissions,
    login_required,
    permission_required,
    permission_required_one,
)
from adminlte2_pdq.mixins import (
    AllowAnonymousAccessMixin,
    # AllowWithoutPermissionsMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
)


# region Function Views


def standard_view(request):
    """Standard testing view. No decorators."""
    return render(request, 'standard_view.html')


@login_required
def login_required_view(request):
    """Testing view with login requirement."""
    return render(request, 'login_required_view.html')


@permission_required_one(['auth.add_foo', 'auth.change_foo'])
def one_permission_required_view(request):
    """Testing view with "one of permissions" requirement."""
    return render(request, 'one_permission_required_view.html')


@permission_required(['auth.add_foo', 'auth.change_foo'])
def full_permissions_required_view(request):
    """Testing view with permission requirement."""
    return render(request, 'full_permissions_required_view.html')


@allow_anonymous_access
def allow_anonymous_access_view(request):
    """Testing view for STRICT mode, allowing full access."""
    return render(request, 'allow_anonymous_access_view.html')


@allow_without_permissions
def allow_without_permissions_view(request):
    """Testing view for STRICT mode, allowing login only requirement."""
    return render(request, 'allow_without_permissions_view.html')


# endregion Function Views

# region Class Views


class StandardView(TemplateView):
    """Standard testing view. No mixins."""

    template_name = "standard_view.html"


class LoginRequiredView(LoginRequiredMixin, TemplateView):
    """Testing view for LOOSE mode, with login requirement."""

    template_name = "login_required_view.html"


class OnePermissionRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    permission_required_one = ['auth.add_foo', 'auth.change_foo']

    template_name = "one_permission_required_view.html"


class FullPermissionsRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    permission_required = ['auth.add_foo', 'auth.change_foo']

    template_name = "full_permissions_required_view.html"


class AllowAnonymousAccessView(AllowAnonymousAccessMixin, TemplateView):
    """Testing view for STRICT mode, allowing full access."""

    template_name = "allow_anonymous_access_view.html"


class AllowWithoutPermissionsView(TemplateView):
    """Testing view for STRICT mode, allowing login only requirement."""

    template_name = "allow_without_permissions_view.html"


# endregion Class Views
