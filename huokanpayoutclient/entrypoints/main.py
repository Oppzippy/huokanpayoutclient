import tkinter
import locale
from huokanpayoutclient.util.resources import get_resource_path
from huokanpayoutclient.widgets.huokanwindow import HuokanWindow

locale.setlocale(locale.LC_ALL, "")


def main():
    root = tkinter.Tk()
    root.minsize(300, 200)
    p = get_resource_path("logo.ico")
    root.iconbitmap(p)
    HuokanWindow(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
