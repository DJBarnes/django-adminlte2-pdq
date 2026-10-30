"""
Base test case for the view access tests: which users can open which views, in each policy setup.

Each test module has one table per policy setup. A table row is a kind of view, and a column is a kind of user. Each
cell is the expected outcome of the user opening the view:

    Y = The page loads.
    L = Redirect to the login page.
    H = Redirect to the home page, with the "permission requirements were not met" message.
    E = The middleware raises ImproperlyConfigured (the view's decorator or mixin conflicts with the policy).

Every row is checked for a function view (decorators) and for a class view (mixins). Every cell also checks the exact
set of warnings the middleware raises, and that each warning is also shown as a message. The whitelist tests run every
table twice: with each view's route in the whitelist (exact), and with the views' path prefix in the matching fuzzy
whitelist (fuzzy).
"""

# System Imports.
import warnings
from contextlib import ExitStack
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django_expanded_test_cases import IntegrationTestCase

# Internal Imports.
from adminlte2_pdq.constants import LOGIN_EXEMPT_WHITELIST, STRICT_POLICY_WHITELIST


# Module Variables.
UserModel = get_user_model()

Y = "page loads"
L = "redirect to login"
H = "redirect to home"
E = "ImproperlyConfigured"

# The wording that differs between function views (decorators) and class views (mixins).
VIEW_TYPES = {
    "function": {
        "based": "function-based",
        "kind": "decorator",
        "allow_anonymous_access": "allow_anonymous_access",
        "login_required": "login_required",
        "allow_without_permissions": "allow_without_permissions",
    },
    "class": {
        "based": "class-based",
        "kind": "mixin",
        "allow_anonymous_access": "AllowAnonymousAccess",
        "login_required": "LoginRequired",
        "allow_without_permissions": "AllowWithoutPermissions",
    },
}

# Each kind of view (the table rows): its route ("adminlte2_pdq_tests:{view_type}-{route}"), its function and class
# names, its page title, and the admin_pdq_data the middleware attaches to its response.
VIEWS = {
    "none": {
        "route": "standard",
        "function": "standard_view",
        "class": "StandardView",
        "title": "Standard View",
        "data": None,
    },
    "allow_anonymous_access": {
        "route": "allow-anonymous-access",
        "function": "allow_anonymous_access_view",
        "class": "AllowAnonymousAccessView",
        "title": "Allow Anonymous Access View",
        "data": {"decorator_name": "allow_anonymous_access", "allow_anonymous_access": True},
    },
    "login_required": {
        "route": "login-required",
        "function": "login_required_view",
        "class": "LoginRequiredView",
        "title": "Login Required View",
        "data": {"decorator_name": "login_required", "login_required": True},
    },
    "allow_without_permissions": {
        "route": "allow-without-permissions",
        "function": "allow_without_permissions_view",
        "class": "AllowWithoutPermissionsView",
        "title": "Allow Without Permissions View",
        "data": {
            "decorator_name": "allow_without_permissions",
            "login_required": True,
            "allow_without_permissions": True,
        },
    },
    "one_permission_required": {
        "route": "one-permission-required",
        "function": "one_permission_required_view",
        "class": "OnePermissionRequiredView",
        "title": "One Permission Required View",
        "data": {
            "decorator_name": "permission_required",
            "login_required": True,
            "one_of_permissions": ("auth.add_foo", "auth.change_foo"),
        },
    },
    "one_permission_required (string)": {
        "route": "one-permission-required-as-string",
        "function": "one_permission_required_view_as_string",
        "class": "OnePermissionRequiredViewAsString",
        "title": "One Permission Required View",
        "data": {
            "decorator_name": "permission_required",
            "login_required": True,
            "one_of_permissions": ("auth.add_foo",),
        },
    },
    "full_permissions_required": {
        "route": "full-permissions-required",
        "function": "full_permissions_required_view",
        "class": "FullPermissionsRequiredView",
        "title": "Full Permissions Required View",
        "data": {
            "decorator_name": "permission_required",
            "login_required": True,
            "full_permissions": ("auth.add_foo", "auth.change_foo"),
        },
    },
    "full_permissions_required (string)": {
        "route": "full-permissions-required-as-string",
        "function": "full_permissions_required_view_as_string",
        "class": "FullPermissionsRequiredViewAsString",
        "title": "Full Permissions Required View",
        "data": {
            "decorator_name": "permission_required",
            "login_required": True,
            "full_permissions": ("auth.add_foo",),
        },
    },
}

# Every route above, for both view types, added to the default whitelists for the whitelist tests.
VIEW_ROUTES = [
    f"adminlte2_pdq_tests:{view_type}-{view['route']}" for view_type in VIEW_TYPES for view in VIEWS.values()
]
LOGIN_WHITELIST = LOGIN_EXEMPT_WHITELIST + VIEW_ROUTES
PERMISSION_WHITELIST = STRICT_POLICY_WHITELIST + VIEW_ROUTES

# The path prefix of every view above, for the fuzzy whitelist tests.
FUZZY_WHITELIST = ("/tests/",)

# The setting each whitelist test patches, in each form, and its value.
WHITELISTS = {
    "login": {
        "exact": ("adminlte2_pdq.middleware.LOGIN_EXEMPT_WHITELIST", LOGIN_WHITELIST),
        "fuzzy": ("adminlte2_pdq.middleware.LOGIN_EXEMPT_FUZZY_WHITELIST", FUZZY_WHITELIST),
    },
    "permission": {
        "exact": ("adminlte2_pdq.middleware.STRICT_POLICY_WHITELIST", PERMISSION_WHITELIST),
        "fuzzy": ("adminlte2_pdq.middleware.STRICT_POLICY_FUZZY_WHITELIST", FUZZY_WHITELIST),
    },
}

# The permissions and groups each kind of user gets. The views use auth.add_foo and auth.change_foo. Group add_bar
# grants add_foo and change_bar grants change_foo. Wrong permissions and groups grant neither.
PERMISSION_SETS = {
    "no permissions": {},
    "wrong permissions": {"permissions": ["view_foo", "delete_foo"]},
    "partial permissions": {"permissions": ["add_foo"]},
    "full permissions": {"permissions": ["add_foo", "change_foo"]},
    "wrong groups": {"groups": ["view_bar", "delete_bar"]},
    "partial groups": {"groups": ["add_bar"]},
    "full groups": {"groups": ["add_bar", "change_bar"]},
}

# The table columns, in order: an = anonymous; in = inactive user (can't log in); for a user and a staff user:
# no = no permissions, wp/pp/fp = wrong/partial/full permissions, wg/pg/fg = wrong/partial/full groups; su = superuser.
USERS = (
    ["anonymous", "inactive user"]
    + [f"user with {name}" for name in PERMISSION_SETS]
    + [f"staff user with {name}" for name in PERMISSION_SETS]
    + ["superuser"]
)

# The middleware's warnings and errors. Formatted with the VIEW_TYPES wording and the view's name.
MESSAGES = {
    "failed_permission_check": (
        "AdminLtePdq Warning: Attempted to access {based} view '{view}' which "
        "requires permissions, and user permission requirements were not met. "
        "Redirected to project home instead. \n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/"
    ),
    "loose_mode__allow_anonymous_access_not_supported": (
        "AdminLtePdq Error: The '{allow_anonymous_access}' {kind} is not supported in AdminLtePdq "
        "LOOSE mode. This {kind} only exists for clarity of permission access in STRICT mode."
    ),
    "loose_mode__allow_without_permissions_not_supported": (
        "AdminLtePdq Error: The '{allow_without_permissions}' {kind} is not supported in AdminLtePdq "
        "LOOSE mode. This {kind} only exists for clarity of permission access in STRICT mode."
    ),
    "login_required_mode__login_required_not_supported": (
        "AdminLtePdq Error: The '{login_required}' {kind} is not supported in AdminLtePdq LOGIN REQUIRED mode. "
        "Having LOGIN REQUIRED mode on implicitly assumes login is required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the '{allow_anonymous_access}' {kind}."
    ),
    "login_required_mode__allow_without_permissions_not_supported": (
        "AdminLtePdq Error: The '{allow_without_permissions}' {kind} is not supported in AdminLtePdq "
        "LOGIN REQUIRED mode. This {kind} only exists for clarity of permission access in STRICT mode."
    ),
    "strict_mode__login_required_not_supported": (
        "AdminLtePdq Error: The '{login_required}' {kind} is not supported in AdminLtePdq STRICT mode. "
        "Having STRICT mode on implicitly assumes login and permissions are required "
        "for all views that are not in a whitelist setting."
        "\n\n"
        "Also consider the '{allow_anonymous_access}' or '{allow_without_permissions}' {kind}s."
    ),
    "login_required_and_login_whitelist": (
        "AdminLtePdq Error: The {based} view '{view}' has a '{login_required}' "
        "{kind}, but is in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST setting. Please remove one."
    ),
    "allow_anonymous_access_and_login_whitelist": (
        "AdminLtePdq Warning: The {based} view '{view}' has an '{allow_anonymous_access}' "
        "{kind}, but is also in the ADMINLTE2_LOGIN_EXEMPT_WHITELIST. These two effectively "
        "achieve the same functionality."
    ),
    "allow_without_permissions_and_permission_whitelist": (
        "AdminLtePdq Warning: The {based} view '{view}' has an "
        "'{allow_without_permissions}' {kind}, but is also in the ADMINLTE2_STRICT_POLICY_WHITELIST. "
        "These two effectively achieve the same functionality."
    ),
    "permissions_and_permission_whitelist": (
        "AdminLtePdq Error: The {based} view '{view}' has a permission "
        "{kind}, but is in the ADMINLTE2_STRICT_POLICY_WHITELIST setting. Please remove one."
    ),
    "ineffective_login_whitelist": (
        "AdminLtePdq Warning: The {based} view '{view}' is login whitelisted, "
        "but the view still requires permissions. A user must login to have permissions, so the login whitelist is "
        "redundant and probably not achieving the desired effect. Correct this by adding the view to "
        "the permission whitelist setting (ADMINLTE2_STRICT_POLICY_WHITELIST), or by adding the "
        "'{allow_without_permissions}' {kind}."
    ),
    "strict_mode__no_decorators": (
        "AdminLtePdq Warning: This project is set to run in strict mode, and "
        "the {based} view '{view}' does not have any {kind}s set. "
        "This means that this view is inaccessible until permission {kind}s "
        "are set for the view, or the view is added to the "
        "ADMINLTE2_STRICT_POLICY_WHITELIST setting."
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    ),
    "missing_permissions": (
        "AdminLtePdq Warning: The {based} view '{view}' has permission "
        "requirements, but does not have any permissions set. "
        "This means that this view is inaccessible until permissions "
        "are set for the view.\n"
        "\n\n"
        "For further information, please see the docs: "
        "https://django-adminlte2-pdq.readthedocs.io/en/latest/authorization/policies.html#strict-policy"
    ),
}


def message(name, view_type, row, **extra):
    """The text of a middleware message, for a view type and a table row."""
    return MESSAGES[name].format(**VIEW_TYPES[view_type], view=VIEWS[row][view_type], **extra)


class Notice:
    """A warning the middleware raises for a row, which is also shown as a message (DEBUG mode).

    By default the notice applies to both view types and to every user. With logged_in_only, only users who pass
    the login check get it, because the middleware raises it after that check.
    """

    def __init__(self, name, view_type=None, logged_in_only=False):
        self.name = name
        self.view_type = view_type
        self.logged_in_only = logged_in_only

    def applies(self, view_type, user):
        """Whether the user gets this notice, when opening the view type."""
        if self.view_type not in (None, view_type):
            return False
        return not self.logged_in_only or (user.is_authenticated and user.is_active)


class AccessTestCase(IntegrationTestCase):
    """Base class for the view access tests."""

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        # The permissions and groups the users get. unused_foo checks that unrelated permissions don't matter.
        content_type = ContentType.objects.get_for_model(Permission)
        for codename in ("add_foo", "change_foo", "view_foo", "delete_foo", "unused_foo"):
            permission = Permission.objects.create(name=codename, codename=codename, content_type=content_type)
            group = Group.objects.create(name=codename.replace("_foo", "_bar"))
            group.permissions.add(permission)

    def _create_table_user(self, name):
        """Create the user for a table column."""
        if name == "anonymous":
            return AnonymousUser()
        user = self.get_user(name.replace(" ", "_"))
        if name == "inactive user":
            user.is_active = False
        elif name == "superuser":
            user.is_superuser = True
        else:
            user.is_staff = name.startswith("staff user with ")
            permission_set = PERMISSION_SETS[name.split(" with ", 1)[1]]
            user.user_permissions.set(Permission.objects.filter(codename__in=permission_set.get("permissions", [])))
            user.groups.set(Group.objects.filter(name__in=permission_set.get("groups", [])))
        user.save()
        return user

    def _create_table_users(self):
        """Create one user for each table column."""
        return {name: self._create_table_user(name) for name in USERS}

    def assert_access(self, table, whitelists=(), forms=("exact", "fuzzy"), notices=None, errors=None):
        """Check every view and user in a table, for function views and class views.

        :param table: The expected outcome for each row and user.
        :param whitelists: The whitelists ("login", "permission") every view is in. The table is checked once for
            each form of the whitelists.
        :param forms: The forms of the whitelists to check: "exact", "fuzzy", or both.
        :param notices: For each row, the Notices (warnings) the middleware raises.
        :param errors: For each row with E cells, the name of the ImproperlyConfigured message.
        """
        notices = notices or {}
        errors = errors or {}
        self.assertEqual(list(table), list(VIEWS), "The table must have a row for every kind of view.")
        error_rows = {row for row, cells in table.items() if E in cells}
        self.assertEqual(error_rows, set(errors), "Every row with E cells, and only those, must name its error.")

        users = self._create_table_users()
        for form in forms if whitelists else (None,):
            with ExitStack() as stack:
                for whitelist in whitelists:
                    stack.enter_context(patch(*WHITELISTS[whitelist][form]))
                for view_type in VIEW_TYPES:
                    for row, cells in table.items():
                        self.assertEqual(len(cells), len(USERS), f"The {row} row must have a column for every user.")
                        for (user_name, user), outcome in zip(users.items(), cells):
                            labels = {"view": f"{view_type} view, {row}", "user": user_name}
                            if form:
                                labels["whitelists"] = form
                            with self.subTest(**labels):
                                expected_notices = [
                                    message(notice.name, view_type, row)
                                    for notice in notices.get(row, [])
                                    if notice.applies(view_type, user)
                                ]
                                self.assert_outcome(view_type, row, user, outcome, expected_notices, errors.get(row))

    def assert_outcome(self, view_type, row, user, outcome, expected_notices, error):
        """Open the view as the user, and check the outcome, warnings, and messages."""
        route = f"adminlte2_pdq_tests:{view_type}-{VIEWS[row]['route']}"
        failed_permission_check = message("failed_permission_check", view_type, row)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")

            if outcome == E:
                with self.assertRaises(ImproperlyConfigured) as err:
                    self.assertGetResponse(route, user=user, expected_status=500)
                self.assertText(message(error, view_type, row), str(err.exception))
                response = None

            elif outcome == L:
                response = self.assertGetResponse(
                    route,
                    user=user,
                    expected_status=200,
                    view_should_redirect=True,
                    expected_title="Login |",
                    expected_content=["Sign in to start your session", "Remember Me", "I forgot my password"],
                    expected_messages=expected_notices,
                )

            elif outcome == H:
                response = self.assertGetResponse(
                    route,
                    user=user,
                    expected_status=200,
                    view_should_redirect=True,
                    expected_title="Dashboard",
                    expected_header="Dashboard <small>Version 2.0</small>",
                    expected_content=["Monthly Recap Report", "Visitors Report", "Inventory", "Downloads"],
                    expected_messages=[failed_permission_check, *expected_notices],
                )

            else:
                self.assertEqual(Y, outcome, f"Unknown outcome: {outcome}")
                response = self.assertGetResponse(
                    route,
                    user=user,
                    expected_status=200,
                    view_should_redirect=False,
                    expected_title=f"{VIEWS[row]['title']} | Django AdminLtePdq Testing",
                    expected_header=f"Django AdminLtePdq | {VIEWS[row]['title']} Header",
                    expected_messages=expected_notices,
                    expected_not_messages=[failed_permission_check],
                )

        actual_notices = sorted(
            str(warning.message) for warning in caught if str(warning.message).startswith("AdminLtePdq")
        )
        self.assertEqual(sorted(expected_notices), actual_notices, "Unexpected middleware warnings.")

        if response is not None:
            if outcome == Y and VIEWS[row]["data"]:
                self.assertAdminPdqData(response, **VIEWS[row]["data"])
            else:
                self.assertAdminPdqData(response, is_empty=True)

    def assertAdminPdqData(  # pylint:disable=invalid-name
        self,
        response,
        is_empty=False,
        decorator_name=None,
        allow_anonymous_access=False,
        login_required=False,
        allow_without_permissions=False,
        one_of_permissions=None,
        full_permissions=None,
    ):
        """Check the admin_pdq_data the middleware attached to the response.

        :param response: Page response to check.
        :param is_empty: Whether the response should have no data (views without decorators or mixins, redirects).
        :param decorator_name: Expected decorator_name value.
        :param allow_anonymous_access: Expected allow_anonymous_access value.
        :param login_required: Expected login_required value.
        :param allow_without_permissions: Expected allow_without_permissions value.
        :param one_of_permissions: Expected one_of_permissions value.
        :param full_permissions: Expected full_permissions value.
        """
        if is_empty:
            self.assertFalse(hasattr(response, "admin_pdq_data"))
            return

        self.assertTrue(hasattr(response, "admin_pdq_data"))
        data = response.admin_pdq_data
        self.assertEqual(decorator_name, data["decorator_name"])
        self.assertEqual(bool(allow_anonymous_access), bool(data["allow_anonymous_access"]))
        self.assertEqual(bool(login_required), bool(data["login_required"]))
        self.assertEqual(bool(allow_without_permissions), bool(data["allow_without_permissions"]))
        if one_of_permissions:
            self.assertEqual(one_of_permissions, tuple(data["one_of_permissions"]))
        else:
            self.assertIsNone(data["one_of_permissions"])
        if full_permissions:
            self.assertEqual(full_permissions, tuple(data["full_permissions"]))
        else:
            self.assertIsNone(data["full_permissions"])
