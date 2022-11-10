import tkinter as tk


import random
import string
import socket

from tkinter import messagebox

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

class INITSERVER():

    def __init__(self):

        self.PORT = 5000
        
        self.SERVER = socket.gethostbyname(socket.gethostname())
        
        self.ADDRESS = (self.SERVER, self.PORT)
       
        self.FORMAT = "utf-8"
        
        self.clients, self.names = [], []
       
        self.server = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)
       
        self.server.bind(self.ADDRESS)

    def revlobbyname(a):

        global lobbyname

        lobbyname = a

    def givlobbyname(self):

        global lobbyname

        return lobbyname

    def makelobbycode(self):

        global lobbycode

        temp = random.choices(string.ascii_letters + string.digits, k = 5)

        temp = [str(x) for x in lobbycode]

        lobbycode = ''.join(temp)


    def givlobbycode():

        global lobbycode

        return lobbycode


i = INITSERVER()
        