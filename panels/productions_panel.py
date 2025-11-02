"""Productions panel: shows the list of grammar productions.

This implements a small Treeview with columns ID / NT / P and a helper to set
productions programmatically.
"""

from tkinter import ttk

from parsers.production_rules import load_prod_rules


class ProductionsPanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tree = ttk.Treeview(
            self, columns=("ID", "NT", "P"), show="headings", height=8
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("NT", text="NT")
        self.tree.heading("P", text="P")
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("NT", width=50, anchor="w")
        self.tree.column("P", width=220, anchor="w")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def load_productions(self, prod_stream):
        with prod_stream as iostream:
            self.productions = load_prod_rules(iostream)

    def set_productions(self):
        # clear
        for i in self.tree.get_children():
            self.tree.delete(i)

        for i in range(1, len(self.productions)):
            prod = self.productions[i]
            assert prod  # for type checking, prod should never be None

            self.tree.insert("", "end", values=[i, prod.name, prod.rule])
