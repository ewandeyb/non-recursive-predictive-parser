"""Parse table panel: simple grid-like view for parse table.

Uses a Treeview where the first column is the nonterminal and the other
columns are terminals. This is a lightweight placeholder that can be fed a
2D mapping.
"""

from tkinter import ttk

from parsers.parse_table import ParseTable


class ParseTablePanel(ttk.Frame):
    def __init__(self, parent, terminals=None, **kwargs):
        super().__init__(parent, **kwargs)

    def _configure_treeview(self):
        """
        Create the table for displaying
        """

        terminals = self.parse_table.terminals
        cols = ["NT"] + terminals
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=60, anchor="center")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def load_table(self, ptbl_stream, production_rules):
        with ptbl_stream as iostream:
            self.parse_table = ParseTable(iostream, production_rules)

        self._configure_treeview()

    def set_table(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        for non_terminal, pointers in self.parse_table.table.items():
            row = [non_terminal]

            # since the parse_table is a sparse matrix, we have to iterate on
            # the terminals
            for terminal in self.parse_table.terminals:
                value = pointers.get(terminal, "")
                row.append(str(value))

            self.tree.insert("", "end", values=row)
