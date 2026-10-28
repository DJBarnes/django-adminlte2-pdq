"""System checks for Django AdminLTE2 PDQ. They run with manage.py check, runserver, migrate, and tests."""

# Third-Party Imports.
from django.conf import settings
from django.core.checks import Warning as CheckWarning, register
from django.urls import URLPattern, URLResolver, get_resolver
from django.urls.resolvers import ResolverMatch


AUTH_MIDDLEWARE = "adminlte2_pdq.middleware.AuthMiddleware"


def _route_text(pattern):
    """The text of a URL pattern's route, without regex anchors."""
    route = str(pattern)
    if route.startswith("^"):
        route = route[1:]
    if route.endswith("$"):
        route = route[:-1]
    return route


def _resolved_patterns(patterns, prefix="", app_names=(), namespaces=()):
    """Yield (path, ResolverMatch) for every view in a URL configuration.

    The path is built from the route text, so routes with converters keep them as text,
    for example "/books/<int:pk>/".
    """
    for pattern in patterns:
        route = prefix + _route_text(pattern.pattern)
        if isinstance(pattern, URLResolver):
            yield from _resolved_patterns(
                pattern.url_patterns,
                route,
                app_names + ((pattern.app_name,) if pattern.app_name else ()),
                namespaces + ((pattern.namespace,) if pattern.namespace else ()),
            )
        elif isinstance(pattern, URLPattern):
            match = ResolverMatch(
                pattern.callback,
                (),
                {},
                url_name=pattern.name,
                app_names=list(app_names),
                namespaces=list(namespaces),
                route=route,
            )
            yield f"/{route}", match


@register("adminlte2_pdq")
def check_views_define_permissions(app_configs, **kwargs):  # pylint: disable=unused-argument
    """adminlte2_pdq.W001: views that require permissions but define none.

    No user can access such a view. The check uses the same logic as AuthMiddleware,
    so it only runs when the middleware is installed.
    """
    if AUTH_MIDDLEWARE not in getattr(settings, "MIDDLEWARE", []):
        return []

    # pylint: disable=import-outside-toplevel
    from adminlte2_pdq.middleware import AuthMiddleware

    middleware = AuthMiddleware(lambda request: None)
    warnings = []
    for path, match in _resolved_patterns(get_resolver().url_patterns):
        view_data = middleware.parse_view_data(path, match, update_view=False)
        if middleware.view_missing_permissions(view_data):
            warnings.append(
                CheckWarning(
                    f"The {view_data['view_type']} view '{view_data['view_name']}' ({path}) requires "
                    "permissions, but does not have any set. No user can access it.",
                    hint=(
                        "Set the view's permissions, or mark it with allow_without_permissions "
                        "(AllowWithoutPermissionsMixin for class-based views), or add it to "
                        "ADMINLTE2_STRICT_POLICY_WHITELIST."
                    ),
                    obj=view_data["view_class"] or match.func,
                    id="adminlte2_pdq.W001",
                )
            )
    return warnings
