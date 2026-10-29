"""
Generator for the package's extra color CSS.

Writes two files:

* ``css/extra-colors/color-variables.css``: one set of CSS custom properties per color.
* ``css/extra-colors/extra-colors.css``: the per-color component rules, using those properties.

Rules are only emitted where AdminLTE 2.3.11 or Bootstrap 3.3.7 does not already style
the class, so stock components keep their stock look.

Run from the repository root after changing this file:

    python -m adminlte2_pdq.color_css

The generated files are committed. A test fails when they are out of date.
"""

# System Imports.
import argparse
import colorsys
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# region Color math


def hex_to_rgb(value):
    """Convert "#rrggbb" or "#rgb" to a tuple of floats in the 0-1 range."""
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(character * 2 for character in value)
    return tuple(int(value[index : index + 2], 16) / 255 for index in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert a tuple of floats in the 0-1 range to "#rrggbb"."""
    # Round halves up, as LESS does. Python's round() rounds halves to even.
    return "#" + "".join(f"{int(channel * 255 + 0.5):02x}" for channel in rgb)


def darken(value, amount):
    """Darken a color the way LESS ``darken()`` does: reduce HSL lightness by ``amount`` (0-1)."""
    hue, lightness, saturation = colorsys.rgb_to_hls(*hex_to_rgb(value))
    return rgb_to_hex(colorsys.hls_to_rgb(hue, max(0.0, lightness - amount), saturation))


def light_tint(value, hover=False):
    """A pale tint of a color, for code and table body rows.

    Keeps the color's hue and part of its own lightness and saturation (lightness 78% plus a tenth of its own,
    saturation 20% plus 40% of its own), so colors that share a hue, such as navy, blue, and primary, stay apart.
    The hover tint is 8% darker.
    """
    hue, lightness, saturation = colorsys.rgb_to_hls(*hex_to_rgb(value))
    tint_lightness = 0.78 + 0.10 * lightness - (0.08 if hover else 0)
    return rgb_to_hex(colorsys.hls_to_rgb(hue, tint_lightness, 0.20 + 0.40 * saturation))


def relative_luminance(value):
    """WCAG relative luminance of a color."""

    def channel(component):
        return component / 12.92 if component <= 0.03928 else ((component + 0.055) / 1.055) ** 2.4

    red, green, blue = (channel(component) for component in hex_to_rgb(value))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


# endregion Color math


# region Palette

TEXT_LIGHT = "#fff"
TEXT_DARK = "#444"
LIGHT_ACCENT_TEXT = TEXT_DARK
TABLE_BODY_TEXT = "#333"

# Backgrounds darker than this get light close buttons and icon tints.
DARK_BACKGROUND_LUMINANCE = 0.05


@dataclass
class Color:
    """A color and the values derived from it.

    ``base``, ``active``, and ``text`` match AdminLTE for every color AdminLTE defines.
    ``border`` (darken 10%) is AdminLTE's callout and modal border. ``hover`` (darken 5%) is
    AdminLTE's button border, button hover, and alert border. ``light_accent`` and
    ``table_hover`` are pale tints used by code and table rows. Values left out are derived
    from ``base``.
    """

    name: str
    base: str
    active: str = None
    light_accent: str = None
    table_hover: str = None
    text: str = TEXT_LIGHT
    border: str = None
    hover: str = None

    def __post_init__(self):
        if self.active is None:
            self.active = darken(self.base, 0.05)
        if self.light_accent is None:
            self.light_accent = light_tint(self.base)
        if self.table_hover is None:
            self.table_hover = light_tint(self.base, hover=True)
        if self.border is None:
            self.border = darken(self.base, 0.10)
        if self.hover is None:
            self.hover = darken(self.base, 0.05)

    @property
    def has_dark_text(self):
        """True when text on this color is dark instead of white."""
        return self.text != TEXT_LIGHT

    @property
    def has_dark_background(self):
        """True when this color is dark enough that AdminLTE's dark overlays disappear."""
        return relative_luminance(self.base) < DARK_BACKGROUND_LUMINANCE


COLORS = [
    Color(
        "default",
        base="#f4f4f4",
        active="#e7e7e7",
        hover="#e7e7e7",
        border="#ddd",
        text=TEXT_DARK,
        light_accent="#f7f7f7",
        table_hover="#f2f2f2",
    ),
    Color("primary", base="#3c8dbc", active="#357ca5"),
    Color("info", base="#00c0ef", active="#00a7d0", light_accent="#d9edf7", table_hover="#c4e3f3"),
    Color("success", base="#00a65a", active="#008d4c", light_accent="#dff0d8", table_hover="#d0e9c6"),
    Color("warning", base="#f39c12", active="#db8b0b", light_accent="#fcf8e3", table_hover="#faf2cc"),
    Color("danger", base="#dd4b39", active="#d33724", light_accent="#f2dede", table_hover="#ebcccc"),
    Color("navy", base="#001f3f", active="#001a35"),
    Color("blue", base="#0073b7", active="#005384"),
    Color("teal", base="#39cccc", active="#30bbbb"),
    Color("olive", base="#3d9970", active="#368763"),
    Color(
        "lime",
        base="#01ff70",
        active="#00e765",
        text=TEXT_DARK,
    ),
    Color("orange", base="#ff851b", active="#ff7701"),
    Color("fuchsia", base="#f012be", active="#db0ead"),
    Color("purple", base="#605ca8", active="#555299"),
    Color("maroon", base="#d81b60", active="#ca195a"),
    Color("black", base="#111111", active="#000000", light_accent="#cccccc", table_hover="#cccccc"),
    Color(
        "gray",
        base="#d2d6de",
        active="#b5bbc8",
        text="#000",
        light_accent="#dfe3eb",
        table_hover="#bdc8de",
    ),
    Color(
        "indigo",
        base="#a35cd8",
        active="#9a52d2",
        border="#8d4bbf",
    ),
]

COLORS_BY_NAME = {color.name: color for color in COLORS}

# Alternate names. Each alias gets its own variables and classes, pointing at the named color.
ALIASES = {
    "light-blue": "primary",
    "aqua": "info",
    "green": "success",
    "yellow": "warning",
    "red": "danger",
    "error": "danger",
}

# Every class name the generator handles, in output order.
NAMES = [
    "default",
    "primary",
    "light-blue",
    "info",
    "aqua",
    "success",
    "green",
    "warning",
    "yellow",
    "danger",
    "red",
    "error",
    "navy",
    "blue",
    "teal",
    "olive",
    "lime",
    "orange",
    "fuchsia",
    "purple",
    "maroon",
    "black",
    "gray",
    "indigo",
]

# AdminLTE's `.bg-{c}`, `.bg-{c}-active`, and `.text-{c}` palette.
ADMINLTE_PALETTE = {
    "light-blue",
    "aqua",
    "green",
    "yellow",
    "red",
    "navy",
    "blue",
    "teal",
    "olive",
    "lime",
    "orange",
    "fuchsia",
    "purple",
    "maroon",
    "black",
    "gray",
}
# Bootstrap's contextual `.bg-{c}`, `.text-{c}`, and table row classes.
BOOTSTRAP_CONTEXTUAL = {"primary", "info", "success", "warning", "danger"}

# AdminLTE's name for each Bootstrap contextual color, for `bg-{c}` classes.
BG_NAMES = {"primary": "light-blue", "info": "aqua", "success": "green", "warning": "yellow", "danger": "red"}

# Component classes that AdminLTE or Bootstrap already ships, per component.
SHIPPED = {
    "bg": ADMINLTE_PALETTE | BOOTSTRAP_CONTEXTUAL,
    # Bootstrap's `.bg-{c}` for contextual names is a pale tint, so no `-active` variant is added.
    "bg-active": ADMINLTE_PALETTE | BOOTSTRAP_CONTEXTUAL,
    "text": ADMINLTE_PALETTE | BOOTSTRAP_CONTEXTUAL,
    "box": {"default", "primary", "info", "success", "warning", "danger"},
    "btn": {"default", "primary", "info", "success", "warning", "danger"},
    "alert": {"info", "success", "warning", "danger", "error"},
    "callout": {"info", "success", "warning", "danger"},
    "label": {"default", "primary", "info", "success", "warning", "danger"},
    "modal": {"primary", "info", "success", "warning", "danger"},
    "table-row": {"info", "success", "warning", "danger"},
}

# AdminLTE's text color on `.bg-{c}` for its own palette. Only `gray` differs from white.
ADMINLTE_BG_TEXT = {"gray": "#000"}

# endregion Palette


# region Rendering


def _color_for(name):
    """Return the Color for a class name, following aliases."""
    return COLORS_BY_NAME[ALIASES.get(name, name)]


VARIABLE_PARTS = ("text", "base", "active", "border", "hover", "light-accent", "light-accent-text", "table-hover")


def _variable_lines(color):
    """Return the CSS custom property declarations for one color."""
    values = {
        "text": color.text,
        "base": color.base,
        "active": color.active,
        "border": color.border,
        "hover": color.hover,
        "light-accent": color.light_accent,
        "light-accent-text": LIGHT_ACCENT_TEXT,
        "table-hover": color.table_hover,
    }
    return [f"    --pdq-{color.name}-{part}: {values[part]};" for part in VARIABLE_PARTS]


def _var(name, part):
    return f"var(--pdq-{name}-{part})"


def _rule(selectors, declarations):
    """Render one CSS rule."""
    if isinstance(selectors, str):
        selectors = [selectors]
    lines = [",\n".join(selectors) + " {"]
    lines += [f"    {declaration};" for declaration in declarations]
    lines.append("}")
    return "\n".join(lines)


def _ships(component, name):
    return name in SHIPPED.get(component, set())


def render_variables():
    """Render the CSS custom properties for every color and alias."""
    parts = [
        "/**",
        " * AdminLTE PDQ color variables.",
        " *",
        " * GENERATED by adminlte2_pdq/color_css.py. Do not edit by hand.",
        " *",
        " * To change a color for your project, redefine its variables in your own CSS,",
        " * loaded after this file. For example:",
        " *",
        " *     :root { --pdq-indigo-base: #6610f2; }",
        " */",
        "",
        "",
        ":root {",
        f"    --pdq-table-body-text: {TABLE_BODY_TEXT};",
    ]
    for name in NAMES:
        if name in ALIASES:
            canonical = ALIASES[name]
            parts.append(f"    /* {name}: alias of {canonical}. */")
            parts += [f"    --pdq-{name}-{part}: var(--pdq-{canonical}-{part});" for part in VARIABLE_PARTS]
        else:
            parts.append(f"    /* {name} */")
            parts += _variable_lines(_color_for(name))
    parts.append("}")
    return "\n".join(parts) + "\n"


def _component_rules(name, color=None):  # pylint: disable=too-many-statements
    """Yield (component, rule) pairs for one class name."""
    color = color or _color_for(name)
    text, base, active = _var(name, "text"), _var(name, "base"), _var(name, "active")
    border, hover = _var(name, "border"), _var(name, "hover")
    light_accent, light_accent_text = _var(name, "light-accent"), _var(name, "light-accent-text")
    table_hover = _var(name, "table-hover")

    # Background, background-active, and text utilities.
    if not _ships("bg", name):
        yield "background", _rule(
            f".bg-{name}",
            [f"color: {text} !important", f"background-color: {base} !important", f"border-color: {border}"],
        )
    elif name in ADMINLTE_PALETTE and color.text != ADMINLTE_BG_TEXT.get(name, TEXT_LIGHT):
        # AdminLTE's text color on this background is not readable. Override it.
        yield "background", _rule([f".bg-{name}", f".bg-{name}-active"], [f"color: {text} !important"])
    if not _ships("bg-active", name):
        yield "background", _rule(
            f".bg-{name}-active",
            [f"color: {text} !important", f"background-color: {active} !important"],
        )
    if not _ships("text", name):
        # `.text-default` uses the default text color; the default base is too light to read.
        text_value = text if name == "default" else base
        yield "text", _rule(f".text-{name}", [f"color: {text_value} !important"])

    # Code tint.
    yield "code", _rule(
        f"code.code-{name}",
        [f"color: {light_accent_text}", f"background-color: {light_accent}"],
    )

    # Alert.
    if not _ships("alert", name):
        yield "alert", _rule(
            f".alert.alert-{name}",
            [f"color: {text}", f"background-color: {base}", f"border-color: {hover}"],
        )
        if color.has_dark_text:
            yield "alert", _rule(f".alert.alert-{name} a", [f"color: {text}"])
    if color.has_dark_background:
        yield "alert", _rule(f".alert.alert-{name} .close", ["color: #fff"])

    # Box.
    if not _ships("box", name):
        yield "box", _rule(f".box.box-{name}", [f"border-top-color: {base}"])
        yield "box", _rule(f".box.box-solid.box-{name}", [f"border: 1px solid {base}"])
        yield "box", _rule(
            f".box.box-solid.box-{name} > .box-header",
            [f"color: {text}", f"background: {base}", f"background-color: {base}"],
        )
        yield "box", _rule(
            [f".box.box-solid.box-{name} > .box-header a", f".box.box-solid.box-{name} > .box-header .btn"],
            [f"color: {text}"],
        )

    # Button. States follow Bootstrap's button-variant mixin, with AdminLTE's colors.
    if not _ships("btn", name):
        yield "button", _rule(
            f".btn.btn-{name}",
            [f"color: {text}", f"background-color: {base}", f"border-color: {hover}"],
        )
        state_selectors = [
            f".btn.btn-{name}:focus",
            f".btn.btn-{name}.focus",
            f".btn.btn-{name}:hover",
            f".btn.btn-{name}.hover",
            f".btn.btn-{name}:active",
            f".btn.btn-{name}.active",
            f".open > .dropdown-toggle.btn.btn-{name}",
        ]
        yield "button", _rule(
            state_selectors,
            [f"color: {text}", f"background-color: {hover}", f"border-color: {border}"],
        )
        yield "button", _rule(
            [
                f".btn.btn-{name}.disabled",
                f".btn.btn-{name}[disabled]",
                f"fieldset[disabled] .btn.btn-{name}",
                f".btn.btn-{name}.disabled:hover",
                f".btn.btn-{name}[disabled]:hover",
                f"fieldset[disabled] .btn.btn-{name}:hover",
                f".btn.btn-{name}.disabled:focus",
                f".btn.btn-{name}[disabled]:focus",
                f"fieldset[disabled] .btn.btn-{name}:focus",
            ],
            [f"background-color: {base}", f"border-color: {hover}"],
        )
        yield "button", _rule(f".btn.btn-{name} .badge", [f"color: {base}", f"background-color: {text}"])
        # Keep the button's own colors inside solid box headers, which recolor every `.btn`.
        yield "button", _rule(f".box.box-solid > .box-header .btn.btn-{name}", [f"color: {text}"])
        yield "button", _rule(
            [
                f".box.box-solid > .box-header .btn.btn-{name}:hover",
                f".box.box-solid > .box-header .btn.btn-{name}:focus",
            ],
            [f"background-color: {hover}"],
        )
    elif name in BOOTSTRAP_CONTEXTUAL:
        # AdminLTE darkens every `.btn` in a solid box header on hover, which hides the hover
        # color of its own colored buttons. Restore it.
        yield "button", _rule(f".box.box-solid > .box-header .btn.btn-{name}", [f"color: {text}"])
        yield "button", _rule(
            [
                f".box.box-solid > .box-header .btn.btn-{name}:hover",
                f".box.box-solid > .box-header .btn.btn-{name}:focus",
            ],
            [f"background-color: {hover}"],
        )

    # Callout.
    if not _ships("callout", name):
        yield "callout", _rule(
            f".callout.callout-{name}",
            [f"color: {text}", f"background-color: {base}", f"border-color: {border}"],
        )
        if color.has_dark_text:
            yield "callout", _rule(f".callout.callout-{name} a", [f"color: {text}"])

    # Carousel. `.carousel-{c}` colors the controls, caption, and indicators.
    yield "carousel", _rule(
        [
            f".carousel.bg-{name} .carousel-indicators li:active",
            f".carousel.bg-{name} .carousel-indicators li:focus",
            f".carousel.bg-{name} .carousel-indicators li:hover",
        ],
        [f"background-color: {border}"],
    )
    yield "carousel", _rule(
        [
            f".carousel.carousel-{name} .carousel-control",
            f".carousel.carousel-{name} .carousel-caption",
            f".carousel.carousel-{name} .carousel-indicators li",
        ],
        [f"color: {base}", f"border-color: {base}"],
    )
    yield "carousel", _rule(
        [
            f".carousel.carousel-{name} .carousel-indicators li.active",
            f".carousel.carousel-{name} .carousel-indicators li:active",
        ],
        [f"background-color: {base}", f"border-color: {border}"],
    )
    yield "carousel", _rule(
        [
            f".carousel.carousel-{name} .carousel-indicators li:focus",
            f".carousel.carousel-{name} .carousel-indicators li:hover",
        ],
        [f"background-color: {border}", f"border-color: {border}"],
    )

    # Dropdown menu.
    menu = f".dropdown-menu.dropdown-menu-{name}"
    yield "dropdown", _rule(
        [menu, f"{menu} li > a", f"{menu} li > input", f"{menu} li > button"],
        [f"color: {text}", f"background-color: {base}", f"border-color: {border}"],
    )
    yield "dropdown", _rule(
        [
            f"{menu} li > a:hover",
            f"{menu} li > a:focus",
            f"{menu} li > input:hover",
            f"{menu} li > input:focus",
            f"{menu} li > button:hover",
            f"{menu} li > button:focus",
            f"{menu} .active > a",
        ],
        [f"color: {text}", f"background-color: {hover}"],
    )
    yield "dropdown", _rule(f"{menu} li.divider", [f"background-color: {border}", f"border-color: {border}"])

    # Info box.
    if color.has_dark_background:
        yield "info-box", _rule(f".info-box.bg-{name} .info-box-icon", ["background: rgba(255, 255, 255, 0.2)"])

    # Label.
    if not _ships("label", name):
        yield "label", _rule(f".label.label-{name}", [f"color: {text}", f"background-color: {base}"])
        if color.has_dark_text:
            yield "label", _rule(
                [f"a.label.label-{name}:hover", f"a.label.label-{name}:focus"],
                [f"color: {text}"],
            )

    # Modal.
    if not _ships("modal", name):
        modal = f".modal.modal-{name}"
        yield "modal", _rule(
            [f"{modal} .modal-header", f"{modal} .modal-footer", f"{modal} .modal-header .alert-{name}"],
            [f"color: {text}", f"background-color: {active}", f"border-color: {border}"],
        )
        yield "modal", _rule(f"{modal} .modal-body", [f"color: {text}", f"background-color: {base}"])

    # Small box.
    if color.has_dark_text:
        yield "small-box", _rule(
            [f".small-box.bg-{name} > .small-box-footer", f".small-box.bg-{name} > .small-box-footer:hover"],
            [f"color: {text}"],
        )
    if color.has_dark_background:
        yield "small-box", _rule(f".small-box.bg-{name} .icon", ["color: rgba(255, 255, 255, 0.15)"])
        yield "small-box", _rule(f".small-box.bg-{name} > .small-box-footer", ["background: rgba(255, 255, 255, 0.1)"])

    # Table rows and cells. Same structure as Bootstrap's contextual table classes.
    # Header and footer rows take the color itself. This includes Bootstrap's contextual rows, which Bootstrap draws in
    # the same pale tint as body rows, so that every color's header and footer look alike.
    yield "table", _rule(
        [f".table > {section} > tr > {cell}.{name}" for section in ("thead", "tfoot") for cell in ("td", "th")]
        + [f".table > {section} > tr.{name} > {cell}" for section in ("thead", "tfoot") for cell in ("td", "th")],
        [f"color: {text}", f"background-color: {base}"],
    )
    if not _ships("table-row", name):
        yield "table", _rule(
            [f".table > tbody > tr > {cell}.{name}" for cell in ("td", "th")]
            + [f".table > tbody > tr.{name} > {cell}" for cell in ("td", "th")],
            ["color: var(--pdq-table-body-text)", f"background-color: {light_accent}"],
        )
        yield "table", _rule(
            [
                f".table-hover > tbody > tr > td.{name}:hover",
                f".table-hover > tbody > tr > th.{name}:hover",
                f".table-hover > tbody > tr.{name}:hover > td",
                f".table-hover > tbody > tr:hover > .{name}",
                f".table-hover > tbody > tr.{name}:hover > th",
            ],
            [f"background-color: {table_hover}"],
        )
    bordered = f".table-bordered.table-border-{name}"
    yield "table", _rule(
        [f"{bordered} > {section} > tr > {cell}" for section in ("thead", "tbody", "tfoot") for cell in ("th", "td")],
        [f"border: 1px solid {light_accent}"],
    )
    yield "table", _rule(
        [f"{bordered} > {section} > tr.{name} > {cell}" for section in ("thead", "tfoot") for cell in ("th", "td")]
        + [f"{bordered} > {section} > tr > {cell}.{name}" for section in ("thead", "tfoot") for cell in ("th", "td")],
        [f"border: 1px solid {border}"],
    )
    yield "table", _rule(
        [f"{bordered} > tbody > tr.{name} > {cell}" for cell in ("th", "td")]
        + [f"{bordered} > tbody > tr > {cell}.{name}" for cell in ("th", "td")],
        [f"border: 1px solid {base}"],
    )

    # Tooltip. The class goes on the element with the tooltip; Bootstrap inserts the tooltip
    # right after it. The tooltip color script also copies the class onto the tooltip itself.
    for direction in ("top", "right", "bottom", "left"):
        yield "tooltip", _rule(
            [
                f".tooltip-{name} + .tooltip.{direction} > .tooltip-arrow",
                f".tooltip.tooltip-{name}.{direction} > .tooltip-arrow",
            ],
            [f"border-{direction}-color: {base}"],
        )
    yield "tooltip", _rule(
        [f".tooltip-{name} + .tooltip > .tooltip-inner", f".tooltip.tooltip-{name} > .tooltip-inner"],
        [f"color: {text}", f"background-color: {base}"],
    )


COMPONENT_ORDER = [
    "background",
    "text",
    "code",
    "alert",
    "box",
    "button",
    "callout",
    "carousel",
    "dropdown",
    "info-box",
    "label",
    "modal",
    "small-box",
    "table",
    "tooltip",
]


def render_components():
    """Render the per-color component rules, grouped by component."""
    grouped = {component: [] for component in COMPONENT_ORDER}
    for name in NAMES:
        for component, rule in _component_rules(name):
            grouped[component].append(rule)

    parts = [
        "/**",
        " * AdminLTE PDQ extra colors.",
        " *",
        " * GENERATED by adminlte2_pdq/color_css.py. Do not edit by hand.",
        " *",
        " * Adds color classes that AdminLTE and Bootstrap do not provide, for every color in",
        " * color-variables.css. Classes that AdminLTE or Bootstrap already define are not",
        " * redefined, so stock components keep their stock look.",
        " */",
    ]
    for component in COMPONENT_ORDER:
        parts += ["", "", f"/* region {component} */", ""]
        parts.append("\n\n".join(grouped[component]))
        parts += ["", f"/* endregion {component} */"]
    return "\n".join(parts) + "\n"


def render_custom_color(color):
    """Render the variables and component rules for one color that is not in the palette.

    The result can be saved as a stylesheet and loaded after the package's CSS.
    """
    if color.name in NAMES:
        raise ValueError(f"'{color.name}' is already a package color.")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", color.name):
        raise ValueError("Color names must be lowercase letters, digits, and hyphens.")

    grouped = {component: [] for component in COMPONENT_ORDER}
    for component, rule in _component_rules(color.name, color):
        grouped[component].append(rule)

    parts = [
        "/**",
        f" * AdminLTE PDQ color: {color.name}.",
        " *",
        " * Generated by: python -m adminlte2_pdq.color_css --custom ...",
        " */",
        "",
        "",
        ":root {",
        *_variable_lines(color),
        "}",
    ]
    for component in COMPONENT_ORDER:
        if grouped[component]:
            parts += ["", "", f"/* {component} */", ""]
            parts.append("\n\n".join(grouped[component]))
    return "\n".join(parts) + "\n"


# endregion Rendering


OUTPUT_DIR = Path(__file__).resolve().parent / "static" / "adminlte2_pdq" / "css" / "extra-colors"
OUTPUTS = {
    "color-variables.css": render_variables,
    "extra-colors.css": render_components,
}


def main(argv=None):
    """Write the package's generated CSS files, or print the CSS for one custom color."""
    parser = argparse.ArgumentParser(prog="python -m adminlte2_pdq.color_css", description=main.__doc__)
    parser.add_argument(
        "--custom",
        nargs=2,
        metavar=("NAME", "BASE"),
        help="Print the CSS for a new color, for example: --custom brand '#6610f2'",
    )
    parser.add_argument("--active", help="Active (darker) shade for --custom. Default: base darkened 5%%.")
    parser.add_argument("--dark-text", action="store_true", help="Use dark text on --custom instead of white.")
    args = parser.parse_args(argv)

    if args.custom:
        name, base = args.custom
        color = Color(name, base=base, active=args.active, text=TEXT_DARK if args.dark_text else TEXT_LIGHT)
        try:
            sys.stdout.write(render_custom_color(color))
        except ValueError as error:
            parser.error(str(error))
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for file_name, render in OUTPUTS.items():
        (OUTPUT_DIR / file_name).write_text(render(), encoding="utf-8")
        print(f"Wrote {OUTPUT_DIR / file_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
