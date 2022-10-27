import cv2
import numpy as np
import os
import sqlite3
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+ "haarcascade_frontalface_default.xml")
model = cv2.face.LBPHFaceRecognizer_create()

model.read('../model/modelResult.yml')

def getProfile(id):
    conn = sqlite3.connect('../../Student.db')
    query = "SELECT * FROM Student WHERE ID="+str(id)
    cursor = conn.execute(query)
    
    profile=None
    
    for row in cursor:
        profile = row
        
    conn.close()
    return profile

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

fontface = cv2.FONT_HERSHEY_SIMPLEX

while(True):
    
    ret , frame = cap.read()
    
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    faces=face_cascade.detectMultiScale(gray)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0, 255, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        
        id, confidence = model.predict(roi_gray)

        if confidence <90:
            profile = getProfile(id)
            if(profile != None):
                # cv2.putText(frame, id, (10,30), fontface, 1, (0, 0, 255), 2)
                cv2.putText(frame, str(profile[1])+", Year: "+ str(profile[2]), (x+10, y+h+30), fontface, 1, (0,255,0) ,2)
              
        else:
            cv2.putText(frame, "Unknown", (x+10, y+h+30), fontface, 1, (0,0,255) ,2)
            
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

def run():
    pass