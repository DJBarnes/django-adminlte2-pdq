"""
Generator for the package's extra color CSS.

Writes three files:

* ``css/extra-colors/color-variables.css``: one set of CSS custom properties per color.
* ``css/extra-colors/extra-colors.css``: the color classes for every color and component, using those properties.
  This includes the classes that AdminLTE 2.3.11 and Bootstrap 3.3.7 already define. Their rules reproduce
  AdminLTE's and Bootstrap's own, so with the default properties they look the same as without this file, and
  changing a color's properties changes every class of that color.
* ``css/extra-colors/consistent-colors.css``: loaded only with the ADMINLTE2_CONSISTENT_COLORS setting. Draws the
  classes that keep Bootstrap's own shades, or AdminLTE's different default grays, in their color's AdminLTE shades,
  so each color name is one color everywhere.

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

    Some classes of Bootstrap's colors (default, primary, info, success, warning, danger) use Bootstrap's own shades,
    which differ from AdminLTE's. They have their own values, so they keep their stock look:

    * ``bootstrap_btn``, ``bootstrap_btn_border``, ``bootstrap_btn_text``: Bootstrap's button colors. AdminLTE only
      replaces a button's normal and hover colors, so its focus, pressed, and disabled states and its badge use these.
    * ``bootstrap_bg``, ``bootstrap_text``: Bootstrap's ``bg-{c}`` (a pale tint, solid for primary) and ``text-{c}``
      (a darker shade).
    * ``box_label``: the gray of AdminLTE's default box and label, which is darker than its default button.

    The hover and pressed shades of these are derived, the way Bootstrap's LESS derives them. ``bootstrap_shades``
    gives Bootstrap's compiled values instead, by variable part, where its LESS build rounded them differently.
    """

    name: str
    base: str
    active: str = None
    light_accent: str = None
    table_hover: str = None
    text: str = TEXT_LIGHT
    border: str = None
    hover: str = None
    bootstrap_btn: str = None
    bootstrap_btn_border: str = None
    bootstrap_btn_text: str = None
    bootstrap_bg: str = None
    bootstrap_text: str = None
    box_label: str = None
    bootstrap_shades: dict = None

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

    def bootstrap_values(self):
        """Return the values for Bootstrap's own shades of this color, by variable part, or {} for other colors."""
        values = {}
        if self.bootstrap_btn:
            # Bootstrap's button-variant mixin.
            values.update(
                {
                    "bootstrap-btn": self.bootstrap_btn,
                    "bootstrap-btn-border": self.bootstrap_btn_border,
                    "bootstrap-btn-text": self.bootstrap_btn_text,
                    "bootstrap-btn-hover": darken(self.bootstrap_btn, 0.10),
                    "bootstrap-btn-hover-border": darken(self.bootstrap_btn_border, 0.12),
                    "bootstrap-btn-focus-border": darken(self.bootstrap_btn_border, 0.25),
                    "bootstrap-btn-pressed": darken(self.bootstrap_btn, 0.17),
                }
            )
        if self.bootstrap_bg:
            # Bootstrap's bg-variant and text-emphasis-variant mixins.
            values.update(
                {
                    "bootstrap-bg": self.bootstrap_bg,
                    "bootstrap-bg-hover": darken(self.bootstrap_bg, 0.10),
                    "bootstrap-text": self.bootstrap_text,
                    "bootstrap-text-hover": darken(self.bootstrap_text, 0.10),
                }
            )
        if self.box_label:
            values["box-label"] = self.box_label
        values.update(self.bootstrap_shades or {})
        return values

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
        bootstrap_btn="#fff",
        bootstrap_btn_border="#ccc",
        bootstrap_btn_text="#333",
        box_label="#d2d6de",
    ),
    Color(
        "primary",
        base="#3c8dbc",
        active="#357ca5",
        bootstrap_btn="#337ab7",
        bootstrap_btn_border="#2e6da4",
        bootstrap_btn_text="#fff",
        bootstrap_bg="#337ab7",
        bootstrap_text="#337ab7",
        bootstrap_shades={
            "bootstrap-btn-hover": "#286090",
            "bootstrap-btn-hover-border": "#204d74",
            "bootstrap-btn-focus-border": "#122b40",
            "bootstrap-btn-pressed": "#204d74",
            "bootstrap-bg-hover": "#286090",
            "bootstrap-text-hover": "#286090",
        },
    ),
    Color(
        "info",
        base="#00c0ef",
        active="#00a7d0",
        light_accent="#d9edf7",
        table_hover="#c4e3f3",
        bootstrap_btn="#5bc0de",
        bootstrap_btn_border="#46b8da",
        bootstrap_btn_text="#fff",
        bootstrap_bg="#d9edf7",
        bootstrap_text="#31708f",
        bootstrap_shades={
            "bootstrap-btn-hover": "#31b0d5",
            "bootstrap-btn-hover-border": "#269abc",
            "bootstrap-btn-focus-border": "#1b6d85",
            "bootstrap-btn-pressed": "#269abc",
            "bootstrap-bg-hover": "#afd9ee",
            "bootstrap-text-hover": "#245269",
        },
    ),
    Color(
        "success",
        base="#00a65a",
        active="#008d4c",
        light_accent="#dff0d8",
        table_hover="#d0e9c6",
        bootstrap_btn="#5cb85c",
        bootstrap_btn_border="#4cae4c",
        bootstrap_btn_text="#fff",
        bootstrap_bg="#dff0d8",
        bootstrap_text="#3c763d",
        bootstrap_shades={
            "bootstrap-btn-hover": "#449d44",
            "bootstrap-btn-hover-border": "#398439",
            "bootstrap-btn-focus-border": "#255625",
            "bootstrap-btn-pressed": "#398439",
            "bootstrap-bg-hover": "#c1e2b3",
            "bootstrap-text-hover": "#2b542c",
        },
    ),
    Color(
        "warning",
        base="#f39c12",
        active="#db8b0b",
        light_accent="#fcf8e3",
        table_hover="#faf2cc",
        bootstrap_btn="#f0ad4e",
        bootstrap_btn_border="#eea236",
        bootstrap_btn_text="#fff",
        bootstrap_bg="#fcf8e3",
        bootstrap_text="#8a6d3b",
        bootstrap_shades={
            "bootstrap-btn-hover": "#ec971f",
            "bootstrap-btn-hover-border": "#d58512",
            "bootstrap-btn-focus-border": "#985f0d",
            "bootstrap-btn-pressed": "#d58512",
            "bootstrap-bg-hover": "#f7ecb5",
            "bootstrap-text-hover": "#66512c",
        },
    ),
    Color(
        "danger",
        base="#dd4b39",
        active="#d33724",
        light_accent="#f2dede",
        table_hover="#ebcccc",
        bootstrap_btn="#d9534f",
        bootstrap_btn_border="#d43f3a",
        bootstrap_btn_text="#fff",
        bootstrap_bg="#f2dede",
        bootstrap_text="#a94442",
        bootstrap_shades={
            "bootstrap-btn-hover": "#c9302c",
            "bootstrap-btn-hover-border": "#ac2925",
            "bootstrap-btn-focus-border": "#761c19",
            "bootstrap-btn-pressed": "#ac2925",
            "bootstrap-bg-hover": "#e4b9b9",
            "bootstrap-text-hover": "#843534",
        },
    ),
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
# Bootstrap's table row and cell classes.
BOOTSTRAP_TABLE_ROWS = {"info", "success", "warning", "danger"}

# Component classes that AdminLTE or Bootstrap already ships, per component. Their rules reproduce the stock look.
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

# Components whose colors AdminLTE sets with !important. Their rules for the classes AdminLTE ships need it too.
IMPORTANT_COMPONENTS = {"alert", "callout", "label", "modal"}

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
    lines = [f"    --pdq-{color.name}-{part}: {values[part]};" for part in VARIABLE_PARTS]
    lines += [f"    --pdq-{color.name}-{part}: {value};" for part, value in color.bootstrap_values().items()]
    return lines


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
    """Whether AdminLTE or Bootstrap already styles the class."""
    return name in SHIPPED.get(component, set())


def _important(rule):
    """Make a rule's color and background declarations !important."""
    return re.sub(
        r"^(    (?:color|background|background-color): [^;!]*);$",
        r"\1 !important;",
        rule,
        flags=re.MULTILINE,
    )


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


def _bootstrap_button_rules(name):
    """Yield the rules for one of Bootstrap's buttons, as Bootstrap and then AdminLTE define them.

    The selectors are Bootstrap's and AdminLTE's own, in the same order, so the result is the same as the stock CSS.
    AdminLTE only replaces the normal and hover colors; the other states keep Bootstrap's shades.
    """
    button = f".btn-{name}"

    def bootstrap(part=""):
        return _var(name, f"bootstrap-btn{'-' + part if part else ''}")

    text = bootstrap("text")

    # Bootstrap's button-variant mixin.
    yield _rule(button, [f"color: {text}", f"background-color: {bootstrap()}", f"border-color: {bootstrap('border')}"])
    yield _rule(
        [f"{button}:focus", f"{button}.focus"],
        [f"color: {text}", f"background-color: {bootstrap('hover')}", f"border-color: {bootstrap('focus-border')}"],
    )
    yield _rule(
        f"{button}:hover",
        [f"color: {text}", f"background-color: {bootstrap('hover')}", f"border-color: {bootstrap('hover-border')}"],
    )
    yield _rule(
        [f"{button}:active", f"{button}.active", f".open > .dropdown-toggle{button}"],
        [f"color: {text}", f"background-color: {bootstrap('hover')}", f"border-color: {bootstrap('hover-border')}"],
    )
    yield _rule(
        [
            f"{button}:active:hover",
            f"{button}.active:hover",
            f".open > .dropdown-toggle{button}:hover",
            f"{button}:active:focus",
            f"{button}.active:focus",
            f".open > .dropdown-toggle{button}:focus",
            f"{button}:active.focus",
            f"{button}.active.focus",
            f".open > .dropdown-toggle{button}.focus",
        ],
        [f"color: {text}", f"background-color: {bootstrap('pressed')}", f"border-color: {bootstrap('focus-border')}"],
    )
    yield _rule(
        [
            f"{button}.disabled:hover",
            f"{button}[disabled]:hover",
            f"fieldset[disabled] {button}:hover",
            f"{button}.disabled:focus",
            f"{button}[disabled]:focus",
            f"fieldset[disabled] {button}:focus",
            f"{button}.disabled.focus",
            f"{button}[disabled].focus",
            f"fieldset[disabled] {button}.focus",
        ],
        [f"background-color: {bootstrap()}", f"border-color: {bootstrap('border')}"],
    )
    yield _rule(f"{button} .badge", [f"color: {bootstrap()}", f"background-color: {text}"])

    # AdminLTE's colors. Its default button has dark text, and its border is the default color's border shade.
    if name == "default":
        normal = [f"color: {_var(name, 'text')}", f"border-color: {_var(name, 'border')}"]
    else:
        normal = [f"border-color: {_var(name, 'hover')}"]
    yield _rule(button, [f"background-color: {_var(name, 'base')}"] + normal)
    yield _rule(
        [f"{button}:hover", f"{button}:active", f"{button}.hover"],
        [f"background-color: {_var(name, 'hover')}"],
    )


def _component_rules(name, color=None):  # pylint: disable=too-many-statements,too-many-branches
    """Yield (component, rule) pairs for one class name.

    Classes that AdminLTE or Bootstrap already define get rules that reproduce their stock look.
    """
    color = color or _color_for(name)

    def ships(component):
        return _ships(component, name)

    text, base, active = _var(name, "text"), _var(name, "base"), _var(name, "active")
    border, hover = _var(name, "border"), _var(name, "hover")
    light_accent, light_accent_text = _var(name, "light-accent"), _var(name, "light-accent-text")
    table_hover = _var(name, "table-hover")

    # Background, background-active, and text utilities.
    if name in BOOTSTRAP_CONTEXTUAL:
        # Bootstrap's `.bg-{c}` is a pale tint (solid for primary, with white text) and its `.text-{c}` a darker shade.
        yield "background", _rule(
            f".bg-{name}",
            ([f"color: {text}"] if name == "primary" else []) + [f"background-color: {_var(name, 'bootstrap-bg')}"],
        )
        yield "background", _rule(
            [f"a.bg-{name}:hover", f"a.bg-{name}:focus"],
            [f"background-color: {_var(name, 'bootstrap-bg-hover')}"],
        )
        yield "text", _rule(f".text-{name}", [f"color: {_var(name, 'bootstrap-text')}"])
        yield "text", _rule(
            [f"a.text-{name}:hover", f"a.text-{name}:focus"],
            [f"color: {_var(name, 'bootstrap-text-hover')}"],
        )
    else:
        # AdminLTE's gray background is the only one whose text color isn't !important.
        important = "" if name == "gray" else " !important"
        background = [f"color: {text}{important}", f"background-color: {base} !important"]
        if not ships("bg"):
            # The package's own colors also color the border, which shows on app buttons (`btn-app`).
            background.append(f"border-color: {border}")
        yield "background", _rule(f".bg-{name}", background)
        yield "background", _rule(
            f".bg-{name}-active",
            [f"color: {text} !important", f"background-color: {active} !important"],
        )
        # `.text-default` uses the default text color; the default base is too light to read.
        text_value = text if name == "default" else base
        yield "text", _rule(f".text-{name}", [f"color: {text_value} !important"])

    # Code tint.
    yield "code", _rule(
        f"code.code-{name}",
        [f"color: {light_accent_text}", f"background-color: {light_accent}"],
    )

    # Alert. The classes AdminLTE ships use its own selectors, so they win and lose against other rules as before.
    yield "alert", _rule(
        f".alert-{name}" if ships("alert") else f".alert.alert-{name}",
        [f"color: {text}", f"background-color: {base}", f"border-color: {hover}"],
    )
    if color.has_dark_text:
        yield "alert", _rule(f".alert.alert-{name} a", [f"color: {text}"])
    if color.has_dark_background:
        yield "alert", _rule(f".alert.alert-{name} .close", ["color: #fff"])

    # Box. AdminLTE's default box is its gray, which is darker than the default color.
    box = _var(name, "box-label") if color.box_label else base
    yield "box", _rule(f".box.box-{name}", [f"border-top-color: {box}"])
    yield "box", _rule(f".box.box-solid.box-{name}", [f"border: 1px solid {box}"])
    yield "box", _rule(
        f".box.box-solid.box-{name} > .box-header",
        [f"color: {text}", f"background: {box}", f"background-color: {box}"],
    )
    yield "box", _rule(
        [f".box.box-solid.box-{name} > .box-header a", f".box.box-solid.box-{name} > .box-header .btn"],
        [f"color: {text}"],
    )

    # Button.
    if ships("btn"):
        for rule in _bootstrap_button_rules(name):
            yield "button", rule
    else:
        # States follow Bootstrap's button-variant mixin, with AdminLTE's colors.
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
    if name != "default":
        # AdminLTE darkens every `.btn` in a solid box header on hover, which hides the button's own hover color.
        # Restore it. AdminLTE's default button already has its own rule there.
        yield "button", _rule(f".box.box-solid > .box-header .btn.btn-{name}", [f"color: {text}"])
        yield "button", _rule(
            [
                f".box.box-solid > .box-header .btn.btn-{name}:hover",
                f".box.box-solid > .box-header .btn.btn-{name}:focus",
            ],
            [f"background-color: {hover}"],
        )

    # Callout.
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

    # Label. AdminLTE's default label is its gray, which is darker than the default color, and a linked default label
    # keeps Bootstrap's hover colors.
    if color.box_label:
        yield "label", _rule(f".label.label-{name}", [f"color: {text}", f"background-color: {_var(name, 'box-label')}"])
    else:
        label = f".label-{name}" if ships("label") else f".label.label-{name}"
        yield "label", _rule(label, [f"color: {text}", f"background-color: {base}"])
        if color.has_dark_text:
            yield "label", _rule(
                [f"a.label.label-{name}:hover", f"a.label.label-{name}:focus"],
                [f"color: {text}"],
            )

    # Modal.
    if ships("modal"):
        modal = f".modal-{name}"
        header = [f"{modal} .modal-header", f"{modal} .modal-footer"]
    else:
        modal = f".modal.modal-{name}"
        header = [f"{modal} .modal-header", f"{modal} .modal-footer", f"{modal} .modal-header .alert-{name}"]
    yield "modal", _rule(header, [f"color: {text}", f"background-color: {active}", f"border-color: {border}"])
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
    if ships("table-row"):
        # Bootstrap's rows: every row, header and footer included, is the pale tint, under the page's text color.
        yield "table", _rule(
            [
                f".table > {section} > tr > {cell}.{name}"
                for cell in ("td", "th")
                for section in ("thead", "tbody", "tfoot")
            ]
            + [
                f".table > {section} > tr.{name} > {cell}"
                for cell in ("td", "th")
                for section in ("thead", "tbody", "tfoot")
            ],
            [f"background-color: {light_accent}"],
        )
    else:
        # Header and footer rows take the color itself, and body rows the pale tint.
        yield "table", _rule(
            [f".table > {section} > tr > {cell}.{name}" for section in ("thead", "tfoot") for cell in ("td", "th")]
            + [f".table > {section} > tr.{name} > {cell}" for section in ("thead", "tfoot") for cell in ("td", "th")],
            [f"color: {text}", f"background-color: {base}"],
        )
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


def _grouped_rules(name, color=None):
    """Return one class name's rules, grouped by component, with !important where AdminLTE uses it."""
    grouped = {component: [] for component in COMPONENT_ORDER}
    for component, rule in _component_rules(name, color):
        # AdminLTE's default label isn't !important, unlike its colored ones.
        if component in IMPORTANT_COMPONENTS and _ships(component, name) and name != "default":
            rule = _important(rule)
        grouped[component].append(rule)
    return grouped


def render_components():
    """Render the per-color component rules, grouped by component."""
    grouped = {component: [] for component in COMPONENT_ORDER}
    for name in NAMES:
        for component, rules in _grouped_rules(name).items():
            grouped[component] += rules
    # AdminLTE's modal header and footer borders come after its alert colors, so they win on an alert that is also a
    # modal header or footer. Repeat them after the alert rules above, which replace AdminLTE's.
    grouped["alert"] += [
        _rule(".modal-header", ["border-bottom-color: #f4f4f4"]),
        _rule(".modal-footer", ["border-top-color: #f4f4f4"]),
    ]

    parts = [
        "/**",
        " * AdminLTE PDQ extra colors.",
        " *",
        " * GENERATED by adminlte2_pdq/color_css.py. Do not edit by hand.",
        " *",
        " * The color classes for every color in color-variables.css. This includes the classes that",
        " * AdminLTE and Bootstrap already define, such as bg-maroon, btn-primary, and label-danger,",
        " * with rules that reproduce their stock look, so changing a color's variables changes every",
        " * class of that color.",
        " */",
    ]
    for component in COMPONENT_ORDER:
        parts += ["", "", f"/* region {component} */", ""]
        parts.append("\n\n".join(grouped[component]))
        parts += ["", f"/* endregion {component} */"]
    return "\n".join(parts) + "\n"


# For ADMINLTE2_CONSISTENT_COLORS, the AdminLTE shade that replaces each of Bootstrap's button shades. These are the
# shades the package's own colors use for the same button states.
CONSISTENT_BUTTON_PARTS = {
    "bootstrap-btn": "base",
    "bootstrap-btn-border": "hover",
    "bootstrap-btn-text": "text",
    "bootstrap-btn-hover": "hover",
    "bootstrap-btn-hover-border": "border",
    "bootstrap-btn-focus-border": "border",
    "bootstrap-btn-pressed": "hover",
}


def render_consistent_colors():
    """Render the stylesheet for ADMINLTE2_CONSISTENT_COLORS.

    Bootstrap's button shades and AdminLTE's default box and label gray point at the color's own variables, and
    Bootstrap's bg-{c}, text-{c}, and table header rows get the rules of the package's other colors.
    """
    variables = []
    for name in sorted(SHIPPED["btn"], key=NAMES.index):
        variables.append(f"    /* {name} */")
        parts = dict(CONSISTENT_BUTTON_PARTS)
        if name == "default":
            # AdminLTE's default button border is the default color's border shade, not its hover shade.
            parts["bootstrap-btn-border"] = "border"
        variables += [f"    --pdq-{name}-{part}: {_var(name, adminlte_part)};" for part, adminlte_part in parts.items()]
    # The default box and label take the default color's border shade, the edge of the default button. AdminLTE's gray
    # would make default the same as the gray color, and the default color itself is too light for a box's top border.
    variables += ["    /* default box and label */", "    --pdq-default-box-label: var(--pdq-default-border);"]

    rules = []
    for name in sorted(BOOTSTRAP_CONTEXTUAL, key=NAMES.index):
        text, base, active = _var(name, "text"), _var(name, "base"), _var(name, "active")
        rules += [
            _rule(f".bg-{name}", [f"color: {text} !important", f"background-color: {base} !important"]),
            _rule(f".bg-{name}-active", [f"color: {text} !important", f"background-color: {active} !important"]),
            _rule(f".text-{name}", [f"color: {base} !important"]),
        ]
    for name in sorted(BOOTSTRAP_TABLE_ROWS, key=NAMES.index):
        # !important, so the dark skins' tint of Bootstrap's rows doesn't apply, as for the other colors' header rows.
        rules.append(
            _rule(
                [f".table > {section} > tr > {cell}.{name}" for section in ("thead", "tfoot") for cell in ("td", "th")]
                + [
                    f".table > {section} > tr.{name} > {cell}"
                    for section in ("thead", "tfoot")
                    for cell in ("td", "th")
                ],
                [f"color: {_var(name, 'text')} !important", f"background-color: {_var(name, 'base')} !important"],
            )
        )

    parts = [
        "/**",
        " * AdminLTE PDQ consistent colors.",
        " *",
        " * GENERATED by adminlte2_pdq/color_css.py. Do not edit by hand.",
        " *",
        " * Loaded only when the ADMINLTE2_CONSISTENT_COLORS setting is True. Draws the classes that",
        " * keep Bootstrap's own shades, or AdminLTE's different default grays, in their color's",
        " * AdminLTE shades, so that each color name is one color everywhere.",
        " */",
        "",
        "",
        ":root {",
        *variables,
        "}",
        "",
        "",
        "\n\n".join(rules),
    ]
    return "\n".join(parts) + "\n"


def render_custom_color(color):
    """Render the variables and component rules for one color that is not in the palette.

    The result can be saved as a stylesheet and loaded after the package's CSS.
    """
    if color.name in NAMES:
        raise ValueError(f"'{color.name}' is already a package color.")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", color.name):
        raise ValueError("Color names must be lowercase letters, digits, and hyphens.")

    grouped = _grouped_rules(color.name, color)

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
    "consistent-colors.css": render_consistent_colors,
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
