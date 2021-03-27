import tkinter
from tkinter import messagebox
import traceback
import locale
from huokanpayoutclient.util.resources import get_resource_path
from huokanpayoutclient.widgets.huokanwindow import HuokanWindow

locale.setlocale(locale.LC_ALL, "")


def main():
    root = tkinter.Tk()
    root.minsize(300, 200)
    root.iconbitmap(get_resource_path("logo.ico"))

    window = HuokanWindow(master=root)
    window.update()

    def alert_error(*args):
        err = traceback.format_exception(*args)
        messagebox.showerror(window.winfo_toplevel().title(), err)

    root.report_callback_exception = alert_error

    root.mainloop()


if __name__ == "__main__":
    main()
