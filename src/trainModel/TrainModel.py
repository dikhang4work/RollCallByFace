from cProfile import label
from tkinter import Label
import numpy as np
import os
from PIL import Image
import cv2

model = cv2.face.LBPHFaceRecognizer_create()
path= 'src/dataSet'

label__notify = None

def getImageWithId(path):
    global label__notify
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    
    faces=[]
    IDs=[]
    sampleNum = 0
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        
        print(faceNp)
        print(os.path.split(imagePath)[1].split('.'))
        #split to get ID of the image
        ID=int(os.path.split(imagePath)[1].split('.')[1])
        
        faces.append(faceNp) 
        IDs.append(ID)
        sampleNum = sampleNum + 1
        if label__notify is not None:
            label__notify.configure(text="Đang huấn luyện... " + str(round((sampleNum/len(imagePaths))*100,2)) + "%")
        cv2.waitKey(10)

    return IDs, faces



def training():
    Ids,faces=getImageWithId(path)

    # trainning
    model.train(faces,np.array(Ids))

    if not os.path.exists('src/model'):
        os.makedirs('src/model')

    model.save('src/model/modelResult.yml')  

def run(frame):
    global label__notify
    label__notify = Label(frame,
                            text="Quét khuôn mặt thành công",
                            font=("Arial", 20),
                            width=20,
                            height=2)
    label__notify.grid(row=0, column=0, sticky="nsew")

    if label__notify is  None:
        label__notify_2 = Label(frame,
                                text="Đang huấn luyện...",
                                font=("Arial", 20),
                                width=20,
                                height=2)
        label__notify_2.grid(row=1, column=0, sticky="nsew")


    training()

                              