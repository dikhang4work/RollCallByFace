from ast import arg
from concurrent.futures import thread
from curses import window
from time import sleep, time
from tkinter import Canvas, Frame, Tk
import tkinter
import cv2
from PIL import Image, ImageTk
from threading import Thread
import numpy as np
import sqlite3
import os
import json
import sys
from src.trainModel.TrainModel import run as trainModel

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
video.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

photo = None
canvas = None
window__ = None
data__ = None
sampleNum = 0
label_status__ = None

def show_frame():
    global canvas, photo, window__, data__, sampleNum, label_status__
    data = json.loads(data__)
    while True:
        _, frame = video.read() # read the video frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)


        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if not os.path.exists('src/dataSet'):
                os.makedirs('src/dataSet')

            sampleNum += 1
            name = 'src/dataSet/User.'+str(data['id'])+'.' +str(sampleNum) +'.jpg'


            cv2.imwrite(name, gray[y: y + h, x: x + w])
            cv2.putText(frame, 'Done : ' + str((sampleNum*100)/200) + "%", (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
            # cv2.imshow('frame 123', frame)
            
            cv2.waitKey(1)
                


        frame = cv2.resize(frame, dsize=None, fx=1, fy=1) # resize the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB

        photo = ImageTk.PhotoImage(image=Image.fromarray(frame)) # convert to PIL image
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW) # put the image on the canvas
        label_status__.config(text="Đang quét khuôn mặt __ " + str((sampleNum*100)/200) + "%")
        if sampleNum > 200:
            canvas.destroy()
            break

def main(window, frame, data, label_status):
    global canvas, window__, data__, label_status__
    if canvas is None:
        canvas = Canvas(frame, width=600, height=400)
        canvas.grid(row=0, column=0)
    if window__ is None:
        window__ = window
    if data__ is None:
        data__ = data
    if label_status__ is None:
        label_status__ = label_status
    show_frame()
    frame.destroy()
    frame = Frame(master=window, width=900, height=600)
    frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
    frame.columnconfigure(0, minsize=10)
    frame.rowconfigure([0, 1], minsize=10)
    trainModel(frame)

def insertOrUpdateStudent(data):

    conn = sqlite3.connect("Student.db")
    cmd = "SELECT * FROM Student WHERE ID = '"+ str(data["id"])+"'"
    
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 0:
        cmd = "INSERT INTO Student(ID, Name, Class, Birthday, Sex) VALUES('" + str(data["id"]) + "','" + str(data["name"]) + "','"+ str(data["class"]) + "','" + str(data["birthday"]) +"','" + str(data['sex']) + "')"
    else:
        cmd = "UPDATE Student SET Name = '" + str(data["name"]) + "', Class = '" + str(data["class"]) +  "', Birthday = '" + str(data["birthday"]) + "', Sex = '" + str(data["sex"]) +  "' WHERE ID = " + str(data["id"])
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    conn.close()



def run(window, frame, data):
    sys.setrecursionlimit(100000)
    

    label_status = tkinter.Label(frame, 
    text="Đang quét khuôn mặt __ 0%", 
    font=("Arial", 20), 
    fg="blue")

    thread = Thread(target=main, args=(window,frame, data, label_status))
    thread.start()

    label_status.grid(row=1, column=0)
    insertOrUpdateStudent(json.loads(data))

