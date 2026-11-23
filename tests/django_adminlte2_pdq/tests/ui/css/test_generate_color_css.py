"""
Tests for the generated color CSS.
"""

# System Imports.
import io
import re
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

# Third-Party Imports.
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

# Internal Imports.
from adminlte2_pdq import generate_color_css as color_css


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
    """Tests for adminlte2_pdq.generate_color_css and the CSS it generates."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.adminlte_rules = _parse_rules(ADMINLTE_CSS.read_text(encoding="utf-8"))

    def test__committed_css_matches_generator(self):
        """The committed CSS files are the generator's current output."""
        for file_name, render in color_css.OUTPUTS.items():
            with self.subTest(file=file_name):
                committed = (color_css.OUTPUT_DIR / file_name).read_text(encoding="utf-8")
                self.assertEqual(
                    committed,
                    render(),
                    f"{file_name} is out of date. Run: python -m adminlte2_pdq.generate_color_css",
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
            with self.subTest(name=name):
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
            with self.subTest(name=name):
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

    def test__stock_classes_use_the_variables(self):
        """The classes AdminLTE and Bootstrap define use the variables, with !important where AdminLTE uses it."""
        css = color_css.render_components()

        for rule in (
            # AdminLTE's palette, without the border the package's own colors add.
            ".bg-maroon {\n"
            "    color: var(--pdq-maroon-text) !important;\n"
            "    background-color: var(--pdq-maroon-base) !important;\n"
            "}",
            ".text-maroon {\n    color: var(--pdq-maroon-base) !important;\n}",
            ".bg-red-active {\n"
            "    color: var(--pdq-red-text) !important;\n"
            "    background-color: var(--pdq-red-active) !important;\n"
            "}",
            # AdminLTE's gray background is the only one whose text color isn't !important.
            ".bg-gray {\n    color: var(--pdq-gray-text);\n    background-color: var(--pdq-gray-base) !important;\n}",
            # AdminLTE's own selectors, so they tie with its other rules as before.
            ".label-danger {\n"
            "    color: var(--pdq-danger-text) !important;\n"
            "    background-color: var(--pdq-danger-base) !important;\n"
            "}",
            ".alert-error {\n"
            "    color: var(--pdq-error-text) !important;\n"
            "    background-color: var(--pdq-error-base) !important;\n"
            "    border-color: var(--pdq-error-hover);\n"
            "}",
            ".box.box-success {\n    border-top-color: var(--pdq-success-base);\n}",
            # Bootstrap's bg-{c} tint and text-{c} shade.
            ".bg-info {\n    background-color: var(--pdq-info-bootstrap-bg);\n}",
            ".bg-primary {\n"
            "    color: var(--pdq-primary-text);\n"
            "    background-color: var(--pdq-primary-bootstrap-bg);\n"
            "}",
            ".text-danger {\n    color: var(--pdq-danger-bootstrap-text);\n}",
            # AdminLTE's default box and label gray, and its default label isn't !important.
            ".box.box-default {\n    border-top-color: var(--pdq-default-box-label);\n}",
            ".label.label-default {\n"
            "    color: var(--pdq-default-text);\n"
            "    background-color: var(--pdq-default-box-label);\n"
            "}",
            # Bootstrap's table rows are its pale tint, header and footer rows included.
            ".table > thead > tr > td.info,",
        ):
            with self.subTest(rule=rule.split(" {")[0]):
                self.assertIn(rule, css)

    def test__package_colors_keep_their_border_and_header_rows(self):
        """The package's own colors color the border of bg-{c}, and their table header rows take the color itself."""
        css = color_css.render_components()

        self.assertIn(".bg-indigo {\n", css)
        self.assertIn("    border-color: var(--pdq-indigo-border);\n}", css)
        self.assertIn(
            ".table > thead > tr > td.indigo,",
            css.split("/* region table */")[1].split("background-color: var(--pdq-indigo-base)")[0],
        )

    def test__stock_buttons_repeat_bootstrap_and_adminlte_rules(self):
        """Each stock button has Bootstrap's and AdminLTE's rules, with the same selectors, in the same order."""
        bootstrap_rules = _parse_rules(BOOTSTRAP_CSS.read_text(encoding="utf-8"))
        generated_rules = _parse_rules(color_css.render_components())

        for name in sorted(color_css.SHIPPED["btn"]):
            with self.subTest(button=name):
                expected = [
                    selectors
                    for selectors, declarations in bootstrap_rules + self.adminlte_rules
                    if all(f"btn-{name}" in selector for selector in selectors)
                    and {"color", "background-color", "border-color"} & set(declarations)
                    and not any(".box" in selector or "user-footer" in selector for selector in selectors)
                ]
                generated = [
                    selectors
                    for selectors, _ in generated_rules
                    if all(f"btn-{name}" in selector for selector in selectors)
                    and not any(".box" in selector for selector in selectors)
                ]
                self.assertEqual(expected, generated)

    def test__bootstrap_shades_match_bootstrap(self):
        """The bootstrap-* variables of Bootstrap's colors are Bootstrap's compiled values."""
        bootstrap_rules = _parse_rules(BOOTSTRAP_CSS.read_text(encoding="utf-8"))

        def bootstrap(selector, prop):
            return _normalize_hex(_value_for(bootstrap_rules, selector, prop))

        for name in sorted(color_css.SHIPPED["btn"]):
            values = color_css.COLORS_BY_NAME[name].bootstrap_values()
            button = f".btn-{name}"
            expected = {
                "bootstrap-btn": bootstrap(button, "background-color"),
                "bootstrap-btn-border": bootstrap(button, "border-color"),
                "bootstrap-btn-text": bootstrap(button, "color"),
                "bootstrap-btn-hover": bootstrap(f"{button}:hover", "background-color"),
                "bootstrap-btn-hover-border": bootstrap(f"{button}:hover", "border-color"),
                "bootstrap-btn-focus-border": bootstrap(f"{button}:focus", "border-color"),
                "bootstrap-btn-pressed": bootstrap(f"{button}:active:hover", "background-color"),
            }
            if name in color_css.BOOTSTRAP_CONTEXTUAL:
                expected.update(
                    {
                        "bootstrap-bg": bootstrap(f".bg-{name}", "background-color"),
                        "bootstrap-bg-hover": bootstrap(f"a.bg-{name}:hover", "background-color"),
                        "bootstrap-text": bootstrap(f".text-{name}", "color"),
                        "bootstrap-text-hover": bootstrap(f"a.text-{name}:hover", "color"),
                    }
                )
            for part, value in expected.items():
                with self.subTest(color=name, part=part):
                    self.assertEqual(_normalize_hex(values[part]), value)

    def test__default_box_and_label_match_adminlte(self):
        """The default color's box-label value is AdminLTE's default box border and default label background."""
        box_label = color_css.COLORS_BY_NAME["default"].box_label

        self.assertEqual(box_label, _value_for(self.adminlte_rules, ".box.box-default", "border-top-color"))
        self.assertEqual(box_label, _value_for(self.adminlte_rules, ".label-default", "background-color"))

    def test__every_color_has_every_class(self):
        """Every color has every component class, and every AdminLTE and Bootstrap color its bg and text classes."""
        css = color_css.render_components()
        # A component class starts a selector: ".btn.btn-maroon {", ".btn-primary {", or ".modal-info .modal-body".
        component_class = (
            r"(?m)^\.(?:(?:alert|btn|label|callout|box|modal)\.)?((?:alert|btn|label|callout|box|modal)-[a-z-]+)[ ,]"
        )
        defined = set(re.findall(component_class, css))
        defined |= set(re.findall(r"(?m)^\.((?:bg|text)-[a-z-]+)(?= \{|,)", css))

        for name in color_css.NAMES:
            for component in ("alert", "btn", "label", "callout", "box", "modal", "bg", "text"):
                with self.subTest(color=name, component=component):
                    self.assertIn(f"{component}-{name}", defined)

    def test__modal_borders_come_after_the_alerts(self):
        """AdminLTE's modal header and footer borders still win on an alert that is also a modal header or footer."""
        css = color_css.render_components()

        self.assertLess(css.index(".alert-danger {"), css.index(".modal-footer {\n    border-top-color: #f4f4f4;\n}"))
        self.assertLess(
            css.index(".alert-danger {"), css.index(".modal-header {\n    border-bottom-color: #f4f4f4;\n}")
        )

    def test__consistent_colors_use_each_colors_own_shades(self):
        """consistent-colors.css points Bootstrap's shades at the color's AdminLTE shades."""
        css = color_css.render_consistent_colors()

        for line in (
            "--pdq-primary-bootstrap-btn: var(--pdq-primary-base);",
            "--pdq-primary-bootstrap-btn-border: var(--pdq-primary-hover);",
            "--pdq-danger-bootstrap-btn-focus-border: var(--pdq-danger-border);",
            "--pdq-info-bootstrap-btn-pressed: var(--pdq-info-hover);",
            # AdminLTE's default button border is the default color's border shade.
            "--pdq-default-bootstrap-btn-border: var(--pdq-default-border);",
            # Default boxes and labels take the edge of the default button, so default stays apart from gray.
            "--pdq-default-box-label: var(--pdq-default-border);",
        ):
            with self.subTest(line=line):
                self.assertIn(f"    {line}\n", css)
        for name in sorted(color_css.SHIPPED["btn"]):
            for part in color_css.CONSISTENT_BUTTON_PARTS:
                with self.subTest(color=name, part=part):
                    self.assertIn(f"    --pdq-{name}-{part}: var(--pdq-{name}-", css)

    def test__consistent_colors_draw_bootstrap_classes_like_adminlte(self):
        """bg-{c} and text-{c} of Bootstrap's colors are drawn like AdminLTE's names for them, and table header rows
        take the color itself."""
        css = color_css.render_consistent_colors()

        for rule in (
            ".bg-info {\n"
            "    color: var(--pdq-info-text) !important;\n"
            "    background-color: var(--pdq-info-base) !important;\n"
            "}",
            ".bg-danger-active {\n"
            "    color: var(--pdq-danger-text) !important;\n"
            "    background-color: var(--pdq-danger-active) !important;\n"
            "}",
            ".text-success {\n    color: var(--pdq-success-base) !important;\n}",
        ):
            with self.subTest(rule=rule.split(" {")[0]):
                self.assertIn(rule, css)
        for name in sorted(color_css.BOOTSTRAP_TABLE_ROWS):
            with self.subTest(table_row=name):
                self.assertIn(f".table > thead > tr > td.{name},", css)
                self.assertIn(f"    background-color: var(--pdq-{name}-base) !important;\n", css)

    def test__custom_color(self):
        """--custom prints variables and every component class for a new color."""
        color = color_css.Color("brand", base="#6610f2")
        css = color_css.render_custom_color(color)

        self.assertIn("--pdq-brand-base: #6610f2;", css)
        self.assertIn("--pdq-brand-active: #5b0cdd;", css)
        for selector in (".bg-brand {", ".btn.btn-brand {", ".label.label-brand {", ".tooltip.tooltip-brand"):
            self.assertIn(selector, css)

    def test__custom_color_rejects_package_names(self):
        """render_custom_color is for new colors only. Package colors get render_color_override."""
        for name in ("navy", "light-blue"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    color_css.render_custom_color(color_css.Color(name, base="#6610f2"))
        with self.assertRaises(ValueError):
            color_css.render_color_override(color_css.Color("brand", base="#6610f2"))

    def test__make_color_rejects_invalid_values(self):
        """make_color only takes lowercase names of letters, digits, and hyphens, and hex colors."""
        for name, base, active in (
            ("Brand", "#6610f2", None),
            ("my color", "#6610f2", None),
            ("1brand", "#6610f2", None),
            ("brand", "6610f2", None),
            ("brand", "#6610f", None),
            ("brand", "#6610f2", "dark"),
        ):
            with self.subTest(name=name, base=base, active=active):
                with self.assertRaises(ValueError):
                    color_css.make_color(name, base, active=active)

    def test__make_color_text(self):
        """make_color picks dark or white text, whichever is easier to read, unless told which."""
        for base, dark_text, expected in (
            ("#87ceeb", None, color_css.TEXT_DARK),
            ("#6610f2", None, color_css.TEXT_LIGHT),
            ("#6610f2", True, color_css.TEXT_DARK),
            ("#87ceeb", False, color_css.TEXT_LIGHT),
        ):
            with self.subTest(base=base, dark_text=dark_text):
                self.assertEqual(color_css.make_color("brand", base, dark_text=dark_text).text, expected)

    def test__make_color_follows_the_new_color(self):
        """For a Bootstrap color, make_color derives Bootstrap's shades from the new color, not Bootstrap's."""
        info = color_css.make_color("info", "#7b2cbf")
        values = info.bootstrap_values()

        self.assertEqual(values["bootstrap-btn"], info.base)
        self.assertEqual(values["bootstrap-btn-border"], info.hover)
        self.assertEqual(values["bootstrap-btn-hover"], info.hover)
        self.assertEqual(values["bootstrap-btn-focus-border"], info.border)
        self.assertEqual(values["bootstrap-bg"], info.light_accent)
        self.assertEqual(values["bootstrap-text"], color_css.dark_shade(info.base))
        self.assertEqual(color_css.make_color("primary", "#7b2cbf").bootstrap_values()["bootstrap-bg"], "#7b2cbf")

        default = color_css.make_color("default", "#eeeeee")
        self.assertEqual(default.box_label, default.border)
        self.assertEqual(default.bootstrap_values()["bootstrap-btn-border"], default.border)
        self.assertEqual(color_css.make_color("brand", "#6610f2").bootstrap_values(), {})

    def test__gray_tints_stay_gray(self):
        """A gray's light tints are gray too."""
        color = color_css.make_color("stone", "#eeeeee")

        for tint in (color.light_accent, color.table_hover):
            with self.subTest(tint=tint):
                self.assertEqual(len(set(color_css.hex_to_rgb(tint))), 1)

    def test__color_override(self):
        """New values for a package color are its variables only, with Bootstrap's shades for Bootstrap's colors."""
        info = color_css.render_color_file(color_css.make_color("info", "#7b2cbf"))
        alias = color_css.render_color_file(color_css.make_color("light-blue", "#87ceeb"))

        self.assertIn("--pdq-info-base: #7b2cbf;", info)
        self.assertIn("--pdq-info-bootstrap-btn: #7b2cbf;", info)
        self.assertNotIn("{\n    color", info)
        self.assertIn("--pdq-light-blue-base: #87ceeb;", alias)
        self.assertNotIn("bootstrap", alias.split(":root")[1])

    def test__light_tints_keep_text_readable(self):
        """Code text stays readable on each light tint, and table text on each hover tint."""

        def contrast(first, second):
            lighter, darker = sorted((color_css.relative_luminance(first), color_css.relative_luminance(second)))[::-1]
            return (lighter + 0.05) / (darker + 0.05)

        for color in color_css.COLORS:
            with self.subTest(color=color.name):
                self.assertGreaterEqual(contrast(color.light_accent, color_css.LIGHT_ACCENT_TEXT), 4.5)
                self.assertGreaterEqual(contrast(color.table_hover, color_css.TABLE_BODY_TEXT), 4.5)

    def test__light_tints_stay_apart(self):
        """No two colors have nearly the same light tint, including colors that share a hue."""

        def rgb(value):
            return [int(value[i : i + 2], 16) for i in (1, 3, 5)]

        colors = color_css.COLORS
        for index, first in enumerate(colors):
            for second in colors[index + 1 :]:
                with self.subTest(first=first.name, second=second.name):
                    distance = (
                        sum((a - b) ** 2 for a, b in zip(rgb(first.light_accent), rgb(second.light_accent))) ** 0.5
                    )
                    self.assertGreaterEqual(distance, 12, (first.light_accent, second.light_accent))

    def test__main__writes_the_css_files(self):
        """Run without arguments, the command writes each generated file."""
        with tempfile.TemporaryDirectory() as output_dir, patch.object(color_css, "OUTPUT_DIR", Path(output_dir)):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(color_css.main([]), 0)
            for file_name, render in color_css.OUTPUTS.items():
                with self.subTest(file=file_name):
                    self.assertEqual((Path(output_dir) / file_name).read_text(encoding="utf-8"), render())

    def test__main__takes_no_arguments(self):
        """The module only writes the package's files. Projects use the generate_color_css command."""
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            color_css.main(["--custom", "brand", "#6610f2"])


class ColorStylesheetsTestCase(TestCase):
    """Which color stylesheets a page loads, and in which order."""

    def test__loaded_before_dark_mode(self):
        """The page loads extra-colors.css after the color variables, and before dark mode, which restyles it."""
        content = self.client.get(reverse("adminlte2_pdq:home")).content.decode()

        variables = content.index("adminlte2_pdq/css/extra-colors/color-variables.css")
        extra_colors = content.index("adminlte2_pdq/css/extra-colors/extra-colors.css")
        dark_mode = content.index("adminlte2_pdq/css/dark-mode/dark-mode.css")
        self.assertLess(variables, extra_colors)
        self.assertLess(extra_colors, dark_mode)

    def test__consistent_colors_not_loaded_by_default(self):
        """Without ADMINLTE2_CONSISTENT_COLORS, the page doesn't load consistent-colors.css."""
        response = self.client.get(reverse("adminlte2_pdq:home"))

        self.assertNotContains(response, "adminlte2_pdq/css/extra-colors/consistent-colors.css")

    @override_settings(ADMINLTE2_CONSISTENT_COLORS=True)
    def test__consistent_colors_loaded_before_dark_mode(self):
        """With ADMINLTE2_CONSISTENT_COLORS, the page loads consistent-colors.css after extra-colors.css and before
        dark mode."""
        content = self.client.get(reverse("adminlte2_pdq:home")).content.decode()

        extra_colors = content.index("adminlte2_pdq/css/extra-colors/extra-colors.css")
        consistent_colors = content.index("adminlte2_pdq/css/extra-colors/consistent-colors.css")
        dark_mode = content.index("adminlte2_pdq/css/dark-mode/dark-mode.css")
        self.assertLess(extra_colors, consistent_colors)
        self.assertLess(consistent_colors, dark_mode)
