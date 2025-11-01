"""panels package: exports modular tkinter UI components used by the example GUI.

Each module exposes a Frame subclass that can be composed by a parent application.
"""

from .input_panel import InputPanel
from .parse_table_panel import ParseTablePanel
from .parsing_trace_panel import ParsingTracePanel
from .productions_panel import ProductionsPanel
from .topbar import TopBar

__all__ = [
    "TopBar",
    "ProductionsPanel",
    "ParseTablePanel",
    "InputPanel",
    "ParsingTracePanel",
]
