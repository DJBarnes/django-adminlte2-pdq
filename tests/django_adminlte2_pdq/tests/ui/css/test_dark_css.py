"""
Tests for the generated dark mode CSS.
"""

# System Imports.
import io
import re
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

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

    def test__dark_text_soft_matches_the_palette(self):
        """The soft text color the tints are checked against is the palette's --pdq-dark-text-soft."""
        source = dark_css.SOURCE_FILE.read_text(encoding="utf-8")
        self.assertIn(f"--pdq-dark-text-soft: {dark_css.DARK_TEXT_SOFT};", source)

    def test__dark_tints_keep_text_readable_and_a_hover_step(self):
        """Every computed dark tint keeps the soft text readable, and its hover tint is a different color."""
        for name in color_css.NAMES:
            base = color_css.COLORS_BY_NAME[color_css.ALIASES.get(name, name)].base
            tint, hover = dark_css.dark_tint(base), dark_css.dark_tint(base, hover=True)
            with self.subTest(name):
                self.assertGreaterEqual(dark_css._contrast(tint, dark_css.DARK_TEXT_SOFT), dark_css.TINT_MIN_CONTRAST)
                self.assertGreaterEqual(dark_css._contrast(hover, dark_css.DARK_TEXT_SOFT), dark_css.TINT_MIN_CONTRAST)
                self.assertNotEqual(tint, hover)

    def test__dark_tints_of_colors_with_one_hue_stay_apart(self):
        """Navy, blue, and primary share a hue; their dark tints still differ visibly."""
        tints = {name: dark_css.dark_tint(color_css.COLORS_BY_NAME[name].base) for name in ("navy", "blue", "primary")}
        rgb = {name: [int(value[i : i + 2], 16) for i in (1, 3, 5)] for name, value in tints.items()}
        for first, second in (("navy", "blue"), ("blue", "primary"), ("navy", "primary")):
            with self.subTest(f"{first} and {second}"):
                distance = sum((a - b) ** 2 for a, b in zip(rgb[first], rgb[second])) ** 0.5
                self.assertGreaterEqual(distance, 15, tints)

    def test__main__writes_the_css_files(self):
        """The command writes each generated file."""
        with tempfile.TemporaryDirectory() as output_dir, patch.object(dark_css, "OUTPUT_DIR", Path(output_dir)):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(dark_css.main(), 0)
            for file_name, render in dark_css.OUTPUTS.items():
                with self.subTest(file_name):
                    self.assertEqual((Path(output_dir) / file_name).read_text(encoding="utf-8"), render())
