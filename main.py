from tkinter import *
from tkinter import messagebox
top = Tk()

C = Canvas(top, bg="blue", height=150, width=100)
filename = PhotoImage(file = "t67.png")
background_label = Label(top, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

C.pack()


import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font


window = top

window.title("Face_Recogniser")
window.geometry('3500x2000')

dialog_title = 'QUIT'
dialog_text = 'quit ?'
 
window.configure(background='#7F38EC')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,bg="#C5CCD4"  ,fg="blue"  ,width=45  ,height=1,font=('times', 22, 'italic bold underline')) 
message.place(x=600, y=80)
label = tk.Label(window, text="Enter ID",width=10  ,height=1  ,fg="blue"  ,bg="#C5CCD4" ,font=('times', 15, ' bold ') ) 
label.place(x=600, y=200)

textinput = tk.Entry(window,width=30,bd=10  ,bg="#C5CCD4" ,fg="WHITE",font=('times', 15, ' bold '))
textinput.place(x=800, y=205)

label2 = tk.Label(window, text="Enter Name",width=10  ,fg="blue"  ,bg="#C5CCD4"    ,height=1 ,font=('times', 15, ' bold ')) 
label2.place(x=600, y=300)

textinput2 = tk.Entry(window,width=30,bd=10 ,bg="#C5CCD4"  ,fg="WHITE",font=('times', 15, ' bold ')  )
textinput2.place(x=800, y=305)

label3 = tk.Label(window, text="Notification : ",width=10  ,fg="blue"  ,bg="#C5CCD4"  ,height=1 ,font=('times', 15, ' bold underline ')) 
label3.place(x=600, y=400)

message = tk.Label(window, text="" ,bg="#C5CCD4"  ,fg="blue"  ,width=30  ,height=1, activebackground = "#C5CCD4" ,font=('times', 15, ' bold ')) 
message.place(x=800, y=400)

label3 = tk.Label(window, text="Attendance : ",width=10  ,fg="blue"  ,bg="#C5CCD4"  ,height=2 ,font=('times', 15, ' bold  underline')) 
label3.place(x=600, y=640)


message2 = tk.Label(window, text="" ,fg="blue"   ,bg="#C5CCD4",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=800, y=640)
 
def clear():
    textinput.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    textinput2.delete(0, 'end')    
    res = ""
    message.configure(text= res)
def ravi():
    import m1
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(textinput.get())
    name=(textinput2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captublue face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    #recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    
    
    
    faces=[]
    
    Ids=[]
    
    for imagePath in imagePaths:
        
        pilImage=Image.open(imagePath).convert('L')
        
        imageNp=np.array(pilImage,'uint8')
        
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    message2.configure(text= res)
  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=1 ,activebackground = "blue" ,font=('times', 15, ' bold '))
clearButton.place(x=1200, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=1, activebackground = "blue" ,font=('times', 15, ' bold '))
clearButton2.place(x=1200, y=300)    
takeImg = tk.Button(window, text="Input", command=TakeImages  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=2, activebackground = "blue" ,font=('times', 15, ' bold '))
takeImg.place(x=700, y=450)
trainImg = tk.Button(window, text="Image Traning", command=TrainImages  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=2, activebackground = "blue" ,font=('times', 15, ' bold '))
trainImg.place(x=900, y=450)
trackImg = tk.Button(window, text="Image Tracking", command=TrackImages  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=2, activebackground = "blue" ,font=('times', 15, ' bold '))
trackImg.place(x=1100, y=450)
#quitWindow1 = tk.Button(window, text="Quit", command=window.destroy  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=2, activebackground = "blue" ,font=('times', 15, ' bold '))
#quitWindow1.place(x=1000, y=550)
#quitWindow = tk.Button(window, text="Mail", command=ravi  ,fg="blue"  ,bg="#C5CCD4"  ,width=10  ,height=2, activebackground = "blue" ,font=('times', 15, ' bold '))
#quitWindow.place(x=800, y=550)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Prudhvi","", "TEAM", "superscript")
copyWrite.configure(state="disabled",fg="blue"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)
 
window.mainloop()
