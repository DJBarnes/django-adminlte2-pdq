"""
Tests for the generated color CSS.
"""

# System Imports.
import re
from pathlib import Path

# Third-Party Imports.
from django.test import SimpleTestCase

# Internal Imports.
from adminlte2_pdq import color_css


STATIC_DIR = Path(color_css.__file__).resolve().parent / "static"
ADMINLTE_CSS = STATIC_DIR / "third-party" / "admin-lte" / "2.3.11" / "css" / "AdminLTE.css"
BOOTSTRAP_CSS = STATIC_DIR / "third-party" / "bootstrap" / "3.3.7" / "css" / "bootstrap.css"


def _parse_rules(css_text):
    """Return a list of (selectors, declarations) pairs for the top-level rules in a stylesheet."""
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    rules = []
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css_text):
        selectors = [selector.strip() for selector in match.group(1).split(",")]
        declarations = {}
        for declaration in match.group(2).split(";"):
            if ":" in declaration:
                prop, value = declaration.split(":", 1)
                declarations[prop.strip()] = value.replace("!important", "").strip().lower()
        rules.append((selectors, declarations))
    return rules


def _value_for(rules, selector, prop):
    """Return the last value AdminLTE sets for ``prop`` on exactly ``selector``."""
    value = None
    for selectors, declarations in rules:
        if selector in selectors and prop in declarations:
            value = declarations[prop]
    return value


def _normalize_hex(value):
    value = value.lstrip("#").lower()
    if len(value) == 3:
        value = "".join(character * 2 for character in value)
    return "#" + value


class ColorCssTestCase(SimpleTestCase):
    """Tests for adminlte2_pdq.color_css and the CSS it generates."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.adminlte_rules = _parse_rules(ADMINLTE_CSS.read_text(encoding="utf-8"))

    def test__committed_css_matches_generator(self):
        """The committed CSS files are the generator's current output."""
        for file_name, render in color_css.OUTPUTS.items():
            with self.subTest(file_name):
                committed = (color_css.OUTPUT_DIR / file_name).read_text(encoding="utf-8")
                self.assertEqual(
                    committed,
                    render(),
                    f"{file_name} is out of date. Run: python -m adminlte2_pdq.color_css",
                )

    def test__darken_matches_less(self):
        """darken() reproduces the values AdminLTE's LESS build produced."""
        for base, amount, expected in (
            ("#3c8dbc", 0.05, "#367fa9"),
            ("#00a65a", 0.05, "#008d4c"),
            ("#dd4b39", 0.10, "#c23321"),
            ("#0073b7", 0.10, "#005384"),
            ("#001f3f", 0.02, "#001a35"),
        ):
            with self.subTest(base=base, amount=amount):
                self.assertEqual(color_css.darken(base, amount), expected)

    def test__palette_matches_adminlte(self):
        """Base and active values equal AdminLTE's `.bg-{c}` and `.bg-{c}-active` for its palette."""
        for name in sorted(color_css.ADMINLTE_PALETTE):
            color = color_css._color_for(name)  # pylint: disable=protected-access
            with self.subTest(name):
                self.assertEqual(
                    _normalize_hex(color.base),
                    _normalize_hex(_value_for(self.adminlte_rules, f".bg-{name}", "background-color")),
                )
                self.assertEqual(
                    _normalize_hex(color.active),
                    _normalize_hex(_value_for(self.adminlte_rules, f".bg-{name}-active", "background-color")),
                )

    def test__derived_borders_match_adminlte(self):
        """hover and border equal AdminLTE's alert, button, callout, and modal borders."""
        for name in ("info", "success", "warning", "danger"):
            color = color_css._color_for(name)  # pylint: disable=protected-access
            with self.subTest(name):
                self.assertEqual(color.hover, _value_for(self.adminlte_rules, f".alert-{name}", "border-color"))
                self.assertEqual(color.hover, _value_for(self.adminlte_rules, f".btn-{name}", "border-color"))
                self.assertEqual(
                    color.border,
                    _value_for(self.adminlte_rules, f".callout.callout-{name}", "border-color"),
                )
                self.assertEqual(
                    color.border,
                    _value_for(self.adminlte_rules, f".modal-{name} .modal-header", "border-color"),
                )

    def test__stock_classes_are_not_redefined(self):
        """No generated component class is one that AdminLTE or Bootstrap already defines."""
        vendor_classes = set()
        for path in (ADMINLTE_CSS, BOOTSTRAP_CSS):
            vendor_classes |= set(re.findall(r"\.([a-zA-Z][\w-]*)", path.read_text(encoding="utf-8")))

        # Deliberate exception: lime uses dark text, which needs to override AdminLTE's white.
        allowed = {"bg-lime", "bg-lime-active"}

        generated = color_css.render_components()
        defined = set()
        for match in re.finditer(r"^\.(alert|btn|label|callout|box|modal)\.\1-([a-z-]+)(?= \{|,)", generated, re.M):
            defined.add(f"{match.group(1)}-{match.group(2)}")
        for match in re.finditer(r"^\.((?:bg|text)-[a-z-]+)(?= \{|,)", generated, re.M):
            defined.add(match.group(1))

        self.assertTrue(defined, "No component classes found in the generated CSS.")
        self.assertEqual(set(), (defined & vendor_classes) - allowed)

    def test__custom_color(self):
        """--custom prints variables and every component class for a new color."""
        color = color_css.Color("brand", base="#6610f2")
        css = color_css.render_custom_color(color)

        self.assertIn("--pdq-brand-base: #6610f2;", css)
        self.assertIn("--pdq-brand-active: #5b0cdd;", css)
        for selector in (".bg-brand {", ".btn.btn-brand {", ".label.label-brand {", ".tooltip.tooltip-brand"):
            self.assertIn(selector, css)

    def test__custom_color_rejects_invalid_names(self):
        """A custom color can't reuse a package color name or contain other characters."""
        for name in ("navy", "light-blue", "Brand", "my color"):
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    color_css.render_custom_color(color_css.Color(name, base="#6610f2"))
