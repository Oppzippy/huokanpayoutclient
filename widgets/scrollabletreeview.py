import tkinter
from tkinter import ttk


class ScrollableTreeview(tkinter.Frame):
    def __init__(
        self,
        master,
        columns,
    ) -> None:
        super().__init__(master=master)
        self.tree_view = ttk.Treeview(self, columns=columns, show="headings")
        self.tree_view.pack(side="left", fill="both", expand=True)

        self.scroll_bar = ttk.Scrollbar(
            self, orient="vertical", command=self.tree_view.yview
        )
        self.scroll_bar.pack(side="right", fill="y")
        self.tree_view.configure(yscrollcommand=self.scroll_bar.set)
