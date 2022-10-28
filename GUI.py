from ctypes import resize
from itertools import count
from sre_parse import State
import threading
import tkinter as tk
from unicodedata import name
from src.control.BtnAdd import run as btnAdd
from src.control.GUI import exit, getALLStudent
from src.muster.muster import run as muster


window = tk.Tk()
window.columnconfigure(0, minsize=10)
window.rowconfigure([0, 1], minsize=10)
window.title("GUI")
window.geometry("1200x600+100+100")
window.configure(bg="white")


# set default all elements to be background color (white)
window.option_add("*Label.Background", "white")
window.option_add("*Entry.Background", "white")
window.option_add("*Frame.Background", "white")
window.option_add("*Button.Background", "white")
window.option_add("*Radiobutton.Background", "white")
window.option_add("*Message.Background", "white")


# set default all text color to be black
window.option_add("*Button.Foreground", "black")
window.option_add("*Label.Foreground", "black")
window.option_add("*Entry.Foreground", "black")

# frame for the title
frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1, width=200)
frame.grid(row=0, column=0, sticky="nsew")
frame.columnconfigure(0, minsize=10)
frame.rowconfigure([0, 1], minsize=10)

# create a frame for content with size 800x600 and place it at (400, 0)
frame_content = tk.Frame(master=window, width=900, height=600)
frame_content.grid(row=0, column=1, rowspan=3, sticky="nsew")
frame_content.columnconfigure(0, minsize=10)
frame_content.rowconfigure([0, 1], minsize=10)

thread_learning = None
thread_muster = None

lstStudent = getALLStudent()


def onclickMuster(frame):
    global window, button__muster, button__add
    frame.destroy()

    frame = tk.Frame(master=window, width=900, height=600)
    frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
    frame.columnconfigure(0, minsize=10)
    frame.rowconfigure([0, 1], minsize=10)

    button__muster['state'] = 'disabled'
    button__add['state'] = 'normal'
    
    window.update()
    muster(window, frame, thread_muster)

def onclickAdd(frame):
    global window, button__muster, button__add
    frame.destroy()

    frame = tk.Frame(master=window, width=900, height=600)
    frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
    frame.columnconfigure(0, minsize=10)
    frame.rowconfigure([0, 1], minsize=10)

    button__muster['state'] = 'normal'
    button__add['state'] = 'disabled'

    window.update()
    btnAdd(window, frame, thread_learning)


label__class = tk.Label(
    master=frame,
    text="Lớp: DHKTPM14",
    width=20,
    height=2,
    font=("Arial", 20)
)
label__class.grid(row=0, column=0, sticky="nsew")

label__class_size = tk.Label(
    master=frame,
    text="Số lượng: "+str(len(lstStudent)),
    width=20,
    height=2,
    font=("Arial", 16)
)
label__class_size.grid(row=2, column=0, sticky="nsew")


button__muster = tk.Button(
    master=frame,
    text="Điểm danh",
    width=20,
    height=2,
    font=("Arial", 16),
    command= lambda: onclickMuster(frame_content)
)
button__muster.grid(row=5, column=0, sticky="nsew")
    
button__add = tk.Button(
    master=frame,
    text="Thêm",
    width=20,
    height=2,
    font=("Arial", 16),
    command=lambda: onclickAdd(frame_content)
)
button__add.grid(row=6, column=0, sticky="nsew")

button__exit = tk.Button(
    master=frame,
    text="Thoát",
    width=20,
    height=2,
    font=("Arial", 16),
    command=lambda: exit(window)
)
button__exit.grid(row=8, column=0, sticky="nsew")


window.mainloop()