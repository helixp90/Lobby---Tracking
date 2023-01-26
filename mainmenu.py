import tkinter as tk
from tkinter import ttk as tick
from tkinter import PhotoImage
import os
import random
import string
import socket
from PIL import ImageTk as itk
import PIL.Image
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

        def turnoff(self):

            self.host.close()
            self.destroy()

            

        def initserver(self):

            self.PORT = 5000
        
            #self.SERVER = "localhost" #exact server address if multiple computers; use "localhost" if server is within the same computer for testing purposes

            self.SERVER = "192.168.0.19" #server address
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
                y = self.entergname.get()
                
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

                            self.host.send(("CLIENT:").encode(self.FORMAT))

                            self.withdraw()
                            
                            self.j = GUI3(self.PORT, self.SERVER, self.ADDRESS, self.FORMAT, self.host, y)

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
        #self.master2.grid_columnconfigure(1, weight = 1)

        self.frame_left = cust.CTkFrame(self.master2, corner_radius = 0, bg_color = "White")
        self.frame_left.grid(row = 0, column = 0, sticky = "nswe", padx = 20, pady = 20)

        #self.frame_right = cust.CTkFrame(self.master2, corner_radius = 0, width = 180)
        #self.frame_right.grid(row = 0, column = 1, sticky= "nswe")

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
        self.bigframe.grid(row = 4, column = 0, sticky = "nswe", columnspan = 2, rowspan = 4, pady = 20, padx = 20)


        self.bigframe.grid_rowconfigure(0, weight = 1)
        self.bigframe.grid_rowconfigure(1, weight = 1)
        #self.bigframe.grid_rowconfigure(2, weight = 1)

        self.bigframe.grid_columnconfigure(0, weight = 1)
        #self.bigframe.grid_columnconfigure(1, weight = 1)
        #self.bigframe.grid_columnconfigure(2, weight = 1)
        #self.bigframe.grid_columnconfigure(3, weight = 1)
        #self.bigframe.grid_columnconfigure(4, weight = 1)

        
        self.nameframe = cust.CTkFrame(self.bigframe, border_color = "Blue")
        self.nameframe.grid(row = 0, column = 0, sticky = "nsew")

        self.nameframe.grid_rowconfigure(0, weight = 1)

        self.nameframe.grid_columnconfigure(0, weight = 1)
        self.nameframe.grid_columnconfigure(1, weight = 1)
        self.nameframe.grid_columnconfigure(2, weight = 1)

        self.lname = cust.CTkLabel(self.nameframe, text = "Name", text_font = ("Times New Roman", 10), fg = "Blue")
        self.lname.grid(row = 0, column = 0, sticky = "nsew")


        #self.statusframe = cust.CTkFrame(self.bigframe, border_color = "Blue")
        #self.statusframe.grid(row = 0, column = 2, sticky = "nsew")

        self.lstatus = cust.CTkLabel(self.nameframe, text = "Status", text_font = ("Times New Roman", 10), fg = "Black")
        self.lstatus.grid(row = 0, column = 1, sticky = "nsew")


        #self.idframe = cust.CTkFrame(self.bigframe, border_color = "Blue", corner_radius = 0)
        #self.idframe.grid(row = 0, column = 4, sticky = "nsew")

        self.lid = cust.CTkLabel(self.nameframe, text = "Active/Inactivity", text_font = ("Times New Roman", 10), fg = "Black")
        self.lid.grid(row = 0, column = 2, sticky = "nsew")


        self.clientframe = cust.CTkFrame(self.bigframe, corner_radius = 0, border_color = "Blue")
        self.clientframe.grid(row = 1, column = 0, sticky = "nswe")

        #self.clientframe.pack_propagate(True)


        self.columns = ("name", "status", "activity")

        self.clientlist = tick.Treeview(self.clientframe, columns = self.columns, show = "tree")
        self.clientlist.grid(row = 0, column = 0, sticky = "nswe")

        self.clientlist.column("#0", minwidth = 0, width = 10, stretch = False)

        self.clientlist.column("name", minwidth = 0, width = 200, stretch = True)
        self.clientlist.column("status", minwidth = 0, width = 200, stretch = True)
        self.clientlist.column("activity", minwidth = 0, width = 200, stretch = True)

        self.cwd = os.getcwd()

        print (self.cwd)

        #self.temp = PIL.Image.open("redlight.png")
        #self.red = itk.PhotoImage(self.temp)

        #self.temp2 = PIL.Image.open("greenlight.png")
        #self.green = itk.PhotoImage(self.temp2)

        #self.temp3 = PIL.Image.open("blacklight.png")
        #self.black = itk.PhotoImage(self.temp3)

        self.red = PhotoImage(file = "redlight.png")
        self.green = PhotoImage(file = "greenlight.png")
        self.black = PhotoImage(file = "blacklight.png")

        #self.clientlist = tk.Listbox(self.clientframe)
        #self.clientlist.grid(row = 0, column = 0, sticky= "nswe")

        # ============ frame_right ============

        #self.frame_right.grid_rowconfigure(0, weight = 1)
        #self.frame_right.grid_rowconfigure(1, weight = 1, minsize = 10)

        #self.frame_right.grid_columnconfigure(0, weight = 1)

        #self.notiframe = cust.CTkFrame(self.frame_right, border_color = "Blue")
        #self.notiframe.grid(row = 0, column = 0, sticky = "nswe")


        #self.lnotif = cust.CTkLabel(self.notiframe, text = "Sleeping Notification", text_font = ("Times New Roman", 10), fg = "Black")
        #self.lnotif.grid(row = 0, column = 0, sticky = "nswe")


        #self.notiflist = tk.Listbox(self.frame_right)
        #self.notiflist.grid(row = 1, column = 0, sticky = "nswe", columnspan = 1, rowspan = 2, pady = 10, padx = 10)

        self.makelobbycode()

        #self.initserver()

        
        print("Before INITSERVER")

        print ("After INITSERVER")
       
        self.thread = Thread(target = self.initreceiver)
        self.thread.start()

        #self.master2.resizable(False, False)

        print ("After Thread INITIALIZATION")

        print ("After Thread start")

    def initreceiver(self):

        try:

            while True:
                
                #self.host.settimeout(0.005)

                self.message = self.host.recv(1024).decode(self.FORMAT)

                print (self.message)

                if "NAME:" in self.message:

                    x = self.message.replace("NAME:", "")

                    self.clientlist.insert("", cust.END, iid = x, values = x)

                    print (x)

                elif "CLEND:" in self.message:

                    x = self.message.replace("CLEND:", "")

                    messagebox.showinfo("Client Disconnected!", x + " has left the server.")

                    self.clientlist.delete(x)

                elif "NO CLIENTS:" in self.message:

                    messagebox.showerror("No Connections!", "No clients connected to host!")

                    self.ecdpower.configure(text = "Off", fg_color = "Red")

                elif "CLOSED:" in self.message:

                    x = self.message.replace("CLOSED:", "")

                    self.clientlist.set(x, "status", "Eyes are closed")
                    self.clientlist.set(x, "activity", "INACTIVE")

                    #self.clientlist.item(x, image = self.red)

                elif "SLEEPING:" in self.message:

                    x = self.message.replace("SLEEPING:", "")

                    self.clientlist.set(x, "status", "Client is sleeping!!")
                    self.clientlist.set(x, "activity", "SLEEPING")


                elif "AWAKE:" in self.message:

                    x = self.message.replace("AWAKE:", "")

                    self.clientlist.set(x, "status", "Eyes are open")
                    self.clientlist.set(x, "activity", "ACTIVE")

                    #self.clientlist.item(x, image = self.green)

                elif "NFD:" in self.message:

                    x = self.message.replace("NFD:", "")

                    self.clientlist.set(x, "status", "No Face Detected")
                    self.clientlist.set(x, "activity", "UNKNOWN")

                

        except Exception:

            print (traceback.format_exc())
            


    def startstream(self):

        try:

            if self.ecdpower.text == "Off":

                self.ecdpower.configure(text = "On", fg_color = "Green")

                self.host.send(("ON:").encode(self.FORMAT))

                print ("On sent")

            else:
                
                self.ecdpower.configure(text = "Off", fg_color = "Red")

                self.host.send(("OFF:").encode(self.FORMAT))

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

    def __init__(self, a, b, c, d, e, f):

        self.PORT = a
        self.SERVER = b
        self.ADDRESS = c
        self.FORMAT = d
        
        self.client = e

        self.clientname = f

        self.flag = Event()

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
        #self.frame_left.grid_rowconfigure(2, weight = 1)
        #self.frame_left.grid_rowconfigure(3, weight = 1, minsize = 50)

        self.frame_left.grid_columnconfigure(0, weight = 1)
        #self.frame_left.grid_columnconfigure(1, weight = 1)
        #self.frame_left.grid_columnconfigure(2, weight = 1)

        self.frame_up = cust.CTkFrame(self.frame_left, corner_radius = 0)
        self.frame_up.grid(row = 0, column = 0, sticky = "nswe")

        self.frame_down = cust.CTkFrame(self.frame_left, corner_radius = 0)
        self.frame_down.grid(row = 1, column = 0, sticky = "nswe")


         # ============ frame_up ============


        self.frame_up.grid_rowconfigure(0, weight = 1)
        self.frame_up.grid_rowconfigure(1, weight = 1)
        
        self.frame_up.grid_columnconfigure(0, weight = 1)
        self.frame_up.grid_columnconfigure(1, weight = 1)
        self.frame_up.grid_columnconfigure(2, weight = 1)



        self.leave = cust.CTkButton(self.frame_up, text = "Leave", fg_color = "Red", text_color = "White", hover_color = "Maroon", command = lambda: self.leavewindow())
        self.leave.grid(row = 0, column = 0, sticky = "n")

        self.ecdlabel = cust.CTkLabel(self.frame_up, text = "Sleeping Detection Status", text_font = ("Times New Roman", 15), fg = "Black")
        self.ecdlabel.grid(row = 0, column = 2, sticky = "nswe")


        self.lnameframe = cust.CTkFrame(self.frame_up, corner_radius = 0, border_color = "Black", highlightcolor = "White", highlightthickness = 2)
        self.lnameframe.grid(row = 1, column = 1, sticky = "nswe")

        self.lname = cust.CTkLabel(self.lnameframe, text = "Lobby Name", text_font = ("Times New Roman", 15), fg = "Black")
        self.lname.grid(row = 0, column = 0, sticky = "nswe")

        # ============ frame_down ============

        self.frame_down.grid_rowconfigure(0, weight = 1)
        
        self.frame_down.grid_columnconfigure(0, weight = 1)


        self.bigframe = cust.CTkFrame(self.frame_down, highlightbackground = "Black", highlightthickness = 2, corner_radius = 0)
        self.bigframe.grid(row = 0, column = 0, sticky = "nswe", padx = 50, pady = 50)

        self.lname2 = cust.CTkLabel(self.bigframe, text_font = ("Times New Roman", 15), fg = "Blue")
        self.lname2.grid(row = 0, column = 0, sticky = "nswe")


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


        self.client.send(("NAME:" + self.clientname).encode(self.FORMAT))

        
        #self.vs = VideoStream(src = 0)

        #self.i = INITCLIENT()

        self.thread = Thread(target = self.initreceiver)
        self.thread.start()


    def initreceiver(self):

        try:

            while True:
                
                #self.host.settimeout(0.005)

                self.message = self.client.recv(1024).decode(self.FORMAT)

                print (self.message)

                if "CLIENT:" in self.message:

                    self.lname.configure(text = self.message.replace("CLIENT:", "") + "'s Lobby")

                    self.lname2.configure(text = "Welcome to " + self.message.replace("CLIENT:", "") + "'s Lobby!")

                elif self.message == "ON:":
                    
                    #self.flag.clear()

                    self.rev = Thread(target = self.startstream2)
                    self.rev.start()

                elif self.message == "OFF:":

                    self.flag.set()

                    self.rev.join()

                    self.flag.clear()

                elif self.message == "CLEND:":

                    #self.flag.set()
                    #self.rev.join()
                    #self.flag.clear()

                    print ("WATASHI GA KITA")

                    return



        except Exception:

            print (traceback.format_exc())

    def leavewindow(self):

        self.client.send(("CLEND:" + self.clientname).encode(self.FORMAT))

        #self.thread.join()

        self.master3.destroy()

        g.deiconify()

        self.client.close()

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

        try:

            self.vs = VideoStream(src = 0)

            self.temp = ""
            self.result = ""

            counter = 0

            nfdcounter = 0

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

            while not self.flag.is_set():

                frame = self.vs.read()

                if frame is None or frame.size == 0:

                    self.client.send(("NFD:" + self.clientname).encode(self.FORMAT))

                    print ("No Face Detected")

                    return

                else:

                    frame = imutils.resize(frame, width = 1080 )
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # detect faces in the grayscale frame
                    rects = detector(gray, 0)

                    if rects is None or not rects: #if camera doesn't detect client's face

                        if nfdcounter != 5:

                            time.sleep(1)

                            nfdcounter += 1

                            print ("NFD Counter added " + str(nfdcounter))

                        else:

                            if self.result == "" or self.result.isspace(): #checks if there were previous frames

                                print (self.result + "s")

                                self.result = "NFD:"

                                print ("NO FACE DETECTED")

                                self.notiflist.insert("end", "NO FACE DETECTED")

                                self.client.send((self.result + self.clientname).encode(self.FORMAT))

                            else:

                                self.temp = "NFD:"

                                if self.result != self.temp:

                                    self.notiflist.delete(0, cust.END)

                                    self.notiflist.insert("end", "NO FACE DETECTED")

                                    print ("Client has disappeared!")

                                    self.client.send((self.temp + self.clientname).encode(self.FORMAT))

                                #elif self.temp == self.result and self.temp == "NFD:": 

                                    #time.sleep(1)

                                    #counter += 1

                                    #print ("SELF.RESULT BEFORE: " + self.result)

                                    #self.result = self.temp #value of current frame becomes value of previous frame

                                    #print ("SELF.RESULT AFTER: " + self.result)

                                    #self.temp = ""

                                    #print ("Counter added " + str(counter))

                                        
                                self.result = self.temp #value of current frame becomes value of previous frame
                                self.temp = ""

                                #nfdcounter = 0

                    else:

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

                            if self.result == "" or self.result.isspace(): #check if self.result value is null

                                # check to see if the eye aspect ratio is below the blink
                                # threshold, and if so, increment the blink frame counter
                                if ear <= EYE_AR_THRESH:
                                    cv2.putText(frame, "Eye: {}".format("close"), (10, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                                    cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                                    self.result = "CLOSED:"

                                    print ("First frame, eyes are closed or Previous frame has no face")

                                    #self.notiflist.delete(0, cust.END)

                                    self.notiflist.insert("end", "Host is watching you!")

                                    self.client.send((self.result + self.clientname).encode(self.FORMAT))

                                    # otherwise, the eye aspect ratio is not below the blink
                                    # threshold
                                elif ear > EYE_AR_THRESH:
                                    cv2.putText(frame, "Eye: {}".format("Open"), (10, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                                    cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                                    print ("First frame, Eyes open")

                                    self.result = "AWAKE:"

                                    #self.notiflist.delete(0, cust.END)

                                    self.notiflist.insert("end", "Thank you for keeping attention")

                                    self.client.send((self.result + self.clientname).encode(self.FORMAT))

                                else:

                                    continue

                            else:

                                if ear <= EYE_AR_THRESH:

                                    self.temp = "CLOSED:"

                                elif ear > EYE_AR_THRESH:

                                    self.temp = "AWAKE:"

                                #else: 

                                    #continue

                                #print ("TEMP VALUE IS: " + self.temp) #for checking
                                #print ("RESULT VALUE IS: " + self.result) #for checking

                                if self.result == "NFD:":

                                    #self.client.send((self.temp + self.clientname).encode(self.FORMAT))

                                    print ("Client has appeared again!")

                                    #self.result = self.temp #value of current frame becomes value of previous frame

                                    #print ("SELF.RESULT AFTER: " + self.result)

                                    #self.temp = ""

                                    print ("Client has been gone for " + str(nfdcounter) + " seconds!")

                                    nfdcounter = 0

                                    self.notiflist.delete(0, cust.END)

                                    self.notiflist.insert("end", "Thank you for coming back!!!")

                                #else:

                                if self.temp != self.result and self.temp == "AWAKE:": #if current frame and previous frame are not the same, and current frame == "AWAKE:", this means the previous frame was closed and that client has just opened their eyes

                                    self.client.send((self.temp + self.clientname).encode(self.FORMAT))

                                    #print ("SELF.RESULT BEFORE: " + self.result)

                                    self.result = self.temp #value of current frame becomes value of previous frame

                                    #print ("SELF.RESULT AFTER: " + self.result)

                                    self.temp = ""

                                    counter = 0

                                    print ("Eyes are open again")

                                    self.notiflist.insert("end", "Thank you for keeping attention.")

                                elif self.temp == self.result and self.temp == "CLOSED:": #if current frame has the same value as the previous frame, and current frame == CLOSED:, that means the client has been closing their eyes consecutively

                                    if counter != 3:

                                        time.sleep(1)

                                        counter += 1

                                        #print ("SELF.RESULT BEFORE: " + self.result)

                                        self.result = self.temp #value of current frame becomes value of previous frame

                                        #print ("SELF.RESULT AFTER: " + self.result)

                                        self.temp = ""

                                        print ("Closed eyes counter added " + str(counter))

                                    else:

                                        self.client.send(("SLEEPING:" + self.clientname).encode(self.FORMAT))

                                        counter = 0

                                        print ("COUNTER = 0")

                                        self.notiflist.delete(0, cust.END)

                                        self.notiflist.insert("end", "Host is watching you 2!")

                                        #print ("SELF.RESULT BEFORE: " + self.result)

                                        self.result = self.temp #value of current frame becomes value of previous frame

                                        #print ("SELF.RESULT AFTER: " + self.result)

                                        self.temp = ""

                                else: #value of current frame becomes value of previous frame

                                    self.result = self.temp
                                    self.temp = ""
   
            else:

                print ("Inside destroy")

                self.vs.stop()

                self.result = ""

                self.temp = ""

                #counter = 0

                return

        except Exception as e:

            self.client.send(("NFD:" + self.clientname).encode(self.FORMAT))

            print ("No Face Detected")

            print (traceback.format_exc())


if __name__ == "__main__":


    g = GUI()

    g.mainloop()