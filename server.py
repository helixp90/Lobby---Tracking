
import random
import string
import socket

from tkinter import messagebox

import threading

from threading import Thread

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
hostlcode = ""

flag = False

PORT = 5000
        
SERVER = socket.gethostbyname(socket.gethostname())

ADDRESS = (SERVER, PORT)

FORMAT = "utf-8"

clients, names = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)


def revlobbyname(a):

    global lobbyname

    lobbyname = a

def givlobbyname():

    #global lobbyname

    return lobbyname


def revhostcode(a):

    global hostlcode

    hostlcode = a

def givhostcode():

    return hostlcode

def setFlag(a):

    global flag

    if a == 0:

        flag = False

    else:

        flag = True


def startChat():

    print("server is working on " + SERVER)

    # listening for connections
    server.listen(30)

    try:

        while True:

            global flag

            if flag:

                break

            else:

                # accept connections and returns
                # a new connection to the client
                #  and  the address bound to it
                conn, addr = server.accept()
                #self.conn.send("NAME".encode(FORMAT))

                # 1024 represents the max amount
                # of data that can be received (bytes)
                name = conn.recv(1024).decode(FORMAT)

                # append the name and client
                # to the respective list

                #self.names.append(self.name)
                clients.append(conn)

                #if "sleep" in self.name or "awake" in self.name:

                    #self.notiflist.insert("end", self.name)

                #else:

                #self.clientlist.insert("end", self.name) #append client names to listbox

                #print(f"Name is {self.name}")

                #print (f"Address is {self.addr}")

                for y in clients:

                    print (f"Address is {y}")

                #print (f"Address is {self.addr[0]}")

                # broadcast message
                #broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))

                #self.conn.send('Connection successful!'.encode(self.FORMAT))

                # Start the handling thread
                #self.thread = threading.Thread(target = self.handle, args = (self.conn, self.addr))
                #self.thread.start()

                # no. of clients connected
                # to the server
                #print(f"active connections {threading.activeCount()-1}")

            #else:

                #return  

    except:

        print (traceback.format_exc())
