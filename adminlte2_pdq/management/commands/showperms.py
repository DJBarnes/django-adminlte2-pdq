"""
Command to list all permissions.
"""

# Third-Party Imports.
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.db.models import F, Value
from django.db.models.functions import Concat


class Command(BaseCommand):
    """Command to list out all project permissions."""

    help = "List out all of the permissions in the database."

    DEFAULT_PERMS = (
        "add_",
        "change_",
        "delete_",
        "view_",
    )

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
            help='Skip displaying the "content type" value for each permission.',
        )
        parser.add_argument(
            "--hide-has_perm-text",
            default=False,
            action="store_true",
            help='Skip displaying the "has_perm" value for each permission.',
        )
        parser.add_argument(
            "--hide-default-perms",
            default=False,
            action="store_true",
            help=(
                "Skip displaying the default perms that every model has. "
                "EX: add_<MODEL>, change_<MODEL>, delete_<MODEL>, view_<MODEL> "
                'NOTE: This option uses "starts_with" to omit perms and could hide others that start the same way.'
            ),
        )

    def handle(self, *args, **options):
        """Entry point of command logic."""

        # Structure to hold the maximum length found of each data type, for output formatting.
        # Default length of 0.
        max_lengths = {
            "name_len": 0,
            "codename_len": 0,
            "content_type_len": 0,
            "has_perm_len": 0,
        }

        # Handle permission "name" arg.
        include_names = not options["hide_names"]

        # Handle permission "codename" arg.
        include_codenames = not options["hide_codenames"]

        # Handle permission "content type" arg.
        include_content_types = not options["hide_content_types"]

        # Handle permission default arg.
        include_default_types = not options["hide_default_perms"]

        # Handle permission has_perm text.
        include_has_perm_text = not options["hide_has_perm_text"]

        # Get all permission objects.
        # all_permissions = Permission.objects.all()
        all_permissions = Permission.objects.order_by(
            "content_type__app_label",
            "codename",
        ).values(
            "name",
            "codename",
            content_type_label=F("content_type__app_label"),
            has_perm_label=Concat("content_type__app_label", Value("."), "codename"),
        )

        # Update calculated max lengths.
        for perm in all_permissions:
            max_lengths["name_len"] = max(max_lengths["name_len"], len(perm["name"]))
            max_lengths["codename_len"] = max(max_lengths["codename_len"], len(perm["codename"]))
            max_lengths["content_type_len"] = max(max_lengths["content_type_len"], len(perm["content_type_label"]))
            max_lengths["has_perm_len"] = max(max_lengths["has_perm_len"], len(perm["has_perm_label"]))

        # Calculate separator and header strings.
        header_str, separator_str, max_lengths = self.process_header_str(
            include_names,
            include_codenames,
            include_content_types,
            include_has_perm_text,
            max_lengths,
        )

        # Display header separators.
        self.stdout.write(self.style.SUCCESS(separator_str))
        self.stdout.write(self.style.SUCCESS(header_str))
        self.stdout.write(self.style.SUCCESS(separator_str))

        current_content_type = ""
        for perm in all_permissions:

            # Check to see if we should skip the built-in default perms
            if not include_default_types and perm["codename"].startswith(self.DEFAULT_PERMS):
                continue

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

            if include_has_perm_text:
                line += "| {has_perm_label:{has_perm_len}} "

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
        include_has_perm_text,
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

        # Handle "has_perm" value.
        if include_has_perm_text:
            header_value = "has_perm"
            max_lengths["has_perm_len"] = max(max_lengths["has_perm_len"], len(header_value))
            if separator_str == "":
                header_str += "| "
                separator_str += "+-"
            else:
                header_str += " | "
                separator_str += "-+-"
            header_str += header_value.ljust(max_lengths["has_perm_len"])
            separator_str += "-" * max_lengths["has_perm_len"]

        header_str += " |"
        separator_str += "-+"

        # Return calculated values.
        return header_str, separator_str, max_lengths
