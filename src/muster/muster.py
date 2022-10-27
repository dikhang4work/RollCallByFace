from cProfile import label
from threading import Thread
import tkinter
from tkinter import messagebox
from tkinter.tix import Tree
import cv2
from PIL import Image, ImageTk
import sqlite3



face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+ "haarcascade_frontalface_default.xml")
model = cv2.face.LBPHFaceRecognizer_create()

model.read('src/model/modelResult.yml')

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)


photo = None
canvas = None
window__ = None
data__ = None

profile__ = None

label__id = None
label__name = None
label__class = None
label__birthday = None
label__sex = None

button__check = None

check = False

__present = []

def stop():
    global check, button__check, profile__

    # check profile__ is not exist in __present list if not exist then append
    if (profile__ not in __present):
        __present.append(profile__)
        check = True
        label__present = tkinter.Label(window__, text="Sinh viên đã điểm danh: " + str(len(__present)), font=("Arial", 16), fg="red")
        label__present.place(x=10, y=400)


        button__check.destroy()
    else:
        messagebox.showinfo("Thông báo", "Sinh viên đã được điểm danh")

    

def getProfile(id):
    conn = sqlite3.connect('Student.db')
    query = "SELECT * FROM Student WHERE ID="+str(id)
    cursor = conn.execute(query)
    
    profile=None
    
    for row in cursor:
        profile = row
        
    conn.close()
    return profile

fontface = cv2.FONT_HERSHEY_SIMPLEX

def show_frame():
    global photo, canvas, window__, data__, check, profile__
    global label__id, label__name, label__class, label__birthday, label__sex

    while (check == False):
        _, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            roi_gray = gray[y:y + h, x:x + w]

            id, confidence = model.predict(roi_gray)

            if confidence < 90:
                profile = getProfile(id)
                if (profile != None):
                    cv2.putText(frame, str(profile[0]), (x + 10, y + h + 30), fontface, 1,
                                (0, 255, 0), 2)
                    profile__ = profile

                    
                    label__id.config(text="Mã sinh viên: " + str(profile[0]))
                    label__name.config(text="Họ và tên: " + str(profile[1]))
                    label__class.config(text="Lớp: " + str(profile[2]))
                    label__birthday.config(text="Ngày sinh: " + str(profile[3]))
                    label__sex.config(text="Giới tính: " + str(profile[4]))
                    
            else:
                cv2.putText(frame, "Unknown", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)
        
        cv2image = cv2.resize(frame, dsize=None, fx=1, fy=1) 
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        photo = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        if check == True:
            canvas.destroy()
            break

def main(window, frame):
    global canvas, window__, check, button__check
    global label__id, label__name, label__class, label__birthday, label__sex
    if window__ is None:
        window__ = window

    canvas = tkinter.Canvas(frame, width=600, height=400)
    canvas.grid(row=0, column=0)
    check = False

    label__id = tkinter.Label(
            master=frame,
            text="Mã sinh viên",
            width=20,
            height=1,
            font=("Arial", 16)
        )
    label__id.grid(row=1, column=0, sticky="nsew")

    label__name = tkinter.Label(
            master=frame,
            text="Họ và tên",
            width=20,
            height=1,
            font=("Arial", 16)
        )
    label__name.grid(row=2, column=0, sticky="nsew")
        
    label__class = tkinter.Label(
            master=frame,
            text="Lớp",
            width=20,
            height=1,
            font=("Arial", 16)
        )
    label__class.grid(row=3, column=0, sticky="nsew")

    label__birthday = tkinter.Label(
            master=frame,
            text="Ngày sinh",
            width=20,
            height=1,
            font=("Arial", 16)
        )
    label__birthday.grid(row=4, column=0, sticky="nsew")

    label__sex = tkinter.Label(
            master=frame,
            text="Giới tính",
            width=20,
            height=1,
            font=("Arial", 16)
        )
    button__check = tkinter.Button(
                        master=frame,
                        text="Check",
                        width=20,
                        height=1,
                        font=("Arial", 16),
                        command= lambda: stop()
                    )
    button__check.grid(row=6, column=0, sticky="nsew")       

    label__sex.grid(row=5, column=0, sticky="nsew")
    show_frame()
    
    

def run(window, frame, thread ):
    thread = Thread(target=main, args=(window, frame))
    thread.start()

