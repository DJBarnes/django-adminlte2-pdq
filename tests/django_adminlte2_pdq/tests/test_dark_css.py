"""
Tests for the generated dark mode CSS.
"""

# System Imports.
import re

# Third-Party Imports.
from django.test import SimpleTestCase

# Internal Imports.
from adminlte2_pdq import color_css, dark_css


def _selectors(css_text):
    """Return every selector of every rule, including rules inside @media blocks."""
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    selectors = []
    for match in re.finditer(r"([^{};]+)\{[^{}]*\}", css_text):
        selectors += [selector.strip() for selector in match.group(1).split(",") if selector.strip()]
    return selectors


class DarkCssTestCase(SimpleTestCase):
    """Tests for adminlte2_pdq.dark_css and the CSS it generates."""

    def test__committed_css_matches_generator(self):
        """The committed CSS files are the generator's current output."""
        for file_name, render in dark_css.OUTPUTS.items():
            with self.subTest(file_name):
                committed = (dark_css.OUTPUT_DIR / file_name).read_text(encoding="utf-8")
                self.assertEqual(
                    committed,
                    render(),
                    f"{file_name} is out of date. Run: python -m adminlte2_pdq.dark_css",
                )

    def test__rules_only_apply_under_dark_skins(self):
        """Every selector requires a dark skin class, so the files change nothing in light mode."""
        for file_name, render in dark_css.OUTPUTS.items():
            selectors = _selectors(render())
            self.assertTrue(selectors)
            for selector in selectors:
                with self.subTest(file=file_name, selector=selector):
                    self.assertTrue(
                        selector.startswith(dark_css.DARK_SELECTOR)
                        or any(
                            re.search(rf"\.{skin_class}(?![\w-])", selector)
                            for skin_class in dark_css.DARK_SKIN_CLASSES
                        ),
                        selector,
                    )

    def test__skins_match_adminlte(self):
        """Each dark skin is AdminLTE's skin with only the class renamed."""
        rendered = dark_css.render_skins()
        for skin in dark_css.SKINS:
            with self.subTest(skin):
                adminlte = (dark_css.ADMINLTE_SKINS_DIR / f"skin-{skin}.css").read_text(encoding="utf-8")
                renamed = re.sub(rf"\.skin-{skin}(?![\w-])", f".skin-{skin}-dark", adminlte).strip()
                self.assertIn(renamed, rendered)

    def test__color_variables_are_redefined(self):
        """Dark mode sets the light-by-design variables for every color name, aliases included."""
        rendered = dark_css.render_dark_mode()
        self.assertNotIn(".pdq-dark", rendered)
        for name in color_css.NAMES:
            for part in ("light-accent", "light-accent-text", "table-hover"):
                with self.subTest(name=name, part=part):
                    self.assertIn(f"--pdq-{name}-{part}:", rendered)
        for name in ("default", "gray"):
            for part in ("text", "base", "active", "border", "hover"):
                with self.subTest(name=name, part=part):
                    self.assertIn(f"--pdq-{name}-{part}:", rendered)
