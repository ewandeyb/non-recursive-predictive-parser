"""Parsing trace panel: shows the stack / input buffer / action columns.

We implement this as a Treeview for ease of adding rows dynamically.
"""

from tkinter import ttk


class ParsingTracePanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        cols = ("Stack", "Input Buffer", "Action")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="w")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def append(self, stack: str, input_buffer: str, action: str):
        self.tree.insert("", "end", values=(stack, input_buffer, action))

    def clear(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
