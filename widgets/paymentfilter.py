import tkinter
from tkinter import ttk


class PaymentFilter(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._set_up_grid()
        self._create_widgets()

    def _set_up_grid(self):
        self.rowconfigure(0)
        self.columnconfigure(0)
        self.columnconfigure(1, weight=1)

    def _create_widgets(self):
        self._name_label = ttk.Label(self, text="Name")
        self._name_label.grid(row=0, column=0)
        self._name_entry = ttk.Entry(self)
        self._name_entry.grid(row=0, column=1, sticky=tkinter.E + tkinter.W)

    def name(self):
        return self._name_entry.get()
