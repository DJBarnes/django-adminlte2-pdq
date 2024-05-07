"""Utility logic."""

# Third-Party Imports.
from .constants import SHOW_DEBUG_PRINT


def debug_print(value):
    """Used to print debug output for project.

    To enable printing, call `debug_print.debug = True` in the local function above where you want printing.
    Alternatively, set `SHOW_DEBUG_PRINT = True` in env.py, to enable debug print statements for entire project.
    """

    if (
        # If package has DEBUG_PRINT value and is True.
        SHOW_DEBUG_PRINT
        # Or if this function has "debug" value set and is True.
        or (hasattr(debug_print, 'debug') and debug_print.debug)
    ):
        # Doing a print. Handle based on type.
        print(value)


# Alias for above DebugPrint.
dprint = debug_print
