import tkinter
import locale
from huokanwindow import HuokanWindow

locale.setlocale(locale.LC_ALL, "")

root = tkinter.Tk()
root.minsize(300, 200)
root.iconbitmap("logo.ico")
window = HuokanWindow(master=root)
root.mainloop()
