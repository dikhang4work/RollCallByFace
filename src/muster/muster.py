from threading import Thread
import tkinter
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
sampleNum = 0

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
    global photo, canvas, window__, data__, sampleNum
    while (True):
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
                    cv2.putText(frame, str(profile[1]) + ", Year: " + str(profile[2]), (x + 10, y + h + 30), fontface, 1,
                                (0, 255, 0), 2)

            else:
                cv2.putText(frame, "Unknown", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2image = cv2.resize(frame, dsize=None, fx=1, fy=1) 
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        photo = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

def main(window, frame):
    global canvas, window__
    
    if window__ is None:
        window__ = window
    if canvas is None:
        canvas = tkinter.Canvas(frame, width=600, height=400)
        canvas.grid(row=0, column=0)
    show_frame()
    

def run(window, frame):
    
    thread = Thread(target=main, args=(window, frame))
    thread.start()
   
