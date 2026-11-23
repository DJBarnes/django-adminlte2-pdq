"""
Tests for the generate_color_css management command.
"""

# System Imports.
import io
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

# Third-Party Imports.
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings

# Internal Imports.
from adminlte2_pdq import generate_color_css


class GenerateColorCssCommandTestCase(SimpleTestCase):
    """Tests for the generate_color_css management command."""

    def setUp(self):
        super().setUp()
        self.directory = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(self.directory.cleanup)
        self.static_dir = Path(self.directory.name) / "static"

    def run_command(self, *args):
        """Run the command and return what it printed."""
        output = io.StringIO()
        call_command("generate_color_css", *args, stdout=output)
        return output.getvalue()

    def test__new_color(self):
        """A new color's file has its variables and every class, in the first static directory."""
        with override_settings(STATICFILES_DIRS=[str(self.static_dir)]):
            printed = self.run_command("brand", "#6610f2")

        css = (self.static_dir / "css" / "colors" / "brand.css").read_text(encoding="utf-8")
        self.assertEqual(css, generate_color_css.render_custom_color(generate_color_css.make_color("brand", "#6610f2")))
        self.assertIn("--pdq-brand-base: #6610f2;", css)
        self.assertIn(".btn.btn-brand {", css)
        self.assertIn(f"Wrote {self.static_dir / 'css' / 'colors' / 'brand.css'}", printed)
        self.assertIn("{% static 'css/colors/brand.css' %}", printed)
        self.assertIn("{% block styles_main_fixes__extra_colors %}", printed)
        self.assertIn("ADMINLTE2_DEMO_CSS_COLORS", printed)
        self.assertNotIn("one of the package's colors", printed)

    def test__options(self):
        """--active and the text options set those values."""
        output = self.static_dir / "brand.css"

        self.run_command("brand", "#6610f2", "--active", "#5b0cdd", "--dark-text", "--output", str(output))
        css = output.read_text(encoding="utf-8")
        self.assertIn("--pdq-brand-active: #5b0cdd;", css)
        self.assertIn(f"--pdq-brand-text: {generate_color_css.TEXT_DARK};", css)

        self.run_command("sky", "#87ceeb", "--light-text", "--output", str(output), "--force")
        self.assertIn(f"--pdq-sky-text: {generate_color_css.TEXT_LIGHT};", output.read_text(encoding="utf-8"))

    def test__package_color(self):
        """A package color's file has its variables only, and the command explains what it changes."""
        with override_settings(STATICFILES_DIRS=[str(self.static_dir)]):
            printed = self.run_command("info", "#7b2cbf")

        css = (self.static_dir / "css" / "colors" / "info.css").read_text(encoding="utf-8")
        self.assertIn("--pdq-info-base: #7b2cbf;", css)
        self.assertIn("--pdq-info-bootstrap-btn: #7b2cbf;", css)
        self.assertNotIn(".btn", css)
        self.assertIn("info is one of the package's colors.", printed)
        self.assertIn("Its other name, aqua, changes too", printed)
        self.assertIn("To go back to the package's info, delete the file, or stop loading it.", printed)
        self.assertNotIn("ADMINLTE2_DEMO_CSS_COLORS", printed)

    def test__package_color_names(self):
        """The notice names a color's other names, or the color an alternate name belongs to."""
        for name, expected in (
            ("danger", "Its other names, red, error, change too, unless you also generate values for them."),
            ("light-blue", "light-blue is another name for primary, which keeps its own values."),
            ("navy", "To go back to the package's navy"),
        ):
            with self.subTest(name=name):
                printed = self.run_command(name, "#7b2cbf", "--output", str(self.static_dir / f"{name}.css"))
                self.assertIn(expected, printed)

    def test__prefixed_static_dir(self):
        """A STATICFILES_DIRS entry with a prefix gives the file's static path that prefix."""
        with override_settings(STATICFILES_DIRS=[("project", str(self.static_dir))]):
            printed = self.run_command("brand", "#6610f2")

        self.assertIn("{% static 'project/css/colors/brand.css' %}", printed)

    def test__file_outside_static_dirs(self):
        """For a file outside the static directories, the command says to move it into one."""
        with override_settings(STATICFILES_DIRS=[str(self.static_dir)]):
            printed = self.run_command("brand", "#6610f2", "--output", str(Path(self.directory.name) / "brand.css"))

        self.assertIn("isn't in one of your STATICFILES_DIRS directories", printed)
        self.assertIn("{% static 'css/colors/brand.css' %}", printed)

    def test__no_static_dirs(self):
        """Without STATICFILES_DIRS, the file goes in the current directory."""
        cwd = os.getcwd()
        os.chdir(self.directory.name)
        self.addCleanup(os.chdir, cwd)

        with override_settings(STATICFILES_DIRS=[]):
            self.run_command("brand", "#6610f2")

        self.assertTrue((Path(self.directory.name) / "brand.css").exists())

    def test__existing_file(self):
        """An existing file is only replaced with --force, or when the user says yes."""
        output = self.static_dir / "brand.css"
        output.parent.mkdir(parents=True)
        output.write_text("old", encoding="utf-8")

        with patch("sys.stdin.isatty", return_value=False), self.assertRaisesMessage(CommandError, "--force"):
            self.run_command("brand", "#6610f2", "--output", str(output))
        self.assertEqual(output.read_text(encoding="utf-8"), "old")

        for answer, replaced in (("", False), ("n", False), ("y", True)):
            output.write_text("old", encoding="utf-8")
            with self.subTest(answer=answer):
                with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value=answer):
                    printed = self.run_command("brand", "#6610f2", "--output", str(output))
                self.assertEqual(output.read_text(encoding="utf-8") != "old", replaced)
                self.assertEqual("Nothing written." in printed, not replaced)

        output.write_text("old", encoding="utf-8")
        self.run_command("brand", "#6610f2", "--output", str(output), "--force")
        self.assertNotEqual(output.read_text(encoding="utf-8"), "old")

    def test__invalid_values(self):
        """Invalid names and colors are errors."""
        for args in (("Brand", "#6610f2"), ("brand", "purple"), ("brand", "#6610f2", "--active", "dark")):
            with self.subTest(args=args):
                with self.assertRaises(CommandError):
                    self.run_command(*args, "--output", str(self.static_dir / "brand.css"))
