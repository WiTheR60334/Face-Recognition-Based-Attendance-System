from tkinter import *
import tkinter.messagebox as tmsg
import os,csv

#Paths......
AU_Icon = "C:\\Users\\romir\\OneDrive\\Desktop\\Project\\au.ico"
Student_Details="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Student details.csv"
Students="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Students"
Haarcascade_Frontal_Face_Default="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\haarcascade_frontalface_default.xml"
AU1_PNG="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\au1.png"
Register_PNG="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\UI_Image\\register.png"
Attendace_PNG="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\UI_Image\\attendance.png"
Verify_PNG="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\UI_Image\\verifyy.png"

#Creating GUI
root = Tk()
root.title("Attendance GUI")
root.geometry("1520x730")
root.minsize(1520,730)
root.wm_iconbitmap(AU_Icon)
root.config(background="black")

def new_student():

    if not os.path.exists(Student_Details):
        f = open(Student_Details,"w",newline="")#Creating Student details.csv for storing the data
        writer=csv.writer(f)
        writer.writerow(["Enrollment No. , Name"])
        f.close()
    else:
        pass #If csv is arleady created, the pass this statemnt 

    root1=Toplevel(root)#Creating new root
    root1.attributes("-topmost", True)#To keep tkinter window on top
    root1.title("Registering New Student's Face")
    root1.wm_iconbitmap(AU_Icon)
    root1.geometry("750x550")
    root1.config(background="black")
    f1 = Frame(root1, bg = "black", borderwidth=6, relief=RIDGE)
    f1.pack(side=TOP, fill="x")
    Label(f1, text="Register New Student",bg = "black", fg="Yellow",font=("Times New Roman", 25, "bold")).pack()
    f2 = Frame(root1, bg = "black")
    f2.pack(side=LEFT, fill=BOTH)
    details=['Full Name          :','Enrollment No. :', 'Progamme         :']

    for i in range(0,len(details)):
        Label(f2, text=details[i],bg = "black", fg="Yellow",font=("Times New Roman", 25, "bold")).pack(anchor="w",padx = 20,pady=20)

    #Giving each entry box a value, store the details
    namevalue = StringVar()
    enrollvalue = StringVar()
    progvalue = StringVar()
    l1=[namevalue,enrollvalue,progvalue]

    for i in range(0,len(details)):
        Entry(root1,textvariable=l1[i], font=("Times New Roman", 25, "bold")).pack(anchor="w",padx = 20,pady=20)

    def Take_Image():
        if (namevalue.get() and enrollvalue.get() and progvalue.get()) == "":#If any value is null
            tmsg.showinfo("Fill all three details", "Please enter all the details !!!",parent=root1)
        else : 
            if not os.path.exists(Students):
                os.makedirs(Students)#Creating folder for storing student's image
            else:
                pass #pass it, if already created
              
            Same_Student= "C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Students\\"+enrollvalue.get()+".jpg"

            if not os.path.exists(Same_Student): #If new student has registered, then below code will execute
                    tmsg.showinfo("Instructions","TO TAKE YOUR IMAGE, PRESS 's' ON YOUR KEYBOARD AND TO EXIT THE CAMERA WINDOW PRESS 'q'",parent=root1) 
                    tmsg.showinfo("Sit in proper light area","Sit in proper brightness area and your face should be clear and visible",parent=root1)
                    f=open(Student_Details,"a")
                    writer = csv.writer(f)
                    writer.writerow([enrollvalue.get(), namevalue.get()])#To write enrollment no. and name in the csv file
                    f.close()
                    import cv2 as cv
                    face_cascade = cv.CascadeClassifier(Haarcascade_Frontal_Face_Default)
                    cam = cv.VideoCapture(0) #for default camera = 0, and for third party camera,use 1
                    while True:
                        _,img = cam.read()
                        gray = cv.cvtColor(img, cv.COLOR_BGR2RGB)#Converting from BGR fromat to RGB
                        cv.imshow("Take Image",img) #To show the video cam
                        
                        if cv.waitKey(1) & 0xFF == ord('s'): #For capturing image, press s
                            cv.imwrite("C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Students\\"+enrollvalue.get()+".jpg",img) #To store the image in Students folder 
                            tmsg.showinfo("Image Taken","Your details and image has been registered.",parent=root1)   
                            break 
                        if cv.waitKey(1) & 0xFF == ord('q'): #For closing the window press q
                            break
                        window_name = "Take Image"  
                        cv.namedWindow("Take Image", cv.WINDOW_NORMAL)
                        cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST,1) #To keep video window on top
                    cam.release()
                    cv.destroyAllWindows() 
            else:
                tmsg.showinfo("Student Details already exists","Student details already exists",parent=root1)

        root1.destroy() #To close window           
    Button(root1, text="Take Image",bg = "black", fg="Yellow",font=("Times New Roman", 20, "bold"),borderwidth=6, relief=RIDGE,command=Take_Image).place(x=300,y=310)

def Take_Attendance():
    root1=Toplevel(root)
    root1.attributes("-topmost", True)
    root1.title("Enter Subject")
    root1.wm_iconbitmap(AU_Icon)
    root1.geometry("550x450")
    root1.config(background="black")
    f1 = Frame(root1, bg = "black", borderwidth=6, relief=RIDGE)
    f1.pack(side=TOP, fill="x")
    Label(f1, text="Enter your Subject",bg = "black", fg="Yellow",font=("Times New Roman", 25, "bold")).pack()
    f2 = Frame(root1, bg = "black")
    f2.pack(side=LEFT, fill=BOTH)
    details=['Subject :']

    for i in range(0,len(details)):
        Label(f2, text=details[i],bg = "black", fg="Yellow",font=("Times New Roman", 25, "bold")).pack(anchor="w",padx = 20,pady=20)

    subvalue = StringVar() #Giving subject input a value
    l1=[subvalue]

    for i in range(0,len(details)):
        Entry(root1,textvariable=l1[i], font=("Times New Roman", 25, "bold")).pack(anchor="w",padx = 20,pady=20)

    def Take_Image():
        if subvalue.get() == "": #If subvalue is null
            tmsg.showinfo("Enter your Subject", "Please enter Subject !!!",parent=root1)
        else :   #To recognise your face 
            tmsg.showinfo("To quit the window","Press 'q' to exit the window",parent=root1)
            import cv2 as cv
            import face_recognition,csv,os
            import numpy as np
            from datetime import datetime
            import pandas as pd
            
            face_cascade=cv.CascadeClassifier(Haarcascade_Frontal_Face_Default)
            cam=cv.VideoCapture(0)
            list_dir=os.listdir(Students) #To make a list of all images captured
            l1=[] #Making a empty set to store all images with extension

            for i in list_dir:
                i=os.path.splitext(i)[0] #To split the extension from name of image
                l1.append(i)
            known_face_encoding=[] #Making a empty set to store all images without extension
            known_faces_names=[] #Making a empty set to store all names of images
            for i in l1:
                   i = face_recognition.load_image_file("C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Students\\"+i+".jpg") #To load the image
                   i=face_recognition.face_encodings(i)[0] #To save their encodings
                   known_face_encoding.append(i) #To append them with known_face_encoding
            for i in l1:
                known_faces_names.append(i)
            students=known_faces_names.copy() #To make another list of name

            face_locations=[]
            face_encodings=[]
            face_names=[]
            s=True
            
            present_time=datetime.now()
            current_date=present_time.strftime("%d-%m-%Y") #day-month-year
            attendance_sheets="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Attendance Sheets"
            if not os.path.exists(attendance_sheets):
                os.mkdir(attendance_sheets)
            else:
                pass    
            attendance_sheet="C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Attendance Sheets\\"+current_date + '.csv'

            if not os.path.exists(attendance_sheet):
                f=open("C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Attendance Sheets\\"+current_date + '.csv','w',newline='')#Creating Attendance Sheet
                writer=csv.writer(f)
                writer.writerow(["Enrollment No.","Name","Time","Subject"])
                f.close()
            else:
                pass    
            
            f=open("C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Attendance Sheets\\"+current_date + '.csv','a',newline='')
            linewriter=csv.writer(f)
            while True:
                _,img = cam.read()
                gray = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                faces=face_cascade.detectMultiScale(gray)
                #(255,0,0) for blue  (0,255,255) for yellow
                small_frame=cv.resize(img,(0,0),fx=0.25,fy=0.25)#resize output of webcam
                rgb_small_frame = small_frame[:,:,::-1]#brg to rgb

                if s:
                    face_locations=face_recognition.face_locations(rgb_small_frame)#This will detect the face locations in webcam 
                    face_encodings=face_recognition.face_encodings(rgb_small_frame,face_locations)#To store the data of face
                    face_names=[]

                    for face_encoding in face_encodings:
                        matches=face_recognition.compare_faces(known_face_encoding,face_encoding)#To compare face stored in known_face_encoding to webcam
                        name=""
                        face_distance=face_recognition.face_distance(known_face_encoding,face_encoding)#To get more accurate by distance
                        best_match_index=np.argmin(face_distance)#to get more precise(returns minimum index)

                        if matches[best_match_index]: 
                            name = known_faces_names[best_match_index]#to konw the name of the face     
                            a = pd.read_csv(Student_Details)
                            df=pd.DataFrame(a)
                            c=df.loc[df["Enrollment No. "]==name] #To get name of user from students details.csv using enrollment no.
                            b=c.iloc[0,1]
                            d = str(name)+'-'+str(b)
                            face_names.append(name)#to append name with the face
                            
                            for (x,y,w,h) in faces:
                                cv.rectangle(img,(x,y),(x+w,y+h),(0,255,255),5)#img, rect co-ordinates,color(bgr),pixels
                                font = cv.FONT_HERSHEY_SIMPLEX
                                cv.putText(img, str(d), (x, y-7), font, 1.0, (255,0,0), 2)#To write name on top of the rectangle

                            if name in known_faces_names:
                                if name in students:
                                    students.remove(name)#so that multiple names wont be written
                                    tmsg.showinfo("Face Matched",str(b)+" your Attendane is taken. You can exit the camera window by clicking 'q'",parent=root1)
                                    current_time=present_time.strftime("%H:%M:%S")#hour-minute-second
                                    linewriter.writerow([name,str(b),current_time,subvalue.get()]) 
                        else:
                            for (x,y,w,h) in faces:
                                cv.rectangle(img,(x,y),(x+w,y+h),(0,255,255),5)
                                font = cv.FONT_HERSHEY_SIMPLEX
                                cv.putText(img, "Face Not Matched", (x, y-7), font, 1.0, (255,0,0), 2)
                          
                root1.wm_iconbitmap(AU_Icon)  
                window_name = "attendance system"
                cv.namedWindow(window_name, cv.WINDOW_NORMAL)
                cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST, 1)        
                cv.imshow("attendance system",img)

                if cv.waitKey(1) &0xFF == ord('q'):
                    break    
            cam.release()
            cv.destroyAllWindows()
            f.close()  
        root1.destroy()                         
    Button(root1, text="Take Attendance",bg = "black", fg="Yellow",font=("Times New Roman", 15, "bold"),borderwidth=6, relief=RIDGE,command=Take_Image).place(x=250,y=140)
   
def View_Attendance():
    from datetime import datetime
    import csv
    present_time=datetime.now()
    current_date=present_time.strftime("%d-%m-%Y")
    root = Tk()
    root.wm_iconbitmap(AU_Icon)
    root.title("Your Attendance")
    root.attributes("-topmost", True)
    f1=Frame(root,bg="grey80")
    f1.pack(side=LEFT)
    r=0
    f = open("C:\\Users\\romir\\OneDrive\\Desktop\\Project\\Attendance Sheets\\"+current_date+".csv","r")
    reader=csv.reader(f)

    for row in reader:
        c=0
        for col in row:
            Label(f1,text=col,width=13,height=1,bg="white",font=("Times New Roman",15),relief=RIDGE).grid(row=r,column=c)
            c+=1
        r+=1 

    root.mainloop()

def close():
    if tmsg.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", close) #Closing the window
f1 = Frame(root, bg = "black", borderwidth=6, relief=RIDGE)
f1.pack(side=TOP, fill="x")
f2 = Frame(root, bg = "black")
f2.pack()
t1 = Label(
    f1,
    text="AHMEDABAD UNIVERSITY",
    bg="black",
    fg="Yellow",
    font=("Times New Roman", 30, "bold")
)
t1.pack()
t2 = Label(
    f2, 
    text="Welcome to the Attendance Management System using Face Recognition AI",
    bg="black",
    fg ="yellow",
    font=("Times New Roman", 25, "bold")
)
t2.grid(row=0,pady=30)
t3 = Button(
    root, 
    text="Register New Student's face",
    bg="black",
    fg ="yellow",
    font=("Times New Roman", 20, "bold"),
    borderwidth=6,relief=RIDGE,
    command=new_student
)
t3.place(x=50, y=540)
t4 = Button(
    root, 
    text="Take Attendance",
    bg="black",
    fg ="yellow",
    font=("Times New Roman", 20, "bold"),
    borderwidth=6,relief=RIDGE,
    command=Take_Attendance
)
t4.place(x=640, y=540)
t5 = Button(
    root, 
    text="View Attendance",
    bg="black",
    fg ="yellow",
    font=("Times New Roman", 20, "bold"),
    borderwidth=6,relief=RIDGE,
    command=View_Attendance
)
t5.place(x=1150, y=540)
au = PhotoImage(file=AU1_PNG)
pic = Label(image=au)
pic.place(x=440,y=8)
Image = PhotoImage(file=Register_PNG)
pic = Label(image=Image)
pic.place(x=115, y=270)
Image1 = PhotoImage(file=Attendace_PNG)
pic = Label(image=Image1)
pic.place(x=620, y=270)
Image2 = PhotoImage(file=Verify_PNG)
pic = Label(image=Image2)
pic.place(x=1150, y=270)
Button(root,text="Exit",bg="black",fg="yellow",borderwidth=6,relief=RIDGE,font=("Times New Roman", 20, "bold"),command=close).place(x=710,y=650)
root.mainloop()
