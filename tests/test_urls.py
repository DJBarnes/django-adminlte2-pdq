"""
Project testing views.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from . import views


app_name = 'adminlte2_pdq_tests'
urlpatterns = [
    # Function Test Views.
    path('function/standard/', views.standard_view, name="function-standard"),
    path('function/login/', views.login_required_view, name="function-login-required"),
    path('function/one_permission/', views.one_permission_required_view, name="function-one-permission-required"),
    path('function/full_permissions/', views.full_permissions_required_view, name="function-full-permissions-required"),
    path('class/allow_anonymous_access/', views.allow_anonymous_access_view, name="function-allow-anonymous-access"),
    path(
        'class/allow_without_permissions/',
        views.allow_without_permissions_view,
        name="function-allow-without-permissions",
    ),
    # Class Test Views.
    path('class/standard/', views.StandardView.as_view(), name="class-standard"),
    path('class/login/', views.LoginRequiredView.as_view(), name="class-login-required"),
    path('class/one_permission/', views.OnePermissionRequiredView.as_view(), name="class-one-permission-required"),
    path(
        'class/full_permissions/',
        views.FullPermissionsRequiredView.as_view(),
        name="class-full-permissions-required",
    ),
    path(
        'class/allow_anonymous_access/',
        views.AllowAnonymousAccessView.as_view(),
        name="class-allow-anonymous-access",
    ),
    path(
        'class/allow_without_permissions/',
        views.AllowWithoutPermissionsView.as_view(),
        name="class-allow-without-permissions",
    ),
    path(
        'class/bleeding/login-with-permissions/',
        views.BleedingLoginWithPermissionsView.as_view(),
        name="class-bleeding-login-with-permissions",
    ),
    path(
        'class/bleeding/anonymous-with-permissions/',
        views.BleedingAnonymousWithPermissionsView.as_view(),
        name="class-bleeding-anonymous-with-permissions",
    ),
    path(
        'class/bleeding/conflicting-permissions/',
        views.BleedingConflictingPermissionsView.as_view(),
        name="class-bleeding-conflicting-permissions",
    ),
    path(
        'class/bleeding/one-permission-missing-permissions/',
        views.BleedingOnePermissionMissingPermissionsView.as_view(),
        name="class-bleeding-one-permission-missing-permissions",
    ),
    path(
        'class/bleeding/full-permission-missing-permissions/',
        views.BleedingFullPermissionMissingPermissionsView.as_view(),
        name="class-bleeding-full-permission-missing-permissions",
    ),
]
