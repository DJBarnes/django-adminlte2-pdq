"""Views for the demo CSS pages.

The pages show the AdminLTE elements and the package's extra CSS, and can be used to check
that the package's HTML and CSS work as expected.
"""

# Third-Party Imports.
from django.contrib import messages
from django.shortcuts import render

# Internal Imports.
from adminlte2_pdq.constants import DEMO_CSS_COLORS
from adminlte2_pdq.color_css import BG_NAMES
from adminlte2_pdq.menu import CSS_MENU, MENU
from adminlte2_pdq.templatetags.sidebar_menu import _default_routes_are_registered


def _render_demo_page(request, template_name, context=None):
    """Render a demo CSS page with the demo menu and color list."""
    menu = list(CSS_MENU)
    if _default_routes_are_registered():
        # Add the default menu's sections after its first ("Home") section.
        menu += MENU[1:]

    page_context = {
        "ADMINLTE2_MENU": menu,
        "bootstrap_types": list(DEMO_CSS_COLORS),
        "demo_css_colors": DEMO_CSS_COLORS,
        # Name used in `bg-{color}` classes. Bootstrap's own `bg-primary`, `bg-info`, etc. are pale
        # tints, so the demo uses AdminLTE's names for those colors.
        "demo_bg_names": {name: BG_NAMES.get(name, name) for name in DEMO_CSS_COLORS},
    }
    page_context.update(context or {})
    return render(request, f"adminlte2_demo_css/{template_name}", page_context)


def demo_css(request):
    """Demo CSS home page, which links to the other demo pages."""
    return _render_demo_page(request, "home.html")


def demo_css_alerts(request):
    """Alerts, including Django messages at each level."""
    messages.set_level(request, messages.DEBUG)
    messages.debug(request, "This is a debug message via the messages framework.")
    messages.info(request, "This is a info message via the messages framework.")
    messages.success(request, "This is a success message via the messages framework.")
    messages.warning(request, "This is a warning message via the messages framework.")
    messages.error(request, "This is a error message via the messages framework.")
    messages.add_message(request, 50, "This is an unknown level message via the messages framework.")
    return _render_demo_page(request, "alerts.html")


def demo_css_boxes_solid(request):
    """Solid boxes."""
    return _render_demo_page(request, "boxes_solid.html")


def demo_css_boxes_standard(request):
    """Standard boxes."""
    return _render_demo_page(request, "boxes_standard.html")


def demo_css_buttons_basic(request):
    """Basic buttons and button groups."""
    return _render_demo_page(request, "buttons_basic.html")


def demo_css_buttons_specialized(request):
    """App buttons and other specialized buttons."""
    return _render_demo_page(request, "buttons_specialized.html")


def demo_css_carousels(request):
    """Carousels."""
    return _render_demo_page(request, "carousels.html")


def demo_css_forms(request):
    """Form elements."""
    return _render_demo_page(request, "forms.html")


def demo_css_full_span_links(request):
    """Full-span links."""
    return _render_demo_page(request, "full_span_links.html")


def demo_css_labels(request):
    """Labels and tooltips."""
    return _render_demo_page(request, "labels.html")


def demo_css_modals(request):
    """Modals."""
    return _render_demo_page(request, "modals.html")


def demo_css_tables(request):
    """Tables."""
    return _render_demo_page(request, "tables.html")


def demo_css_typography(request):
    """Text and typography."""
    return _render_demo_page(request, "typography.html")


def demo_css_ui_general(request):
    """General UI elements, including the color palette."""
    return _render_demo_page(request, "ui_general.html")


def demo_css_widgets(request):
    """Widgets: info boxes, small boxes, and state widgets."""
    return _render_demo_page(request, "widgets.html")
