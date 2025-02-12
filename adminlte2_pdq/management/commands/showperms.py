"""
Command to list all permissions.
"""

# Third-Party Imports.
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.db.models import F


class Command(BaseCommand):
    """Command to list out all project permissions."""

    help = "List out all of the permissions in the database."

    def add_arguments(self, parser):
        """Define arguments to pass into command."""

        parser.add_argument(
            "--hide-names",
            default=False,
            action="store_true",
            help='Skip displaying permission "name" value for each permission.',
        )
        parser.add_argument(
            "--hide-codenames",
            default=False,
            action="store_true",
            help='Skip displaying permission "codename" value for each permission.',
        )
        parser.add_argument(
            "--hide-content-types",
            default=False,
            action="store_true",
            help='Skip displaying "content type" value for each permission.',
        )

    def handle(self, *args, **options):
        """Entry point of command logic."""

        # Structure to hold the maximum length found of each data type, for output formatting.
        # Default length of 0.
        max_lengths = {
            "name_len": 0,
            "codename_len": 0,
            "content_type_len": 0,
        }

        # Handle permission "name" arg.
        if options["hide_names"]:
            include_names = False
        else:
            include_names = True

        # Handle permission "codename" arg.
        if options["hide_codenames"]:
            include_codenames = False
        else:
            include_codenames = True

        # Handle permission "content type" arg.
        if options["hide_content_type"]:
            include_content_types = False
        else:
            include_content_types = True

        # Get all permission objects.
        # all_permissions = Permission.objects.all()
        all_permissions = Permission.objects.order_by(
            "content_type__app_label",
            "codename",
        ).values(
            "name",
            "codename",
            content_type_label=F("content_type__app_label"),
        )

        # Update calculated max lengths.
        for perm in all_permissions:
            max_lengths["name_len"] = max(max_lengths["name_len"], len(perm["name"]))
            max_lengths["codename_len"] = max(max_lengths["codename_len"], len(perm["codename"]))
            max_lengths["content_type_len"] = max(max_lengths["content_type_len"], len(perm["content_type_label"]))

        # Calculate separator and header strings.
        header_str, separator_str, max_lengths = self.process_header_str(
            include_names,
            include_codenames,
            include_content_types,
            max_lengths,
        )

        # Display header separators.
        self.stdout.write(self.style.SUCCESS(separator_str))
        self.stdout.write(self.style.SUCCESS(header_str))
        self.stdout.write(self.style.SUCCESS(separator_str))

        current_content_type = ""
        for perm in all_permissions:

            # Handle if con tent type changed.
            if current_content_type == "":
                current_content_type = perm["content_type_label"]
            elif current_content_type != perm["content_type_label"]:
                self.stdout.write(self.style.WARNING(separator_str))
                current_content_type = perm["content_type_label"]

            line = ""
            if include_content_types:
                line += "| {content_type_label:{content_type_len}} "

            if include_names:
                line += "| {name:{name_len}} "

            if include_codenames:
                line += "| {codename:{codename_len}} "

            line += "|"

            # Print parsed output values to console.
            self.stdout.write(line.format(**perm, **max_lengths))

        # Display footer separators.
        self.stdout.write(self.style.SUCCESS(separator_str))

    def process_header_str(
        self,
        include_names,
        include_codenames,
        include_content_types,
        max_lengths,
    ):
        """Calculates header string and separator string values for nicer output."""

        header_str = ""
        separator_str = ""

        # Handle "content type" value.
        if include_content_types:
            header_value = "Content Type"
            max_lengths["content_type_len"] = max(max_lengths["content_type_len"], len(header_value))
            header_str += "| "
            separator_str += "+-"
            header_str += header_value.ljust(max_lengths["content_type_len"])
            separator_str += "-" * max_lengths["content_type_len"]

        # Handle "name" value.
        if include_names:
            header_value = "Name"
            max_lengths["name_len"] = max(max_lengths["name_len"], len(header_value))
            if separator_str == "":
                header_str += "| "
                separator_str += "+-"
            else:
                header_str += " | "
                separator_str += "-+-"
            header_str += header_value.ljust(max_lengths["name_len"])
            separator_str += "-" * max_lengths["name_len"]

        # Handle "codename" value.
        if include_codenames:
            header_value = "Codename"
            max_lengths["codename_len"] = max(max_lengths["codename_len"], len(header_value))
            if separator_str == "":
                header_str += "| "
                separator_str += "+-"
            else:
                header_str += " | "
                separator_str += "-+-"
            header_str += header_value.ljust(max_lengths["codename_len"])
            separator_str += "-" * max_lengths["codename_len"]

        header_str += " |"
        separator_str += "-+"

        # Return calculated values.
        return header_str, separator_str, max_lengths
