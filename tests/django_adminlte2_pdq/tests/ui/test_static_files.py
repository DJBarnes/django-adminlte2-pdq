"""
Tests for the package's static files and the template references to them.
"""

# System Imports.
import re
from pathlib import Path

# Third-Party Imports.
from django.test import SimpleTestCase

# Internal Imports.
import adminlte2_pdq


# Found from the package itself, so the test doesn't depend on where this file sits.
PACKAGE_DIR = Path(adminlte2_pdq.__file__).resolve().parent
STATIC_DIR = PACKAGE_DIR / "static"
TEMPLATE_DIR = PACKAGE_DIR / "templates"
PDQ_STATIC_DIR = STATIC_DIR / "adminlte2_pdq"


class StaticFilesTestCase(SimpleTestCase):
    """Tests for files under adminlte2_pdq/static/adminlte2_pdq/."""

    def test__template_static_references_exist(self):
        """Every {% static %} path in the package templates exists in the package's static files.

        Paths under admin/ are Django admin's own static files, so they are not checked here.
        """
        pattern = re.compile(r"""{%\s*static\s+['"]((?!admin/)[^'"]+)['"]\s*%}""")
        templates = list(TEMPLATE_DIR.rglob("*.html"))
        self.assertTrue(templates, f"No templates found in {TEMPLATE_DIR}.")
        for template in templates:
            for path in pattern.findall(template.read_text(encoding="utf-8")):
                with self.subTest(template=str(template.relative_to(TEMPLATE_DIR)), path=path):
                    self.assertTrue((STATIC_DIR / path).is_file(), f"{path} does not exist.")

    def test__css_imports_exist(self):
        """Every @import in the package CSS points at a file that exists."""
        pattern = re.compile(r"""@import\s+["']([^"']+)["']""")
        stylesheets = list(PDQ_STATIC_DIR.rglob("*.css"))
        self.assertTrue(stylesheets, f"No stylesheets found in {PDQ_STATIC_DIR}.")
        for stylesheet in stylesheets:
            for path in pattern.findall(stylesheet.read_text(encoding="utf-8")):
                with self.subTest(stylesheet=str(stylesheet.relative_to(PDQ_STATIC_DIR)), path=path):
                    self.assertTrue((stylesheet.parent / path).resolve().is_file(), f"{path} does not exist.")
