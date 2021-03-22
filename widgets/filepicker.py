import tkinter
from tkinter import ttk
from tkinter import filedialog
from enum import Enum, auto


class FilePickerType(Enum):
    FILE = auto()
    DIRECTORY = auto()


class FilePicker(tkinter.Frame):
    def __init__(
        self,
        master,
        type: FilePickerType = FilePickerType.FILE,
        label=None,
        command: callable = None,
    ):
        super().__init__(master)
        self.path = ""
        self._type = type
        self._label = label
        self._command = command
        self._set_up_grid()
        self._create_widgets()

    def set_path(self, path: str):
        self.path = path
        self._path_entry_text.set(path)

    def _set_up_grid(self):
        self.columnconfigure(0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2)
        self.rowconfigure(0)

    def _create_widgets(self):
        if self._label:
            self._path_label = ttk.Label(self, text=self._label)
            self._path_label.grid(row=0, column=0)

        self._path_entry_text = tkinter.StringVar()
        self._path_entry_text.set(self.path)
        self._path_entry = ttk.Entry(
            self, textvariable=self._path_entry_text, state="readonly"
        )
        self._path_entry.grid(row=0, column=1, sticky=tkinter.E + tkinter.W)

        self._path_button = ttk.Button(
            self, text="Choose", command=self._path_button_click
        )
        self._path_button.grid(row=0, column=2)

    def _path_button_click(self):
        if self._type == FilePickerType.FILE:
            self.path = filedialog.askopenfilename()
        else:
            self.path = filedialog.askdirectory()
        self._path_entry_text.set(self.path)
        if self._command:
            self._command(self.path)
