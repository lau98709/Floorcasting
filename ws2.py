from PIL import Image as PILImage
from PIL import ImageTk
from PIL import ImageDraw, ImageFont
from tkinter import *
# from tkinter import filedialog
# from tkinter.filedialog import asksaveasfilename

import time
import math
# import os
# import pathlib

class WindowSystem:
    #  Classe fenêtre tkinter qui comporte un canvas (zone de dessin)

    def __init__(self, width=0, height=0, title=""):
        self.running = True
        self.focus = False
        self.lastmouse = (0,0)
        self.count = 0

        self.window = Tk()
        self.window.title(title);
        self.build(width=width, height=height);

        self.initBuffer()
        # self.putBuffer()

        self.window.bind("<KeyPress>", self.keyProc)
        self.window.bind("<Configure>", self.onResize)

        self.canvas.bind("<Motion>", self.mouseMove)
        self.canvas.bind("<Button>", self.mouseBtn)
        self.canvas.bind("<ButtonRelease>", self.mouseBtn)
        self.canvas.bind("<Enter>", self.onEnter)
        self.canvas.bind("<Leave>", self.onLeave)
        self.canvas.bind("<MouseWheel>", self.mouseWheel)

    def build(self, width=0, height=0):
        self.canvas = Canvas(self.window)
        if width != 0 and height != 0:
            self.canvas.config(width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.window.update()

    def mouseBtn(self, event):
        if str(event.type)=='ButtonPress':
            self.dragstart = (event.x, event.y)
        elif str(event.type)=='ButtonRelease':
            self.putBuffer()

    def mouseMove(self, event):
        self.lastmouse = (event.x, event.y)

    def mouseWheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.count -= 1
        if event.num == 4 or event.delta == 120:
            self.count += 1

    def onEnter(self, event):
        self.focus = True

    def onLeave(self, event):
        self.focus = False

    def keyProc(self, event):
        if event.keysym == "Escape":
            self.running = False

    def onResize(self, event):
        self.initBuffer()
        self.putBuffer()

    def canvasSize(self):
        return self.canvas.winfo_width(), self.canvas.winfo_height()

    def initBuffer(self):
        w, h = self.canvasSize()
        self.buffer = PILImage.new('RGB', (w,h), color='black')
        self.imgtk = ImageTk.PhotoImage(self.buffer)

    def putBuffer(self):
        w, h = self.canvasSize()
        imagedraw = ImageDraw.Draw(self.buffer)
        self.draw(imagedraw, w, h)

        self.imgtk = ImageTk.PhotoImage(self.buffer)
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=NW, image=self.imgtk)

        self.window.update()

    def update(self, draw=True):
        try:
            if self.running:
                if draw:
                    self.putBuffer()
                self.window.update()
        except Exception as e:
            print(e.args)
            self.running = False

    def loop(self):
        while self.running:
            self.update()
        exit()

    def draw(self, imagedraw, w, h):
        pass
