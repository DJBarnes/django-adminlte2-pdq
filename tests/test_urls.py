"""
Project testing views.
"""

# Third-Party Imports.
from django.urls import include, path

# Internal Imports.
from . import views


app_name = "adminlte2_pdq_tests"
urlpatterns = [
    # General Function Test Views.
    path(
        "function/",
        include(
            [
                path("standard/", views.standard_view, name="function-standard"),
                path(
                    "allow_anonymous_access/",
                    views.allow_anonymous_access_view,
                    name="function-allow-anonymous-access",
                ),
                path(
                    "login/",
                    views.login_required_view,
                    name="function-login-required",
                ),
                path(
                    "allow_without_permissions/",
                    views.allow_without_permissions_view,
                    name="function-allow-without-permissions",
                ),
                path(
                    "one_permission/",
                    views.one_permission_required_view,
                    name="function-one-permission-required",
                ),
                path(
                    "full_permissions/",
                    views.full_permissions_required_view,
                    name="function-full-permissions-required",
                ),
            ]
        ),
    ),
    # "Overlapping" Function Test Views.
    path(
        "function-overlap/",
        include(
            [
                # View with both one_of_permissions and full_permissions defined.
                path(
                    "stacked-permissions-required/",
                    views.stacked_permissions_required_view,
                    name="function-stacked-permissions-required",
                ),
            ]
        ),
    ),
    # General Class Test Views.
    path(
        "class/",
        include(
            [
                path("standard/", views.StandardView.as_view(), name="class-standard"),
                path(
                    "allow_anonymous_access/",
                    views.AllowAnonymousAccessView.as_view(),
                    name="class-allow-anonymous-access",
                ),
                path(
                    "login/",
                    views.LoginRequiredView.as_view(),
                    name="class-login-required",
                ),
                path(
                    "allow_without_permissions/",
                    views.AllowWithoutPermissionsView.as_view(),
                    name="class-allow-without-permissions",
                ),
                path(
                    "one_permission/",
                    views.OnePermissionRequiredView.as_view(),
                    name="class-one-permission-required",
                ),
                path(
                    "full_permissions/",
                    views.FullPermissionsRequiredView.as_view(),
                    name="class-full-permissions-required",
                ),
            ]
        ),
    ),
    # "Bleeding" Edge-Case Class Test Views.
    path(
        "class-bleeding/",
        include(
            [
                # Equivalent to "allow_anonymous_access".
                path(
                    "anonymous-with-permissions/",
                    views.BleedingAnonymousWithPermissionsView.as_view(),
                    name="class-bleeding-anonymous-with-permissions",
                ),
                # Equivalent to "login_required".
                path(
                    "login-with-permissions/",
                    views.BleedingLoginWithPermissionsView.as_view(),
                    name="class-bleeding-login-with-permissions",
                ),
                # Equivalent to "allow_without_permissions".
                path(
                    "conflicting-permissions/",
                    views.BleedingConflictingPermissionsView.as_view(),
                    name="class-bleeding-conflicting-permissions",
                ),
                # Equivalent to "permission_required_one".
                path(
                    "one-permission-missing-permissions/",
                    views.BleedingOnePermissionMissingPermissionsView.as_view(),
                    name="class-bleeding-one-permission-missing-permissions",
                ),
                # Equivalent to "permission_required".
                path(
                    "full-permission-missing-permissions/",
                    views.BleedingFullPermissionMissingPermissionsView.as_view(),
                    name="class-bleeding-full-permission-missing-permissions",
                ),
            ]
        ),
    ),
    # "Overlapping" Class Test Views.
    path(
        "class-overlap/",
        include(
            [
                # View with both one_of_permissions and full_permissions defined.
                path(
                    "stacked-permissions-required/",
                    views.StackedPermissionsRequiredView.as_view(),
                    name="class-stacked-permissions-required",
                ),
            ]
        ),
    ),
]
