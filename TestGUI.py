from tkinter import Canvas, Tk
import tkinter
import cv2
from PIL import Image, ImageTk



window = Tk()
window.columnconfigure(0, minsize=1)
window.rowconfigure([0, 1], minsize=1)
window.title("GUI")

#set size of window
window.geometry("1200x600+100+100")

video = cv2.VideoCapture(0)

canvas = Canvas(window, width=400, height=300)
canvas.grid(row=0, column=0)

photo = None


def show_frame():
    global canvas, photo, bw
    _, frame = video.read() # read the video frame
    frame = cv2.resize(frame, dsize=None, fx=0.2, fy=0.2) # resize the frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert to RGB
    photo = ImageTk.PhotoImage(image=Image.fromarray(frame)) # convert to PIL image
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW) # put the image on the canvas
    window.after(1, show_frame) # call the same function after 1 ms
    
    


show_frame()



window.mainloop()