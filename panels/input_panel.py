"""Input panel: contains the INPUT label, entry field and a Parse button."""

from tkinter import ttk


class InputPanel(ttk.Frame):
    def __init__(self, parent, parse_command=None, **kwargs):
        super().__init__(parent, **kwargs)
        lbl = ttk.Label(self, text="INPUT")
        self.entry = ttk.Entry(self)
        self.parse_btn = ttk.Button(self, text="Parse", command=self._on_parse)

        lbl.grid(row=0, column=0, sticky="w")
        self.entry.grid(row=0, column=1, sticky="ew", padx=6)
        self.parse_btn.grid(row=0, column=2, padx=(6, 0))

        self.columnconfigure(1, weight=1)

        self._external_parse = parse_command

    def _on_parse(self):
        text = self.entry.get()
        if callable(self._external_parse):
            self._external_parse(text)

    def get_text(self):
        return self.entry.get()

    def set_text(self, text: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, text)
