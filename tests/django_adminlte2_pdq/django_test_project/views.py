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
    login_required,
    permission_required,
    permission_required_one,
)
from adminlte2_pdq.mixins import (
    AllowAnonymousAccessMixin,
    AllowWithoutPermissionsMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
)


# region Function Views


def standard_view(request):
    """Standard testing view. No decorators."""
    return render(request, "django_adminlte2_pdq_tests/templates/standard_view.html")


@allow_anonymous_access
def allow_anonymous_access_view(request):
    """Testing view for STRICT mode, allowing full access."""
    return render(request, "django_adminlte2_pdq_tests/templates/allow_anonymous_access_view.html")


@login_required
def login_required_view(request):
    """Testing view with login requirement."""
    return render(request, "django_adminlte2_pdq_tests/templates/login_required_view.html")


@allow_without_permissions
def allow_without_permissions_view(request):
    """Testing view for STRICT mode, allowing login only requirement."""
    return render(request, "django_adminlte2_pdq_tests/templates/allow_without_permissions_view.html")


@permission_required_one(["auth.add_foo", "auth.change_foo"])
def one_permission_required_view(request):
    """Testing view with "one of permissions" requirement."""
    return render(request, "django_adminlte2_pdq_tests/templates/one_permission_required_view.html")


@permission_required_one("auth.add_foo")
def one_permission_required_view_as_string(request):
    """Testing view with "one of permissions" requirement, but defined as a string instead of a list/tuple."""
    return render(request, "django_adminlte2_pdq_tests/templates/one_permission_required_view.html")


@permission_required(["auth.add_foo", "auth.change_foo"])
def full_permissions_required_view(request):
    """Testing view with permission requirement."""
    return render(request, "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html")


@permission_required("auth.add_foo")
def full_permissions_required_view_as_string(request):
    """Testing view with permission requirement, but defined as a string instead of a list/tuple."""
    return render(request, "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html")


# endregion Function Views


# region Function Class Views


@permission_required_one(["auth.view_foo", "auth.delete_foo"])
@permission_required(["auth.add_foo", "auth.change_foo"])
def stacked_permissions_required_view(request):
    """Testing view with both permission attributes set.

    Decorator/mixin logic should stack. So by nature of having one Mixin for
    both attribute options, it means that the user should have
    "all of one set" plus "at last one of the other set".
    """

    return render(request, "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html")


# endregion Function Class Views


# region Class Views


class StandardView(TemplateView):
    """Standard testing view. No mixins."""

    template_name = "django_adminlte2_pdq_tests/templates/standard_view.html"

    def get_context_data(self, **kwargs):
        """Add additional context (variables) for template to display."""

        # Call parent logic.
        context = super().get_context_data(**kwargs)

        # Define custom menu nodes to test "dynamic menu" logic on.
        from .custom_menu_definitions import (
            CUSTOM_MENU_FIRST,
            CUSTOM_MENU_STANDARD,
            CUSTOM_MENU_LAST,
        )

        # Override AdminLte menu with our custom ones.
        context["ADMINLTE2_MENU_FIRST"] = CUSTOM_MENU_FIRST
        context["ADMINLTE2_MENU"] = CUSTOM_MENU_STANDARD
        context["ADMINLTE2_MENU_LAST"] = CUSTOM_MENU_LAST

        # Return updated context.
        return context


class AllowAnonymousAccessView(AllowAnonymousAccessMixin, TemplateView):
    """Testing view for STRICT mode, allowing full access."""

    template_name = "django_adminlte2_pdq_tests/templates/allow_anonymous_access_view.html"


class LoginRequiredView(LoginRequiredMixin, TemplateView):
    """Testing view for LOOSE mode, with login requirement."""

    template_name = "django_adminlte2_pdq_tests/templates/login_required_view.html"


class AllowWithoutPermissionsView(AllowWithoutPermissionsMixin, TemplateView):
    """Testing view for STRICT mode, allowing login only requirement."""

    template_name = "django_adminlte2_pdq_tests/templates/allow_without_permissions_view.html"


class OnePermissionRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    permission_required_one = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/one_permission_required_view.html"


class OnePermissionRequiredViewAsString(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement, but defined as a string instead of a list/tuple."""

    permission_required_one = "auth.add_foo"

    template_name = "django_adminlte2_pdq_tests/templates/one_permission_required_view.html"


class FullPermissionsRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement."""

    permission_required = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html"


class FullPermissionsRequiredViewAsString(PermissionRequiredMixin, TemplateView):
    """Testing view with permission requirement, but defined as a string instead of a list/tuple."""

    permission_required = "auth.add_foo"

    template_name = "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html"


class StrictModeOnePermissionRequiredView(TemplateView):
    """Testing view with permission requirement, but no per mixin. Assumes using Strict Mode."""

    permission_required_one = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/one_permission_required_view.html"


class StrictModeOnePermissionRequiredViewAsString(TemplateView):
    """Testing view with permission requirement as string, but no per mixin. Assumes using Strict Mode."""

    permission_required_one = "auth.add_foo"

    template_name = "django_adminlte2_pdq_tests/templates/one_permission_required_view.html"


class StrictModeFullPermissionsRequiredView(TemplateView):
    """Testing view with permission requirement, but no per mixin. Assumes using Strict Mode."""

    permission_required = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html"


class StrictModeFullPermissionsRequiredViewAsString(TemplateView):
    """Testing view with permission requirement as string, but no per mixin. Assumes using Strict Mode."""

    permission_required = "auth.add_foo"

    template_name = "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html"


# endregion Class Views


# region Bleeding Class Views


class BleedingAnonymousWithPermissionsView(AllowAnonymousAccessMixin, TemplateView):
    """Testing "allow_anonymous_access" mixin bleeding view."""

    permission_required_one = ["auth.add_foo", "auth.change_foo"]
    permission_required = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/allow_anonymous_access_view.html"


class BleedingLoginWithPermissionsView(LoginRequiredMixin, TemplateView):
    """Testing "login_required" mixin bleeding view."""

    permission_required_one = ["auth.add_foo", "auth.change_foo"]
    permission_required = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/login_required_view.html"


class BleedingConflictingPermissionsView(AllowWithoutPermissionsMixin, TemplateView):
    """Testing "allow_without_permissions" mixin bleeding view."""

    permission_required_one = ["auth.add_foo", "auth.change_foo"]
    permission_required = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/allow_without_permissions_view.html"


class BleedingOnePermissionMissingPermissionsView(PermissionRequiredMixin, TemplateView):
    """Testing "permission_required_one" mixin bleeding view."""

    permission_required_one = tuple()

    template_name = "django_adminlte2_pdq_tests/templates/one_permission_required_view.html"


class BleedingFullPermissionMissingPermissionsView(PermissionRequiredMixin, TemplateView):
    """Testing "permission_required" mixin bleeding view."""

    permission_required = tuple()

    template_name = "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html"


# endregion Bleeding Class Views


# region Stacked Class Views


class StackedPermissionsRequiredView(PermissionRequiredMixin, TemplateView):
    """Testing view with both permission attributes set.

    Decorator/mixin logic should stack. So by nature of having one Mixin for
    both attribute options, it means that the user should have
    "all of one set" plus "at last one of the other set".
    """

    # To access view, user should require at least one of these.
    permission_required_one = ["auth.view_foo", "auth.delete_foo"]
    # AND ALSO all of these.
    permission_required = ["auth.add_foo", "auth.change_foo"]

    template_name = "django_adminlte2_pdq_tests/templates/full_permissions_required_view.html"


# endregion Stacked Class Views
