"""Parse table panel: simple grid-like view for parse table.

Uses a Treeview where the first column is the nonterminal and the other
columns are terminals. This is a lightweight placeholder that can be fed a
2D mapping.
"""

from tkinter import ttk


class ParseTablePanel(ttk.Frame):
    def __init__(self, parent, terminals=None, **kwargs):
        super().__init__(parent, **kwargs)
        terminals = terminals or ["id", "+", "*", "(", ")", "$"]
        cols = ["NT"] + terminals
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=60, anchor="center")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def set_table(self, table_rows):
        """Load table rows.

        table_rows is an iterable of sequences with same length as columns above.
        """
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in table_rows:
            self.tree.insert("", "end", values=row)
