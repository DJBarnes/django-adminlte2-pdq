"""
Command to list all URL routes in project.
"""

# Third-Party Imports.
from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls.resolvers import URLPattern, URLResolver


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

        # Array that our url data will populate to. This array is then read in for std output.
        all_urls = []

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
        urlconf = __import__(settings.ROOT_URLCONF, globals={}, locals={}, fromlist=[""])

        app_name = ""

        def parse_url_data(urlpatterns, acc=None):
            """Process URL route data."""

            nonlocal app_name

            # Populate if array is not yet set.
            if acc is None:
                acc = []

            # Return if nothing further to parse.
            if not urlpatterns:
                return

            # Get first pattern in set.
            url = urlpatterns[0]

            # Attempt to determine app name
            new_app_name = getattr(url, "app_name", None)
            if new_app_name:
                app_name = new_app_name

            # Only proceed if dealing with actual url pattern.
            if isinstance(url, URLPattern):
                pattern = "".join(acc + [str(url.pattern)])

                if len(pattern) == 0 or pattern[-1] != "/":
                    pattern += "/"

                # Process url "name" as defined in the Django url definition.
                name = str(url.name).strip()
                if name == "" or name == "None":
                    name = "None"
                elif app_name:
                    name = app_name + ":" + name

                # Add parsed values to processed url list.
                all_urls.append(
                    {
                        "app_name": app_name,
                        "pattern": pattern,
                        "name": name,
                        "lookup_str": url.lookup_str,
                        "default_args": str(url.default_args),
                    }
                )

                # Update calculated max lengths.
                if include_app_names:
                    max_lengths["app_name_len"] = max(max_lengths["app_name_len"], len(app_name))
                max_lengths["pattern_len"] = max(max_lengths["pattern_len"], len(pattern))
                if include_url_names:
                    max_lengths["name_len"] = max(max_lengths["name_len"], len(name))
                if include_lookup_str:
                    max_lengths["lookup_str_len"] = max(max_lengths["lookup_str_len"], len(str(url.lookup_str)))
                if include_default_args:
                    max_lengths["default_args_len"] = max(max_lengths["default_args_len"], len(str(url.default_args)))
            elif isinstance(url, URLResolver):
                parse_url_data(url.url_patterns, acc + [str(url.pattern)])

            # Call function again, minus url at start of set.
            parse_url_data(urlpatterns[1:], acc)

        # Call function to parse project url data.
        parse_url_data(urlconf.urlpatterns)

        # Calculate separator and header strings.
        header_str, separator_str, max_lengths = self.process_header_str(
            include_app_names,
            include_url_names,
            include_lookup_str,
            include_default_args,
            max_lengths,
        )

        # Display header separators.
        self.stdout.write(self.style.SUCCESS(separator_str))
        self.stdout.write(self.style.SUCCESS(header_str))
        self.stdout.write(self.style.SUCCESS(separator_str))

        # Display parsed url data.
        current_app_name = ""
        for url_dict in all_urls:

            # Handle if app name changed.
            if current_app_name == "":
                current_app_name = url_dict["app_name"]
            elif current_app_name != url_dict["app_name"]:
                self.stdout.write(self.style.WARNING(separator_str))
                current_app_name = url_dict["app_name"]

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
