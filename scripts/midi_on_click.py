#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: aditya
"""

import pygame
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2 as cv
import Simulate
import os
import sys
pygame.init()

pygame.mixer.init()

if __name__ == "__main__":
    root = Tk()
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)
    
    #adding the image
    File = askopenfilename(parent=root, initialdir=os.getcwd()+"/images",title='Choose an image.')
    imgCV = cv.imread(File)
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    
    def call_simulate(event):
        #print root.winfo_pointerxy()
        # print (event.x, event.y)
        print("GBR color")
        print (imgCV[event.y, event.x])
        filename = Simulate.simulate(imgCV[event.y, event.x])
        pygame.mixer.music.load(filename)
        # pygame.mixer.music.play(0)

    #mouseclick event
    canvas.bind("<Button 1>",call_simulate)

    
    def play():
        pygame.mixer.music.play(0)
    
    def stop():
        pygame.mixer.music.stop()

        
    play_button = Button(root, text = 'Create audio', command = play)
    play_button.pack()
    
    stop_button = Button(root, text = 'Stop Audio', command = stop)
    stop_button.pack()
    
    Button(root, text="Quit", command=root.destroy).pack()

    root.mainloop()