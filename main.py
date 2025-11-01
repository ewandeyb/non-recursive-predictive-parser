import tkinter as tk
from tkinter import ttk

from panels import (
    InputPanel,
    ParseTablePanel,
    ParsingTracePanel,
    ProductionsPanel,
    TopBar,
)

SAMPLE_PRODUCTIONS = [
    (1, "E", "T E'"),
    (2, "E'", "+ T E'"),
    (3, "E'", "ε"),
    (4, "T", "F T'"),
    (5, "T'", "* F T'"),
    (6, "T'", "ε"),
    (7, "F", "( E )"),
    (8, "F", "id"),
]

SAMPLE_PARSE_TABLE = [
    ("E", "1", "", "", "1", "", ""),
    ("E'", "", "2", "", "3", "3", ""),
    ("T", "4", "", "", "4", "", ""),
    ("T'", "", "6", "5", "6", "6", ""),
    ("F", "8", "", "", "7", "", ""),
]


class ParserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Non-Recursive Predictive Parser - Example")
        self.geometry("1000x700")

        # Left: productions
        self.prods = ProductionsPanel(self, relief="sunken")
        self.prods.grid(
            row=0, column=0, rowspan=2, sticky="nsew", padx=8, pady=8
        )
        self.prods.set_productions(SAMPLE_PRODUCTIONS)

        # Right top: parse table and topbar stacked
        topframe = ttk.Frame(self)
        topframe.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        topframe.columnconfigure(0, weight=1)

        self.topbar = TopBar(
            topframe, load_command=self._on_load, parse_command=self._on_parse
        )
        self.topbar.grid(row=0, column=0, sticky="ew")

        self.parse_table = ParseTablePanel(topframe)
        self.parse_table.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        self.parse_table.set_table(SAMPLE_PARSE_TABLE)

        # Middle: input
        self.input_panel = InputPanel(self, parse_command=self._on_input_parse)
        self.input_panel.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
        )

        # Bottom: parsing trace
        self.trace = ParsingTracePanel(self, relief="sunken")
        self.trace.grid(
            row=3, column=0, columnspan=2, sticky="nsew", padx=8, pady=8
        )

        # grid weight
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        # seed example trace
        self._seed_trace()

    def _seed_trace(self):
        # Add a few example rows similar to the attachment's trace
        rows = [
            ("E $", "id + id * id $", "Output E > T E'"),
            ("T E' $", "id + id * id $", "Output T > F T'"),
            ("F T' E' $", "id + id * id $", "Output F > id"),
        ]
        for s, i, a in rows:
            self.trace.append(s, i, a)

    def _on_load(self):
        # placeholder: in a full app this would open and read rules.prod
        self.topbar.loaded_label.config(text="LOADED: rules.prod (sample)")

    def _on_parse(self):
        # when top-right Parse is pressed, just append a marker
        self.trace.append("$", "$", "Parse (topbar)")

    def _on_input_parse(self, text):
        self.trace.append(text, "$", f"Parse input: {text}")


def main():
    app = ParserApp()
    app.mainloop()


if __name__ == "__main__":
    main()
