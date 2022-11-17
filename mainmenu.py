import tkinter as tk
#import server as serv
from tkinter import ttk

import random
import string
import socket

from tkinter import messagebox

from threading import Thread
from threading import Event

import traceback
import customtkinter as cust

from scipy.spatial import distance as dist

from imutils.video import VideoStream
from imutils import face_utils

import imutils
import time
import dlib
import cv2


lobbyname = ""
lobbycode = ""



class GUI(cust.CTk):  #initializes root/mainmenu window

        def __init__(self):

            super().__init__()

            self.title("Sleep Detection Monitoring Software")
            
            self.geometry(f"{300}x{200}")

            self.resizable(False, False)

            self.protocol("WM_DELETE_WINDOW", exit)

            self.grid_rowconfigure(0, weight = 1)
            self.grid_rowconfigure(1, weight = 1)
            self.grid_rowconfigure(2, weight = 1)
            


            self.windowtitle = cust.CTkLabel(self, text = "Sleep Detection Monitoring Software", text_font = ("Times New Roman", 15), fg = "Black")
            self.windowtitle.grid(row = 0, column = 0, sticky = "nswe")

            self.masterframe = cust.CTkFrame(self, corner_radius = 0)

            self.masterframe.grid(row = 1, column = 0, sticky = "nswe")

            self.masterframe.grid_rowconfigure(0, minsize = 10, weight = 1)  

            self.masterframe.grid_columnconfigure(1, weight = 1)  
            self.masterframe.grid_columnconfigure(2, minsize = 10, weight = 1)


            self.clobbybutton = cust.CTkButton(self.masterframe, text = "Create Lobby", fg_color = "Black", text_color = "White", hover_color = "Silver", command = lambda: self.packcreateframe())
            self.clobbybutton.grid(row = 0, column = 0)

            self.jlobbybutton = cust.CTkButton(self.masterframe, text = "Join Lobby", fg_color = "Black", text_color = "White", hover_color = "Silver", command = lambda: self.packjoinframe())
            self.jlobbybutton.grid(row = 0, column = 2)



            self.masterframe2 = cust.CTkFrame(self, corner_radius = 0)

            self.masterframe2.grid(row = 2, column = 0, sticky = "nswe")

            self.back = cust.CTkButton(self.masterframe2, text = "Back", fg_color = "Red", text_color = "White", hover_color = "Maroon", state = "disabled", command = lambda: self.goback())
            self.back.pack(side = cust.BOTTOM, pady=5, padx=5)

            self.exit = cust.CTkButton(self.masterframe2, text = "Exit", fg_color = "Red", text_color = "White", hover_color = "Maroon", command = exit)
            self.exit.pack(side = cust.BOTTOM, pady = 5, padx = 5)

            

        def initserver(self):

            self.PORT = 5000
        
            #self.SERVER = "localhost" #exact server address if multiple computers; use "localhost" if server is within the same computer for testing purposes

            self.SERVER = "192.168.0.19"
            self.ADDRESS = (self.SERVER, self.PORT)
            self.FORMAT = "utf-8"

            self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                
                self.host.connect(self.ADDRESS)

            except:

                messagebox.showwarning("Server down!", "Server is currently down. Creating and/or joining lobbies might not work.")

                print (traceback.format_exc()) 


        def packcreateframe(self): 

            self.createframe = cust.CTkFrame(self, corner_radius = 0)

            self.createframe.grid_rowconfigure(0, minsize = 10, weight = 1)   
            self.createframe.grid_rowconfigure(1, minsize = 10, weight = 1)    
            self.createframe.grid_columnconfigure(0, weight = 1)  

            self.enterlname = cust.CTkEntry(self.createframe, placeholder_text = "Enter Lobby Name")
            self.enterlname.grid(row = 0, pady = 20, padx = 20, sticky = "news")

            self.mlobbybutton = cust.CTkButton(self.createframe, text = "Make Lobby", fg_color = "Black", text_color = "White", hover_color = "Silver", command = lambda: self.makelobby())
            self.mlobbybutton.grid(row = 1, sticky = "news")

            self.masterframe.grid_remove()
                    
            self.createframe.grid(row = 1, column = 0, sticky = "nswe")
            self.back.configure(state = cust.NORMAL)

            self.current_frame = self.createframe


        def packjoinframe(self):

            self.joinframe = cust.CTkFrame(self, corner_radius = 0)

            self.joinframe.grid_rowconfigure(0, weight = 1)   
            self.joinframe.grid_rowconfigure(1, weight = 1)    
            self.joinframe.grid_columnconfigure(0, weight = 1)  
            self.joinframe.grid_columnconfigure(1, weight = 1)
            

            self.entergname = cust.CTkEntry(self.joinframe, placeholder_text = "Enter your name")
            
            self.entergname.grid(row = 0, column = 0, pady = 1, padx = 1)

            self.enterlcode = cust.CTkEntry(self.joinframe, placeholder_text = "Enter the Lobby Code")
            
            self.enterlcode.grid(row = 0, column = 1, pady = 1, padx = 1)

            self.joinbutton = cust.CTkButton(self.joinframe, text = "Join", fg_color = "Black", text_color = "White", hover_color = "Silver", command = lambda: self.joinlobby())
            self.joinbutton.grid(row = 1, column = 1, pady = 1, padx = 1)


            self.masterframe.grid_remove()
                    
            self.joinframe.grid(row = 1, column = 0, sticky = "nswe")
            self.back.configure(state = cust.NORMAL)

            self.current_frame = self.joinframe


        def goback(self):

            self.current_frame.grid_remove()

            self.masterframe.grid(row = 1, column = 0, sticky = "nswe")
            self.back.configure(state = cust.DISABLED)


        def makelobby(self): #hides main menu window and initializes admin/host GUI

            #global lobbyname

            if len(self.enterlname.get()) == 0:

                messagebox.showwarning("Invalid input!", "Lobby should have a name!")

            else:

                self.initserver()

                self.host.send(("CL:" + self.enterlname.get()).encode(self.FORMAT))

                self.enterlname.delete(0, cust.END)
                self.enterlname.focus_set()

                self.withdraw()
                
                self.h = GUI2(self.PORT, self.SERVER, self.ADDRESS, self.FORMAT, self.host)
                

        def joinlobby(self): #hides main menu window and initializes client GUI


            if len(self.entergname.get()) == 0 or len (self.enterlcode.get()) == 0:

                messagebox.showwarning("Invalid input!", "Name and/or code should have input!")

            else:

                self.initserver()

                print ("I AM HERE")

                x = self.enterlcode.get()
                
                try: 

                    print ("BEFORE SENDING")

                    self.host.send(("RCODE:").encode(self.FORMAT))

                    self.lobbycode = self.host.recv(1024).decode(self.FORMAT)

                    print("AFTER RECEIVING")

                    print (self.lobbycode + "LMAO")

                    if x == "" or x.isspace(): #check if lobbycode is empty or whitespace only; either denotes lobby doesn't exist or was termintated

                        messagebox.showerror("Lobby offline!", "The lobby you're trying to connect to may be inactive.")

                    else:
                    
                        if x == self.lobbycode:

                            self.withdraw()
                            
                            self.j = GUI3()

                        else:

                            messagebox.showerror("Wrong Code!", "Lobby code provided doesn't match the host's.")

                except Exception:

                    messagebox.showerror("Error detected!", "The app is bugged!!!")

                    print (traceback.format_exc())

class GUI2(cust.CTk): #admin/host UI

    def __init__(self, a, b, c, d, e):

        #global lobbycode

        self.PORT = a
        self.SERVER = b
        self.ADDRESS = c
        self.FORMAT = d
        #self.FORMAT = "utf-8"
        self.host = e

        #self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.master2 = cust.CTkToplevel()


        self.master2.title("Admin/Host Lobby")
        self.master2.geometry(f"{906}x{400}")


        self.master2.protocol("WM_DELETE_WINDOW", self.leavewindow)


        self.master2.grid_rowconfigure(0, weight = 1)

        self.master2.grid_columnconfigure(0, weight = 1)
        self.master2.grid_columnconfigure(1, weight = 1)

        self.frame_left = cust.CTkFrame(self.master2, corner_radius = 0, bg_color = "White")
        self.frame_left.grid(row = 0, column = 0, sticky = "nswe", padx = 20, pady = 20)

        self.frame_right = cust.CTkFrame(self.master2, corner_radius = 0, width = 180)
        self.frame_right.grid(row = 0, column = 1, sticky= "nswe")

        # ============ frame_left ============


        self.frame_left.grid_rowconfigure(0, weight = 1)
        self.frame_left.grid_rowconfigure(1, weight = 1)
        self.frame_left.grid_rowconfigure(2, weight = 1)
        self.frame_left.grid_rowconfigure(3, weight = 1, minsize = 10)

        self.frame_left.grid_columnconfigure(0, weight = 1)
        self.frame_left.grid_columnconfigure(1, weight = 1)
        self.frame_left.grid_columnconfigure(2, weight = 1)
        

        self.leave = cust.CTkButton(self.frame_left, text = "Leave", fg_color = "Red", text_color = "White", hover_color = "Maroon", command = lambda: self.leavewindow())
        self.leave.grid(row = 0, column = 0, sticky = "n", padx = 1, pady = 1)


        self.ecdlabel = cust.CTkLabel(self.frame_left, text = "Eye Closure Detection", text_font = ("Arial Bold", 15), fg = "Black")
        self.ecdlabel.grid(row = 0, column = 2, sticky = "n")

        self.frame_code = cust.CTkFrame(self.frame_left, corner_radius = 0, border_color = "Blue")
        self.frame_code.grid(row = 1, column = 1, sticky= "nswe")

        self.lnumber = cust.CTkLabel(self.frame_code, text = "# ", text_font = ("Times New Roman", 15), fg = "Black", corner_radius = 0)
        self.lnumber.grid(row = 0, column = 0)

        self.ecdpower = cust.CTkButton(self.frame_left, text = "Off", fg_color = "Black", text_color = "White", hover_color = "Silver", command = lambda: Thread(target = self.startstream).start())
        self.ecdpower.grid(row = 1, column = 2)

        self.bigframe = cust.CTkFrame(self.frame_left, corner_radius = 0, border_color = "Black")
        self.bigframe.grid(row = 4, column = 0, sticky= "nswe", columnspan = 2, rowspan = 4, pady = 20, padx = 20)


        self.bigframe.grid_rowconfigure(0, weight = 1)
        self.bigframe.grid_rowconfigure(1, weight = 1)
        self.bigframe.grid_rowconfigure(2, weight = 1)

        self.bigframe.grid_columnconfigure(0, weight = 1)
        self.bigframe.grid_columnconfigure(1, weight = 1)
        self.bigframe.grid_columnconfigure(2, weight = 1)
        self.bigframe.grid_columnconfigure(3, weight = 1)
        self.bigframe.grid_columnconfigure(4, weight = 1)

        
        self.nameframe = cust.CTkFrame(self.bigframe, border_color = "Blue")
        self.nameframe.grid(row = 0, column = 0, sticky = "nsew")

        self.lname = cust.CTkLabel(self.nameframe, text = "Name", text_font = ("Times New Roman", 10), fg = "Blue")
        self.lname.grid(row = 0, column = 0, sticky = "nsew")


        self.statusframe = cust.CTkFrame(self.bigframe, border_color = "Blue")
        self.statusframe.grid(row = 0, column = 2, sticky = "nsew")

        self.lstatus = cust.CTkLabel(self.statusframe, text = "Status", text_font = ("Times New Roman", 10), fg = "Black")
        self.lstatus.grid(row = 0, column = 0, sticky = "nsew")


        self.idframe = cust.CTkFrame(self.bigframe, border_color = "Blue", corner_radius = 0)
        self.idframe.grid(row = 0, column = 4, sticky = "nsew")

        self.lid = cust.CTkLabel(self.idframe, text = "Active/Inactivity", text_font = ("Times New Roman", 10), fg = "Black")
        self.lid.grid(row = 0, column = 0, sticky = "nsew")


        self.clientframe = cust.CTkFrame(self.bigframe, corner_radius = 0, border_color = "Blue")
        self.clientframe.grid(row = 2, column = 0, sticky= "nswe", columnspan = 1, rowspan = 2, pady = 10, padx = 10)


        self.clientlist = tk.Listbox(self.clientframe)
        self.clientlist.grid(row = 0, column = 0, sticky= "nswe")

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(0, weight = 1)
        self.frame_right.grid_rowconfigure(1, weight = 1, minsize = 10)

        self.frame_right.grid_columnconfigure(0, weight = 1)

        self.notiframe = cust.CTkFrame(self.frame_right, border_color = "Blue")
        self.notiframe.grid(row = 0, column = 0, sticky = "nswe")


        self.lnotif = cust.CTkLabel(self.notiframe, text = "Sleeping Notification", text_font = ("Times New Roman", 10), fg = "Black")
        self.lnotif.grid(row = 0, column = 0, sticky = "nswe")


        self.notiflist = tk.Listbox(self.frame_right)
        self.notiflist.grid(row = 1, column = 0, sticky = "nswe", columnspan = 1, rowspan = 2, pady = 10, padx = 10)

        self.makelobbycode()

        #self.initserver()

        
        print("Before INITSERVER")

        print ("After INITSERVER")
       

        #self.master2.resizable(False, False)

        print ("After Thread INITIALIZATION")

        print ("After Thread start")


    def startstream(self):

        
        try:

                print (str(self.master2.winfo_width()) + " x " + str(self.master2.winfo_height()))

            #while True:

                if not self.clients:

                    messagebox.showerror("No Connections!", "No clients connected to host!")

                else:

                    for x in self.clients:

                        if self.ecdpower.text == "Off":

                            self.ecdpower.configure(text = "On", fg_color = "Green")

                            x.send(("On").encode(self.FORMAT))

                            print ("On sent")

                            

                            self.message = self.conn.recv(1024).decode(self.FORMAT)

                            self.notiflist.insert("end", self.message)

                        else:
                            
                            self.ecdpower.configure(text = "Off", fg_color = "Red")

                            x.send(("Off").encode(self.FORMAT))

                            print ("Off sent")

        except:

            print (traceback.format_exc())

    


    def leavewindow(self):

        self.host.send(("OFF").encode(self.FORMAT))
        
        #print("Thread closed")

        self.host.close()

        self.master2.destroy()
        
        g.deiconify()
        


    def makelobbycode(self):

        global lobbycode

        temp = random.choices(string.ascii_letters + string.digits, k = 5)

        temp = [str(x) for x in temp]

        lobbycode = ''.join(temp)

        messagebox.showinfo("New Lobby Code!", "Your lobby code is: " + lobbycode)

        self.lnumber.configure(text = "# " + lobbycode)

        #self.host.send(("CL:" + self.enterlname.get()).encode(self.FORMAT))

        self.host.send(("GCODE:" + lobbycode).encode(self.FORMAT)) 

        print (lobbycode)


class GUI3(cust.CTk): #initializes client GUI

    def __init__(self):

        super().__init__()

       
        self.master3 = cust.CTkToplevel()

        self.master3.title("Joined Lobby")
        self.master3.geometry(f"{906}x{400}")

        self.master3.protocol("WM_DELETE_WINDOW", self.leavewindow)

        self.master3.grid_rowconfigure(0, weight = 1)

        self.master3.grid_columnconfigure(0, weight = 1)
        self.master3.grid_columnconfigure(1, weight = 1)


        self.frame_left = cust.CTkFrame(self.master3, corner_radius = 0, bg_color = "White")
        self.frame_left.grid(row = 0, column = 0, sticky = "nswe", padx = 20, pady = 20)

        self.frame_right = cust.CTkFrame(self.master3, corner_radius = 0, width = 180)
        self.frame_right.grid(row = 0, column = 1, sticky= "nswe")

        # ============ frame_left ============


        self.frame_left.grid_rowconfigure(0, weight = 1)
        self.frame_left.grid_rowconfigure(1, weight = 1)
        self.frame_left.grid_rowconfigure(2, weight = 1)
        self.frame_left.grid_rowconfigure(3, weight = 1, minsize = 50)

        self.frame_left.grid_columnconfigure(0, weight = 1)
        self.frame_left.grid_columnconfigure(1, weight = 1)
        self.frame_left.grid_columnconfigure(2, weight = 1)



        self.leave = cust.CTkButton(self.frame_left, text = "Leave", fg_color = "Red", text_color = "White", hover_color = "Maroon", command = lambda: self.leavewindow())
        self.leave.grid(row = 0, column = 0, sticky = "n")

        self.ecdlabel = cust.CTkLabel(self.frame_left, text = "Sleeping Detection Status", text_font = ("Times New Roman", 15), fg = "Black")
        self.ecdlabel.grid(row = 0, column = 2, sticky = "nswe")


        self.lnameframe = cust.CTkFrame(self.frame_left, corner_radius = 0, border_color = "Black", bg_color = "White")
        self.lnameframe.grid(row = 1, column = 1, sticky = "nswe")

        self.lname = cust.CTkLabel(self.lnameframe, text = "+", text_font = ("Times New Roman", 15), fg = "Black")
        self.lname.grid(row = 0, column = 0, sticky = "nswe")


        


        self.bigframe = cust.CTkFrame(self.frame_left, border_color = "Black", corner_radius = 0)
        self.bigframe.grid(row = 3, column = 0, sticky = "nswe", padx = 50, pady = 50)

        self.lname = cust.CTkLabel(self.bigframe, text = "Watching you", text_font = ("Times New Roman", 15), fg = "Blue")
        self.lname.grid(row = 0, column = 0, sticky = "nswe")


        self.frame_right.grid_rowconfigure(0, weight = 1)
        self.frame_right.grid_rowconfigure(1, weight = 1, minsize = 10)

        self.frame_right.grid_columnconfigure(0, weight = 1)

        self.notiframe = cust.CTkFrame(self.frame_right, border_color = "Black")
        self.notiframe.grid(row = 0, column = 0, sticky = "nswe")

        self.lnotif = cust.CTkLabel(self.notiframe, text = "Sleeping Notification", text_font = ("Times New Roman", 15), fg = "Blue")
        self.lnotif.grid(row = 0, column = 0, sticky = "nswe")


        #self.notiframe2 = cust.CTkFrame(self.frame_right, border_color = "Blue")
        #self.notiframe2.grid(row = 1, column = 0, sticky = "nswe")


        self.notiflist = tk.Listbox(self.frame_right)
        self.notiflist.grid(row = 1, column = 0, sticky = "nswe")

        self.PORT = 5000
        
        self.SERVER = "192.168.0.19" #exact server address; may need to be changed depending on the computer
        self.ADDRESS = (self.SERVER, self.PORT)
        self.FORMAT = "utf-8"

        self.client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

        self.client.connect(self.ADDRESS)

        self.name = g.entergname.get()

        self.client.send(self.name.encode(self.FORMAT)) #sends client's name to server

        self.vs = VideoStream(src = 0).start()

        self.rev = Thread(target = self.startstream2)

        self.rev.start()

        #self.rev.join()

        #self.i = INITCLIENT()

    

    def leavewindow(self):

        self.client.close()

        self.master3.destroy()

        g.deiconify()

    def eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        a = dist.euclidean(eye[1], eye[5])
        b = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizonta
        # eye landmark (x, y)-coordinates
        c = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (a + b) / (2.0 * c)

        # return the eye aspect ratio
        return ear

    def startstream2(self):

        global message

        #self.vs.start()

        try:

            #while True:

                print("inside while")

                message = self.client.recv(1024).decode(self.FORMAT)

                if message == "On":

                    time.sleep(3)

                    self.vs.start()

                    print ("INSIDE FOR LOOP THE: " + self.SERVER)

                    EYE_AR_THRESH = 0.35
                    EYE_AR_CONSEC_FRAMES = 3

                    # initialize the frame counters and the total number of blinks
                    COUNTER = 0
                    TOTAL = 0

                    # initialize dlib's face detector (HOG-based) and then create
                    # the facial landmark predictor
                    print("[INFO] loading facial landmark predictor...")
                    detector = dlib.get_frontal_face_detector()
                    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

                    # grab the indexes of the facial landmarks for the left and
                    # right eye, respectively
                    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
                    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

                    #vs = VideoStream(src=0).start()

                    

                    # vs = VideoStream(usePiCamera=True).start()
                    #time.sleep(0)

                    # loop over frames from the video stream
                    #while True:

                    print (message)
                    # if this is a file video stream, then we need to check if
                    # there any more frames left in the buffer to process

                    # grab the frame from the threaded video file stream, resize
                    # it, and convert it to grayscale
                    # channels)
                    frame = self.vs.read()
                    frame = imutils.resize(frame, width=1080 )
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # detect faces in the grayscale frame
                    rects = detector(gray, 0)

                    # loop over the face detections
                    for rect in rects:
                        # determine the facial landmarks for the face region, then
                        # convert the facial landmark (x, y)-coordinates to a NumPy
                        # array
                        shape = predictor(gray, rect)
                        shape = face_utils.shape_to_np(shape)

                        # extract the left and right eye coordinates, then use the
                        # coordinates to compute the eye aspect ratio for both eyes
                        leftEye = shape[lStart:lEnd]
                        rightEye = shape[rStart:rEnd]

                        leftEAR = self.eye_aspect_ratio(leftEye)
                        rightEAR = self.eye_aspect_ratio(rightEye)

                        # average the eye aspect ratio together for both eyes
                        ear = (leftEAR + rightEAR)

                        # compute the convex hull for the left and right eye, then
                        # visualize each of the eyes
                        leftEyeHull = cv2.convexHull(leftEye)
                        rightEyeHull = cv2.convexHull(rightEye)
                        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)


                        # check to see if the eye aspect ratio is below the blink
                        # threshold, and if so, increment the blink frame counter
                        if ear < EYE_AR_THRESH:
                            cv2.putText(frame, "Eye: {}".format("close"), (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                            print ("Eyes closed")

                            self.notiflist.insert("end", "Host is watching you!")

                            self.client.send((self.name + " is sleeping!!").encode(self.FORMAT))

                            self.vs.stop()

                            self.master3.after(1000, self.startstream2)


                            # otherwise, the eye aspect ratio is not below the blink
                            # threshold
                        else:
                            cv2.putText(frame, "Eye: {}".format("Open"), (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                            print ("Eyes open")

                            self.notiflist.insert("end", "Thank you for keeping attention")

                            self.client.send((self.name + " is awake!!").encode(self.FORMAT))

                            #self.notiflist.delete(0, tk.END)

                            self.vs.stop()

                            self.master3.after(1000, self.startstream2)

                        # draw the total number of blinks on the frame along with
                        # the computed eye aspect ratio for the frame

                        # show the frame
                        #cv2.imshow("Eye Close Detection Using EAR", frame)
                        #key = cv2.waitKey(1) & 0xFF

                        # if the `q` key was pressed, break from the loop
                        #if key == ord("q"):
                            #break

                    # do a bit of cleanup
                    #cv2.destroyAllWindows()
                    #vs.stop()
                else:

                    print ("Inside destroy")

                    self.vs.stop()
                    #cv2.destroyAllWindows()

                    self.master3.after(1000, self.startstream2)

                    #return

        except Exception as e:

            if e == ConnectionResetError:

                messagebox.showerror("Lobby Closed!", "The host has closed this lobby.")

            else:

                print (traceback.format_exc())

if __name__ == "__main__":


    g = GUI()

    g.mainloop()