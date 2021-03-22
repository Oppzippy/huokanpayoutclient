import tkinter
import locale
from resources import get_resource_path
from huokanwindow import HuokanWindow

locale.setlocale(locale.LC_ALL, "")

root = tkinter.Tk()
root.minsize(300, 200)
root.iconbitmap(get_resource_path("logo.ico"))
window = HuokanWindow(master=root)
root.mainloop()
