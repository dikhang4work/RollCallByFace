from doctest import master
import json
from select import select
import tkinter as tk
import tkcalendar as tkc
from tkinter import messagebox
from src.control.ScanFace import run as scanFace

def selectDate(root, result, button):
    def print_sel():
        button.grid(row=4, column=2, sticky="nsew")
        result.config(text = str(cal.selection_get().strftime("%d/%m/%Y")))
        top.destroy()

    top = tk.Toplevel(root)
    cal = tkc.Calendar(
        top,
        font="Arial 14",
        selectmode='day',
        cursor="hand1", 
        year=2000, 
        month=9, 
        day=26
        )
    cal.pack(fill="both", expand=True, padx=10, pady=10)
    tk.Button(top, text="ok", command=print_sel).pack()

def handleFinish(id, name, class__, birthday, sex, window, frame, thread):
    if id == "":
        messagebox.showerror("Lỗi", "Mã sinh viên không được để trống")
        return
    idIsNumber = True
    try:
        int(id)
    except:
        idIsNumber = False
    
    if not idIsNumber:
        messagebox.showerror("Lỗi", "Mã sinh viên phải là số")
        return
        
    if name == "":
        messagebox.showerror("Lỗi", "Họ và tên không được để trống")
        return
    if class__ == "":
        messagebox.showerror("Lỗi", "Lớp không được để trống")
        return
    if birthday == "":
        messagebox.showerror("Lỗi", "Ngày sinh không được để trống")
        return
    
    temp = {
        "id": id,
        "name": name,
        "class": class__,
        "birthday": birthday,
        "sex": sex
    }
    data = json.dumps(temp)
    
    frame.destroy()
    frame = tk.Frame(master=window, width=900, height=600)
    frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
    frame.columnconfigure(0, minsize=10)
    frame.rowconfigure([0, 1], minsize=10)
    
    scanFace(window, frame, data, thread)

def run(window, frame, thread):

    sex = tk.StringVar(master=frame, value="Nam")
    label__id = tk.Label(
        master=frame,
        text="Mã sinh viên",
        width=20,
        height=2,
        font=("Arial", 16)
    )
    label__id.grid(row=1, column=0, sticky="nsew")

    entry__id = tk.Entry(
        master=frame,
        width=20,
        font=("Arial", 16)
    )
    entry__id.grid(row=1, column=1, sticky="nsew")

    label__name = tk.Label(
        master=frame,
        text="Họ và tên",
        width=20,
        height=2,
        font=("Arial", 16)
    )
    label__name.grid(row=2, column=0, sticky="nsew")
    
    entry__name = tk.Entry(
        master=frame,
        width=20,
        font=("Arial", 16)
    )
    entry__name.grid(row=2, column=1, sticky="nsew")

    label__class = tk.Label(
        master=frame,
        text="Lớp",
        width=20,
        height=2,
        font=("Arial", 16)
    )
    label__class.grid(row=3, column=0, sticky="nsew")

    entry__class = tk.Entry(
        master=frame,
        width=20,
        font=("Arial", 16)
    )

    entry__class.grid(row=3, column=1, sticky="nsew")

    label__birthday = tk.Label(
        master=frame,
        text="Ngày sinh",
        width=20,
        height=2,
        font=("Arial", 16)
    )

    label__birthday.grid(row=4, column=0, sticky="nsew")

    entry__birthday = tk.Label(
        master=frame,
        width=20,
        font=("Arial", 16)
    )

    entry__birthday.grid(row=4, column=1, sticky="nsew")


    button__birthday = tk.Button(
        master=frame,
        text="Chọn",
        width=5,
        height=1,
        font=("Arial", 16),
        command= lambda: selectDate(frame, entry__birthday, button__birthday)
    )

    button__birthday.grid(row=4, column=1, sticky="nsew")

    label__sex = tk.Label(
        master=frame,
        text="Giới tính",
        width=20,
        height=2,
        font=("Arial", 16)
    )

    label__sex.grid(row=5, column=0, sticky="nsew")

    radio__male = tk.Radiobutton(
        master=frame,
        text="Nam",
        width=5,
        height=1,
        font=("Arial", 16),
        variable = sex,
        value="Nam",
    )

    radio__male.grid(row=5, column=1, sticky="nsew")

    radio__female = tk.Radiobutton(
        master=frame,
        text="Nữ",
        width=5,
        height=1,
        font=("Arial", 16),
        variable = sex,
        value="Nữ",
    )

    radio__female.grid(row=6, column=1, sticky="nsew", rowspan=2)

    button__finish = tk.Button(
        master=frame,
        text="Bắt đầu quét khuôn mặt",
        width=20,
        height=2,
        font=("Arial", 16), 
        command= lambda: handleFinish(
            entry__id.get(),
            entry__name.get(),
            entry__class.get(),
            entry__birthday.cget('text'),
            sex.get(),
            window,
            frame, 
            thread),
    )

    button__finish.grid(row=8, column=1, sticky="nsew")