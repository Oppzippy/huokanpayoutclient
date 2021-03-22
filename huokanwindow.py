import tkinter
from tkinter import ttk, messagebox
from widgets.scrollabletreeview import ScrollableTreeview
from widgets.filepicker import FilePicker, FilePickerType
from widgets.paymentfilter import PaymentFilter
from huokanpayout.payoutsearch import search_payouts, InvalidWoWDirectoryException


class HuokanWindow(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.results = []
        self._prev_sort_column = None
        self._prev_sort_reverse = None
        self.winfo_toplevel().title("Huokan Payout Client")
        self._set_up_grid()
        self._create_widgets()

    def _set_up_grid(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.grid(sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2)
        self.rowconfigure(3, weight=1)

    def _create_widgets(self):
        self._wow_path_picker = FilePicker(
            self, label="WoW Folder", type=FilePickerType.DIRECTORY
        )
        self._wow_path_picker.set_path(
            "C:/Program Files (x86)/World of Warcraft/_retail_"
        )
        self._wow_path_picker.grid(row=0, column=0, sticky=tkinter.E + tkinter.W)
        self._payment_filter = PaymentFilter(self)
        self._payment_filter.grid(row=1, column=0, sticky=tkinter.E + tkinter.W)
        self._search_button = ttk.Button(self, text="Search", command=self.search)
        self._search_button.grid(row=2, column=0, sticky=tkinter.E + tkinter.W)

        self._scrollable_results_view = ScrollableTreeview(
            self, columns=("timestamp", "name", "gold")
        )
        self._scrollable_results_view.grid(
            row=3, column=0, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S
        )
        self._results_view = self._scrollable_results_view.tree_view
        self._results_view.heading(
            "#1",
            text="Timestamp",
            command=lambda: self.sort_results("timestamp", True),
        )
        self._results_view.heading(
            "#2", text="Name", command=lambda: self.sort_results("name", False)
        )
        self._results_view.heading(
            "#3",
            text="Gold",
            command=lambda: self.sort_results("gold", True),
        )

    def search(self):
        try:
            unsorted_results = search_payouts(
                self._wow_path_picker.path, self._payment_filter.name()
            )
            self.results = sorted(
                unsorted_results, reverse=True, key=lambda result: result["timestamp"]
            )
            self.display_results()
        except InvalidWoWDirectoryException:
            messagebox.showerror(
                self.winfo_toplevel().title(),
                "No HuokanPayout.lua SavedVariables found. Make sure the _retail_ directory is selected.",
            )

    def sort_results(self, col: str, reverse: bool = False):
        if col == self._prev_sort_column:
            reverse = not self._prev_sort_reverse
        self._prev_sort_column = col
        self._prev_sort_reverse = reverse

        self.results = sorted(
            self.results, key=lambda result: result[col], reverse=reverse
        )
        self.display_results()

    def display_results(self):
        self._results_view.delete(*self._results_view.get_children())
        for result in self.results:
            timestamp = result["timestamp"].strftime("%c")
            self._results_view.insert(
                "", "end", values=(timestamp, result["name"], result["gold"])
            )
