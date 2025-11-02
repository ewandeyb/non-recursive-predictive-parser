import tkinter as tk
import tkinter.filedialog as fd
from pathlib import Path
from tkinter import ttk

from output_handling import create_file, create_parsing_steps_table
from panels.input_panel import InputPanel
from panels.load_file import LoadFileWidget
from panels.parse_table_panel import ParseTablePanel
from panels.parsing_trace_panel import ParsingTracePanel
from panels.productions_panel import ProductionsPanel


class ParserApp(tk.Tk):
    NO_FILE = "No file loaded yet."

    def __init__(self):
        super().__init__()
        self.title("Non-Recursive Predictive Parser - Example")
        self.geometry("1000x700")

        self.file_name = self.NO_FILE

        self._init_production_rules()  # top left
        self._init_parse_table()  # top right
        self._init_input_panel()  # middle
        self._init_result_panel()  # under input panel
        self._init_parse_trace()  # bottom

        # grid weight
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        # row 0: productions / parse table header (fixed)
        self.rowconfigure(0, weight=0)
        # row 1: parse table content (stretch)
        self.rowconfigure(1, weight=1)
        # row 2: input panel (fixed)
        self.rowconfigure(2, weight=0)
        # row 3: result label (fixed)
        self.rowconfigure(3, weight=0)
        # row 4: parsing trace (stretch)
        self.rowconfigure(4, weight=1)

    def _init_production_rules(self):
        # Left: productions
        self.production_table = ProductionsPanel(self, relief="sunken")
        self.production_table.grid(
            row=0, column=0, rowspan=2, sticky="nsew", padx=8, pady=8
        )

    def _init_parse_table(self):
        # Right top: parse table and load file stacked
        topframe = ttk.Frame(self)
        topframe.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        topframe.columnconfigure(0, weight=1)

        self.parse_table = ParseTablePanel(topframe)
        self.parse_table.grid(row=0, column=0, sticky="nsew", pady=(8, 0))

        self.load_file = LoadFileWidget(topframe, load_command=self._on_load)
        self.load_file.grid(row=1, column=0, sticky="ew")
        self.load_file.update_filename(self.file_name)

    def _init_input_panel(self):
        # Middle: input
        self.input_panel = InputPanel(self, parse_command=self._on_input_parse)
        self.input_panel.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
        )

    def _init_result_panel(self):
        # Under input: result label
        self.result_label = ttk.Label(
            self,
            text="PARSING:",
            font=("TkDefaultFont", 12, "bold"),
        )
        self.result_label.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=8,
            pady=(0, 0),
        )

    def _init_parse_trace(self):
        # Bottom: parsing trace
        self.trace = ParsingTracePanel(self, relief="sunken")
        self.trace.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=8,
            pady=8,
        )

    def _on_load(self):
        """
        Open a `.prod` file and look for the corresponding `.ptbl` file in the
        same directory and store its pointers.
        """
        prod_stream = fd.askopenfile(
            "r",
            defaultextension=".prod",
            filetypes=[("Production rules files", "*.prod")],
        )

        # if no file selected
        if prod_stream is None:
            return

        prod_path = Path(prod_stream.name)
        ptbl_path = prod_path.parent / (prod_path.stem + ".ptbl")

        # if .ptbl not found
        if not ptbl_path.is_file():
            self.file_name = self.NO_FILE
            self.load_file.update_filename(
                (
                    self.NO_FILE
                    + f" (No corresponding `.ptbl` found for {prod_path.name})"
                )
            )
            return

        self.file_name = prod_path.name
        ptbl_stream = ptbl_path.open("r")

        self.production_table.load_productions(prod_stream)
        self.production_table.set_productions()

        self.parse_table.load_table(
            ptbl_stream,
            self.production_table.productions,
        )
        self.parse_table.set_table()

        self.load_file.update_filename(self.file_name)

    def _on_input_parse(self):
        self.trace.clear()

        if getattr(self.production_table, "productions", None) is None:
            self.trace.append("", "$", "ERROR: No production table found.")
            return

        input_text = self.input_panel.get_text().strip()
        seq = create_parsing_steps_table(
            self.parse_table.parse_table, input_text
        )

        for row in seq:
            self.trace.append(*row)

        # write output file
        output_basename = self.file_name.rstrip(".prod")
        create_file(seq, output_basename)
        # determine parsing result by looking at the last non-empty action.
        last_action = ""
        for step in reversed(seq):
            a = (step[2] or "").strip()
            if a:
                last_action = a
                break

        if last_action == "Match $":
            out_filename = f"test_{output_basename}.prsd"
            self.result_label.config(
                text=f"Valid. Please see the {out_filename}"
            )
        else:
            reason = last_action or "Unknown error"
            self.result_label.config(text=f"INVALID: {reason}")


def main():
    app = ParserApp()
    app.mainloop()


if __name__ == "__main__":
    main()
