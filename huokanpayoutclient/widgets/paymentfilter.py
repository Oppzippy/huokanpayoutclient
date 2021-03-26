import tkinter
from tkinter import ttk


class PaymentFilter(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._set_up_grid()
        self._create_widgets()

    def _set_up_grid(self):
        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2)
        self.columnconfigure(0)
        self.columnconfigure(1, weight=1)

    def _create_widgets(self):
        self._sender_realm_label = ttk.Label(self, text="Realm")
        self._sender_realm_label.grid(row=0, column=0, sticky=tkinter.E)
        self._sender_realm_entry = ttk.Entry(self)
        self._sender_realm_entry.grid(row=0, column=1, sticky=tkinter.E + tkinter.W)

        self._sender_name_label = ttk.Label(self, text="Sender Name")
        self._sender_name_label.grid(row=1, column=0, sticky=tkinter.E)
        self._sender_name_entry = ttk.Entry(self)
        self._sender_name_entry.grid(row=1, column=1, sticky=tkinter.E + tkinter.W)

        self._recipient_name_label = ttk.Label(self, text="Recipient Name")
        self._recipient_name_label.grid(row=2, column=0, sticky=tkinter.E)
        self._recipient_name_entry = ttk.Entry(self)
        self._recipient_name_entry.grid(row=2, column=1, sticky=tkinter.E + tkinter.W)

    def sender_realm(self):
        return self._sender_realm_entry.get()

    def sender_name(self):
        return self._sender_name_entry.get()

    def recipient_name(self):
        return self._recipient_name_entry.get()
