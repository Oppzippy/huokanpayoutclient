import tkinter
from tkinter import ttk


class ScrollableTreeview(tkinter.Frame):
    def __init__(
        self,
        master,
        columns,
    ) -> None:
        super().__init__(master=master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1)
        self.rowconfigure(0, weight=1)

        self.tree_view = ttk.Treeview(self, columns=columns, show="headings")
        self.tree_view.grid(
            row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W
        )

        self.scroll_bar = ttk.Scrollbar(
            self, orient="vertical", command=self.tree_view.yview
        )
        self.scroll_bar.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)
        self.tree_view.configure(yscrollcommand=self.scroll_bar.set)
