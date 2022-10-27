from ctypes import resize
import tkinter as tk
from src.control.BtnAdd import run as btnAdd
from src.control.GUI import exit
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
    text="Số lượng: 30",
    width=20,
    height=2,
    font=("Arial", 16)
)
label__class_size.grid(row=2, column=0, sticky="nsew")

label__class_present = tk.Label(
    master=frame,
    text="Có mặt: 0",
    width=20,
    height=2,
    font=("Arial", 16),
    fg="red"
)
label__class_present.grid(row=3, column=0, sticky="nsew")


button__muster = tk.Button(
    master=frame,
    text="Điểm danh",
    width=20,
    height=2,
    font=("Arial", 16),
    command= lambda: muster(window, frame_content)
)
button__muster.grid(row=5, column=0, sticky="nsew")
    
button__add = tk.Button(
    master=frame,
    text="Thêm",
    width=20,
    height=2,
    font=("Arial", 16),
    command=lambda: btnAdd(window,frame_content)
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