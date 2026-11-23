"""
Command to generate the CSS for a project's own color, or new values for one of the package's colors.
"""

# System Imports.
import sys
from pathlib import Path

# Third-Party Imports.
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Internal Imports.
from adminlte2_pdq.generate_color_css import ALIASES, NAMES, make_color, render_color_file


class Command(BaseCommand):
    """Command to write a color's CSS to a file, and explain how to load it."""

    help = (
        "Write the CSS for a new color, or new values for one of the package's colors, to a file to load after the "
        "package's CSS."
    )

    def add_arguments(self, parser):
        """Define arguments to pass into command."""

        parser.add_argument("name", help="The color's name, such as brand or light-blue.")
        parser.add_argument("base", help="The color itself, as a hex value, such as #6610f2.")
        parser.add_argument(
            "--active",
            help="The darker shade, for bg-{name}-active and modal headers. Default: the color darkened by 5%%.",
        )
        text = parser.add_mutually_exclusive_group()
        text.add_argument(
            "--dark-text",
            dest="dark_text",
            action="store_const",
            const=True,
            help="Use dark text on the color. Default: dark or white, whichever is easier to read.",
        )
        text.add_argument(
            "--light-text",
            dest="dark_text",
            action="store_const",
            const=False,
            help="Use white text on the color.",
        )
        parser.add_argument(
            "--output",
            help=(
                "The file to write. Default: css/colors/{name}.css in the first STATICFILES_DIRS directory, or "
                "{name}.css in the current directory when STATICFILES_DIRS is empty."
            ),
        )
        parser.add_argument("--force", action="store_true", help="Replace the file without asking if it exists.")

    def handle(self, *args, **options):
        """Entry point of command logic."""
        name = options["name"]

        try:
            color = make_color(name, options["base"], active=options["active"], dark_text=options["dark_text"])
        except ValueError as error:
            raise CommandError(str(error)) from error

        output = Path(options["output"]) if options["output"] else self.default_output(name)
        if output.exists() and not options["force"] and not self.confirm(f"{output} exists. Replace it? [y/N] "):
            self.stdout.write("Nothing written.")
            return

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_color_file(color), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"Wrote {output}"))
        self.stdout.write("")
        if name in NAMES:
            self.stdout.write(self.package_color_notice(name))
            self.stdout.write("")
        self.stdout.write(self.loading_instructions(name, output))

    @staticmethod
    def static_dirs():
        """Return the STATICFILES_DIRS entries as (prefix, directory) pairs."""
        entries = []
        for entry in getattr(settings, "STATICFILES_DIRS", []):
            prefix, directory = entry if isinstance(entry, (list, tuple)) else ("", entry)
            entries.append((prefix, Path(directory)))
        return entries

    def default_output(self, name):
        """The file to write when --output isn't given."""
        static_dirs = self.static_dirs()
        if static_dirs:
            return static_dirs[0][1] / "css" / "colors" / f"{name}.css"
        return Path(f"{name}.css")

    def confirm(self, prompt):
        """Ask the user to confirm. Without a terminal to ask, stop instead."""
        if not sys.stdin.isatty():
            raise CommandError(f"{prompt.split(' Replace')[0]} Use --force to replace it.")
        return input(prompt).strip().lower() in ("y", "yes")

    @staticmethod
    def package_color_notice(name):
        """Explain what writing values for one of the package's colors changes."""
        lines = [f"{name} is one of the package's colors. This file gives it new values, for every {name} class."]
        if name in ALIASES:
            lines.append(f"{name} is another name for {ALIASES[name]}, which keeps its own values.")
        else:
            other_names = [alias for alias, canonical in ALIASES.items() if canonical == name]
            if other_names:
                lines.append(
                    f"Its other {'names' if len(other_names) > 1 else 'name'}, {', '.join(other_names)}, "
                    f"{'change' if len(other_names) > 1 else 'changes'} too, unless you also generate values for "
                    f"{'them' if len(other_names) > 1 else 'it'}."
                )
        lines.append(f"To go back to the package's {name}, delete the file, or stop loading it.")
        return "\n".join(lines)

    def loading_instructions(self, name, output):
        """Explain where the file goes and how to load it."""
        static_path = None
        for prefix, directory in self.static_dirs():
            try:
                relative = output.resolve().relative_to(directory.resolve())
            except ValueError:
                continue
            static_path = "/".join(part for part in (prefix, relative.as_posix()) if part)
            break

        lines = []
        if static_path is None:
            static_path = f"css/colors/{output.name}"
            lines += [
                "The file isn't in one of your STATICFILES_DIRS directories. Move it into one, for example as",
                f"{static_path}, so that Django can serve it.",
                "",
            ]
        lines += [
            "To load it after the package's colors, add it to the styles_main_fixes__extra_colors block, in your",
            "project's templates/adminlte2/partials/_styles.html:",
            "",
            '    {% extends "adminlte2/partials/_styles.html" %}',
            "    {% load static %}",
            "",
            "    {% block styles_main_fixes__extra_colors %}",
            "      {{ block.super }}",
            f'      <link rel="stylesheet" href="{{% static \'{static_path}\' %}}">',
            "    {% endblock styles_main_fixes__extra_colors %}",
        ]
        if name not in NAMES:
            lines += [
                "",
                f"To show {name} on the demo CSS pages, add it to the ADMINLTE2_DEMO_CSS_COLORS setting.",
            ]
        return "\n".join(lines)
