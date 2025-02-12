"""
Command to list all URL routes in project.
"""

# System Imports.
import ast
import inspect

# Third-Party Imports.
from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls.resolvers import URLPattern, URLResolver

# Internal Imports.
from adminlte2_pdq.mixins import (
    AllowAnonymousAccessMixin,
    LoginRequiredMixin,
    AllowWithoutPermissionsMixin,
    PermissionRequiredMixin,
)


class Command(BaseCommand):
    """Command to list out all URL routes."""

    help = "List out all URL routes and their names"

    def add_arguments(self, parser):
        """Define arguments to pass into command."""

        parser.add_argument(
            "--hide-app-names",
            default=False,
            action="store_true",
            help="Skip displaying app name at far left side.",
        )
        parser.add_argument(
            "--hide-url-names",
            default=False,
            action="store_true",
            help='Skip displaying url "endpoint name" values for each route.',
        )
        parser.add_argument(
            "--show-lookup-strings",
            default=False,
            action="store_true",
            help='Display "lookup strings" values for each route.',
        )
        parser.add_argument(
            "--show-default-args",
            default=False,
            action="store_true",
            help='Display "default route" args for each route.',
        )

    def handle(self, *args, **options):
        """Entry point of command logic."""

        # Dict of arrays that our url data will populate to. These arrays are then read in for std output.
        all_urls = {
            "allow_anonymous_access": [],
            "login_required": [],
            "allow_without_permissions": [],
            "permission_required_one": [],
            "permission_required": [],
        }

        # Structure to hold the maximum length found of each data type, for output formatting.
        # Default length of 0.
        max_lengths = {
            "app_name_len": 0,
            "pattern_len": 0,
            "name_len": 0,
            "lookup_str_len": 0,
            "default_args_len": 0,
        }

        # Handle "app name" arg.
        if options["hide_app_names"]:
            include_app_names = False
        else:
            include_app_names = True

        # Handle "app name" arg.
        if options["hide_url_names"]:
            include_url_names = False
        else:
            include_url_names = True

        # Handle "lookup str" arg.
        if options["show_lookup_strings"]:
            include_lookup_str = True
        else:
            include_lookup_str = False

        # Handle "default_args" arg.
        if options["show_default_args"]:
            include_default_args = True
        else:
            include_default_args = False

        # Import project urls.
        # Done this way to force urls to populate fully.
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])

        decorated_views = {
            "allow_anonymous_access": [],
            "login_required": [],
            "allow_without_permissions": [],
            "permission_required_one": [],
            "permission_required": [],
        }

        app_name = ""

        def process_decorators_mixins(urlpatterns, decorated_views, acc=None):
            """Checks for use of package decorators and mixins across registered project views."""

            nonlocal app_name

            # Populate if array is not yet set.
            if acc is None:
                acc = []

            # Return if nothing further to parse.
            if not urlpatterns:
                return

            # Get first pattern in set.
            url = urlpatterns[0]

            # Attempt to determine app name.
            new_app_name = getattr(url, "app_name", None)
            if new_app_name:
                app_name = new_app_name
            url.app_name = app_name

            # Only proceed if dealing with actual url pattern.
            if isinstance(url, URLPattern):

                # Try-catch to attempt to find views with decorators/mixins from this package.
                try:
                    # Parse the url data to import project views and then parse data about them.
                    # This seems to be the required minimum in order to check for decorators/mixins.
                    import_str = url.lookup_str
                    import_str = import_str.split(".")
                    view_name = import_str[-1]
                    import_str = ".".join(import_str[:-1])
                    module_data = __import__(import_str, globals={}, locals={}, fromlist=[""])
                    view_data = getattr(module_data, view_name, None)
                    is_handled = False

                    # Handle if class is in project "ADMINLTE2_LOGIN_EXEMPT_WHITELIST" setting.
                    if hasattr(settings, "ADMINLTE2_LOGIN_EXEMPT_WHITELIST") and (
                        url.name in settings.ADMINLTE2_LOGIN_EXEMPT_WHITELIST
                        or f"{url.app_name}:{url.name}" in settings.ADMINLTE2_STRICT_POLICY_WHITELIST
                    ):
                        decorated_views["login_required"].append(url)

                    # Handle if class is in project "ADMINLTE2_STRICT_POLICY_WHITELIST" setting.
                    if hasattr(settings, "ADMINLTE2_STRICT_POLICY_WHITELIST") and (
                        url.name in settings.ADMINLTE2_STRICT_POLICY_WHITELIST
                        or f"{url.app_name}:{url.name}" in settings.ADMINLTE2_STRICT_POLICY_WHITELIST
                    ):
                        decorated_views["allow_without_permissions"].append(url)

                    # Handle if is class has package mixins.
                    if view_name in AllowAnonymousAccessMixin.subclasses:
                        decorated_views["allow_anonymous_access"].append(url)
                        is_handled = True
                    elif view_name in LoginRequiredMixin.subclasses:
                        decorated_views["login_required"].append(url)
                        is_handled = True
                    elif view_name in AllowWithoutPermissionsMixin.subclasses:
                        decorated_views["allow_without_permissions"].append(url)
                        is_handled = True
                    elif view_name in PermissionRequiredMixin.subclasses:
                        decorated_views["permission_required"].append(url)
                        is_handled = True

                    # Otherwise might be a method decorator.
                    if not is_handled:
                        # Attempt to parse decorator data out of view.
                        parsed_decorators = self.get_decorators(view_data)[view_name]

                        # Check if parsed data matches package decorators.
                        if "allow_anonymous_access" in parsed_decorators:
                            decorated_views["allow_anonymous_access"].append(url)
                        elif "login_required" in parsed_decorators:
                            decorated_views["login_required"].append(url)
                        elif "allow_without_permissions" in parsed_decorators:
                            decorated_views["allow_without_permissions"].append(url)
                        elif "permission_required_one" in parsed_decorators:
                            decorated_views["permission_required_one"].append(url)
                        elif "permission_required" in parsed_decorators:
                            decorated_views["permission_required"].append(url)

                except (ModuleNotFoundError, KeyError):
                    # If we ran into one of these errors, either was a built-in Django view that won't have
                    # this package's custom decorators/mixins, or it's a view that didn't have an association
                    # with this package's custom decorators/mixins.
                    # In either case, should be good to ignore exception.
                    pass

            elif isinstance(url, URLResolver):
                process_decorators_mixins(url.url_patterns, decorated_views, acc + [str(url.pattern)])

            # Call function again, minus url at start of set.
            process_decorators_mixins(urlpatterns[1:], decorated_views, acc)

        # Call function to parse project views for decorators/mixins.
        process_decorators_mixins(urlconf.urlpatterns, decorated_views)

        def parse_url_data(urlpatterns, decorator_type=None, acc=None):
            """Process URL route data."""

            # Populate if array is not yet set.
            if acc is None:
                acc = []

            # Return if nothing further to parse.
            if not urlpatterns:
                return

            # Get first pattern in set.
            url = urlpatterns[0]

            # Only proceed if dealing with actual url pattern.
            if isinstance(url, URLPattern):

                pattern = "".join(acc + [str(url.pattern)])

                if len(pattern) == 0 or pattern[-1] != "/":
                    pattern += "/"

                # Process url "name" as defined in the Django url definition.
                name = str(url.name).strip()
                if name == "" or name == "None":
                    name = "None"
                elif url.app_name:
                    name = url.app_name + ":" + name

                # Add parsed values to processed url list.
                all_urls[decorator_type].append(
                    {
                        "app_name": url.app_name,
                        "pattern": pattern,
                        "name": name,
                        "lookup_str": url.lookup_str,
                        "default_args": str(url.default_args),
                    }
                )

                # Update calculated max lengths.
                if include_app_names:
                    max_lengths["app_name_len"] = max(max_lengths["app_name_len"], len(url.app_name))
                max_lengths["pattern_len"] = max(max_lengths["pattern_len"], len(pattern))
                if include_url_names:
                    max_lengths["name_len"] = max(max_lengths["name_len"], len(name))
                if include_lookup_str:
                    max_lengths["lookup_str_len"] = max(max_lengths["lookup_str_len"], len(str(url.lookup_str)))
                if include_default_args:
                    max_lengths["default_args_len"] = max(max_lengths["default_args_len"], len(str(url.default_args)))
            elif isinstance(url, URLResolver):
                parse_url_data(url.url_patterns, decorator_type, acc + [str(url.pattern)])

            # Call function again, minus url at start of set.
            parse_url_data(urlpatterns[1:], decorator_type, acc)

        # Call function to parse project url data.
        parse_url_data(decorated_views["allow_anonymous_access"], "allow_anonymous_access")
        parse_url_data(decorated_views["login_required"], "login_required")
        parse_url_data(decorated_views["allow_without_permissions"], "allow_without_permissions")
        parse_url_data(decorated_views["permission_required_one"], "permission_required_one")
        parse_url_data(decorated_views["permission_required"], "permission_required")

        # Calculate separator and header strings.
        header_str, separator_str, max_lengths = self.process_header_str(
            include_app_names,
            include_url_names,
            include_lookup_str,
            include_default_args,
            max_lengths,
        )

        self.stdout.write()
        self.stdout.write(
            "The following are views that use the permission and authentication decorators/mixins defined within the "
            "AdminLte2_Pdq Django package.\n"
            "For a full list of views (regardless of decorators/mixins), use the `manage.py showroutes` command."
        )
        self.stdout.write()

        # Display header separators.
        self.stdout.write(self.style.SUCCESS(separator_str))
        self.stdout.write(self.style.SUCCESS(header_str))
        self.stdout.write(self.style.SUCCESS(separator_str))

        # Display parsed url data.
        for decorator_type in [
            ("allow_anonymous_access", "Allow Anonymous Access"),
            ("login_required", "Logic Required"),
            ("allow_without_permissions", "Allow Without Permissions"),
            ("permission_required_one", "One Permission Required"),
            ("permission_required", "Permission Required"),
        ]:
            # Get the url set for current decorator type.
            url_set = all_urls[decorator_type[0]]

            # Make sure current decorator type has at least one url. Otherwise skip output.
            if len(url_set) == 0:
                continue

            # Output separator indicating what type of decorator is displaying.
            decorator_str = f"===== {len(url_set)} Views - "
            decorator_str += decorator_type[1]
            decorator_str += " ="
            decorator_str = decorator_str.ljust(len(separator_str), "=")

            self.stdout.write(self.style.WARNING(separator_str))
            self.stdout.write(self.style.WARNING(decorator_str))
            self.stdout.write(self.style.WARNING(separator_str))

            # Process output for this subset of urls.
            for url_dict in url_set:

                line = ""
                if include_app_names:
                    line += "| {app_name:{app_name_len}} "
                line += "| {pattern:{pattern_len}} |"
                if include_url_names:
                    line += " {name:{name_len}} |"
                if include_lookup_str:
                    line = line + " {lookup_str:{lookup_str_len}} |"
                if include_default_args:
                    line = line + " {default_args:{default_args_len}} |"

                # Print parsed output values to console.
                self.stdout.write(line.format(**url_dict, **max_lengths))

        # Display footer separators.
        self.stdout.write(self.style.SUCCESS(separator_str))

    def get_decorators(self, value):
        """Parses the decorators/mixins associated with provided view.

        Original logic (for parsing decorators) from:
        https://stackoverflow.com/a/31197273
        """
        if inspect.isclass(value):
            # Is class view, so it won't have the decorator's we're searching for.
            # Return empty dict.
            return {}

        target = value
        decorators = {}

        def visit_FunctionDef(node):
            decorators[node.name] = []
            for n in node.decorator_list:
                name = ""
                if isinstance(n, ast.Call):
                    name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
                else:
                    name = n.attr if isinstance(n, ast.Attribute) else n.id

                decorators[node.name].append(name)

        # Function view. May have package decorators. Continue.
        node_iter = ast.NodeVisitor()
        node_iter.visit_FunctionDef = visit_FunctionDef
        node_iter.visit(ast.parse(inspect.getsource(target)))

        # Return dict of parsed decorators from view.
        return decorators

    def process_header_str(
        self,
        include_app_names,
        include_url_names,
        include_lookup_str,
        include_default_args,
        max_lengths,
    ):
        """Calculates header string and separator string values for nicer output."""

        header_str = ""
        separator_str = ""

        # Handle "app name" value.
        if include_app_names:
            header_value = "App Name"
            max_lengths["app_name_len"] = max(max_lengths["app_name_len"], len(header_value))
            header_str += "| "
            separator_str += "+-"
            header_str += header_value.ljust(max_lengths["app_name_len"])
            separator_str += "-" * max_lengths["app_name_len"]

        # Handle "pattern" value.
        header_value = "Url Pattern"
        max_lengths["pattern_len"] = max(max_lengths["pattern_len"], len(header_value))
        if header_str == "":
            header_str += "| "
            separator_str += "+-"
        else:
            header_str += " | "
            separator_str += "-+-"
        header_str += header_value.ljust(max_lengths["pattern_len"])
        separator_str += "-" * max_lengths["pattern_len"]

        # Handle "name" value.
        if include_url_names:
            header_value = "Url Endpoint Name"
            max_lengths["name_len"] = max(max_lengths["name_len"], len(header_value))
            header_str += " | "
            separator_str += "-+-"
            header_str += header_value.ljust(max_lengths["name_len"])
            separator_str += "-" * max_lengths["name_len"]

        # Handle "lookup" value.
        if include_lookup_str:
            header_value = "Lookup String"
            max_lengths["lookup_str_len"] = max(max_lengths["lookup_str_len"], len(header_value))
            header_str += " | "
            separator_str += "-+-"
            header_str += header_value.ljust(max_lengths["lookup_str_len"])
            separator_str += "-" * max_lengths["lookup_str_len"]

        # Handle "default args" value.
        if include_default_args:
            header_value = "Default Args"
            max_lengths["default_args_len"] = max(max_lengths["default_args_len"], len(header_value))
            header_str += " | "
            separator_str += "-+-"
            header_str += header_value.ljust(max_lengths["default_args_len"])
            separator_str += "-" * max_lengths["default_args_len"]

        header_str += " |"
        separator_str += "-+"

        # Return calculated values.
        return header_str, separator_str, max_lengths
