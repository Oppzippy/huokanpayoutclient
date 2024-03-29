import tkinter
from tkinter import ttk, messagebox
from huokanpayoutclient.huokanpayout.payoutsearch import (
    search_payouts,
    InvalidWoWDirectoryException,
)
from .scrollabletreeview import ScrollableTreeview
from .filepicker import FilePicker, FilePickerType
from .paymentfilter import PaymentFilter


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
        self.rowconfigure(3)
        self.rowconfigure(4)
        self.rowconfigure(5, weight=1)

    def _create_widgets(self):
        self._wow_path_picker = FilePicker(
            self, label="WoW Folder", type_=FilePickerType.DIRECTORY
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
            self, columns=("timestamp", "realm", "sender", "recipient", "gold")
        )
        self._scrollable_results_view.grid(
            row=5, column=0, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S
        )
        self._results_view = self._scrollable_results_view.tree_view
        self._results_view.heading(
            "#1",
            text="Timestamp",
            command=lambda: self.sort_results("timestamp", True),
        )
        self._results_view.heading(
            "#2", text="Realm", command=lambda: self.sort_results("senderRealm", False)
        )
        self._results_view.heading(
            "#3", text="Sender", command=lambda: self.sort_results("senderName", False)
        )
        self._results_view.heading(
            "#4",
            text="Recipient",
            command=lambda: self.sort_results("recipientName", False),
        )
        self._results_view.heading(
            "#5",
            text="Gold",
            command=lambda: self.sort_results("gold", True),
        )

        self._context_menu = tkinter.Menu(self, tearoff=0)
        self._context_menu.add_command(
            label="Copy Timestamp to Clipboard",
            command=lambda: self._copy_to_clipboard("timestamp"),
        )
        self._context_menu.add_command(
            label="Copy Realm to Clipboard",
            command=lambda: self._copy_to_clipboard("realm"),
        )
        self._context_menu.add_command(
            label="Copy Sender Name to Clipboard",
            command=lambda: self._copy_to_clipboard("sender"),
        )
        self._context_menu.add_command(
            label="Copy Recipient Name to Clipboard",
            command=lambda: self._copy_to_clipboard("recipient"),
        )
        self._context_menu.add_command(
            label="Copy Gold to Clipboard",
            command=lambda: self._copy_to_clipboard("gold"),
        )

        self._results_view.bind("<Button-3>", self._show_context_menu)

    def search(self):
        try:
            unsorted_results = search_payouts(
                self._wow_path_picker.path,
                sender_realm=self._payment_filter.sender_realm(),
                sender_name=self._payment_filter.sender_name(),
                recipient_name=self._payment_filter.recipient_name(),
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
            self.results, key=lambda result: result.get(col, ""), reverse=reverse
        )
        self.display_results()

    def display_results(self):
        self._results_view.delete(*self._results_view.get_children())
        for result in self.results:
            timestamp = result["timestamp"].strftime("%c")
            self._results_view.insert(
                "",
                "end",
                values=(
                    timestamp,
                    result.get("senderRealm", ""),
                    result.get("senderName", ""),
                    result["recipientName"],
                    result["gold"],
                ),
            )

    def _show_context_menu(self, event):
        self._results_view.selection_set(self._results_view.identify_row(event.y))
        self._context_menu.post(event.x_root, event.y_root)

    def _copy_to_clipboard(self, column):
        (selected_row) = self._results_view.selection()
        column_value = self._results_view.set(selected_row, column)
        self.clipboard_clear()
        self.clipboard_append(column_value)
