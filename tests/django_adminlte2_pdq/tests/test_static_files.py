"""
Tests for the package's static files and the template references to them.
"""

# System Imports.
import re
from pathlib import Path

# Third-Party Imports.
from django.test import SimpleTestCase


PACKAGE_DIR = Path(__file__).resolve().parents[3] / "adminlte2_pdq"
STATIC_DIR = PACKAGE_DIR / "static"
TEMPLATE_DIR = PACKAGE_DIR / "templates"
PDQ_STATIC_DIR = STATIC_DIR / "adminlte2_pdq"

# Old paths kept for templates that still link them, mapped to the current file.
# JavaScript can't import other files, so each old path is a copy of the current file.
DEPRECATED_JS_COPIES = {
    "extra-features/extra-features.js": "js/extra-features/extra-features.js",
    "extra-features/header-breadcrumb-overlap-fix.js": "js/extra-features/header_breadcrumb_overlap_fix.js",
    "extra-features/sidebar-state.js": "js/extra-features/sidebar-state.js",
    "conflicts/conflicts.js": "js/conflicts/conflicts.js",
}
DEPRECATED_CSS_STUBS = [
    "extra-features/extra-features.css",
    "extra-features/header-breadcrumb-overlap-fix.css",
    "conflicts/conflicts.css",
    "conflicts/django-admin-conflicts.css",
]


class StaticFilesTestCase(SimpleTestCase):
    """Tests for files under adminlte2_pdq/static/adminlte2_pdq/."""

    def test__template_static_references_exist(self):
        """Every {% static %} path in the package templates exists in the package's static files.

        Paths under admin/ are Django admin's own static files, so they are not checked here.
        """
        pattern = re.compile(r"""{%\s*static\s+['"]((?!admin/)[^'"]+)['"]\s*%}""")
        for template in TEMPLATE_DIR.rglob("*.html"):
            for path in pattern.findall(template.read_text(encoding="utf-8")):
                with self.subTest(template=str(template.relative_to(TEMPLATE_DIR)), path=path):
                    self.assertTrue((STATIC_DIR / path).is_file(), f"{path} does not exist.")

    def test__css_imports_exist(self):
        """Every @import in the package CSS points at a file that exists."""
        pattern = re.compile(r"""@import\s+["']([^"']+)["']""")
        for stylesheet in PDQ_STATIC_DIR.rglob("*.css"):
            for path in pattern.findall(stylesheet.read_text(encoding="utf-8")):
                with self.subTest(stylesheet=str(stylesheet.relative_to(PDQ_STATIC_DIR)), path=path):
                    self.assertTrue((stylesheet.parent / path).resolve().is_file(), f"{path} does not exist.")

    def test__deprecated_css_paths_are_import_stubs(self):
        """Old CSS paths still exist and only import their replacements."""
        for old_path in DEPRECATED_CSS_STUBS:
            with self.subTest(old_path):
                content = re.sub(r"/\*.*?\*/", "", (PDQ_STATIC_DIR / old_path).read_text(encoding="utf-8"), flags=re.S)
                statements = [line.strip() for line in content.splitlines() if line.strip()]
                self.assertTrue(statements)
                for statement in statements:
                    self.assertTrue(statement.startswith("@import "), statement)

    def test__deprecated_js_paths_match_current_files(self):
        """Old JavaScript paths are exact copies of the current files."""
        for old_path, new_path in DEPRECATED_JS_COPIES.items():
            with self.subTest(old_path):
                self.assertEqual(
                    (PDQ_STATIC_DIR / old_path).read_text(encoding="utf-8"),
                    (PDQ_STATIC_DIR / new_path).read_text(encoding="utf-8"),
                    f"Copy {new_path} to {old_path}.",
                )
