import tkinter
import locale
from util.resources import get_resource_path
from widgets.huokanwindow import HuokanWindow

locale.setlocale(locale.LC_ALL, "")


def main():
    root = tkinter.Tk()
    root.minsize(300, 200)
    root.iconbitmap(get_resource_path("logo.ico"))
    HuokanWindow(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
