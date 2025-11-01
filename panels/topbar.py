"""Top bar for the parser UI.

Contains a small label and Load / Parse buttons to mimic the top-right area
in the reference layout.
"""

from tkinter import ttk


class TopBar(ttk.Frame):
    def __init__(self, parent, load_command=None, parse_command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.loaded_label = ttk.Label(self, text="LOADED: rules.prod")
        self.load_button = ttk.Button(self, text="Load", command=load_command)
        self.parse_button = ttk.Button(
            self, text="Parse", command=parse_command
        )

        self.loaded_label.grid(row=0, column=0, sticky="w")
        self.load_button.grid(row=0, column=1, padx=(8, 4))
        self.parse_button.grid(row=0, column=2)
