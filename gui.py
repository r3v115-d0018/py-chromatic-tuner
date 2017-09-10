from Tkinter import *
from colour import Color
import tuner
import math

class App:
    __tuner = None
    __master = None
    __accuracy = None

    __text_info = None
    __info_content = None

    __canvas = None

    __needle = None
    __colors = []

    __height = None
    __width = None

    def __init__(self, width, height, A4 = 440, tolerance = 0.1, accuracy = 5):
        self.__tuner = tuner.Tuner(A4, tolerance, accuracy)
        self.__master = Tk()

        screen_w = self.__master.winfo_screenwidth()
        screen_h = self.__master.winfo_screenheight()

        self.__width  = width
        self.__height = height

        pos = "+{}+{}".format(screen_w/2-self.__width/2,
                              screen_h/2-self.__height/2)

        self.__master.geometry(pos)
        self.__accuracy = accuracy

        self.__info_content = StringVar()
        self.__text_info = Label(self.__master, textvariable=self.__info_content)

        self.__canvas = Canvas(self.__master, width=self.__width, height=self.__height)

        self.__canvas.grid(row=0,column=0)
        self.__text_info.grid(row=1,column=0)
        self.drawBar()
        self.drawNeedle()

        self.initColors()

    def update(self):
        errorper, error, pitch, note, octave = self.__tuner.getData() 

        if pitch != 0:
            self.updateInfo(pitch, note, octave)
            self.updateNeedle(errorper, error)

        self.__master.after(10, self.update)
    
    def updateInfo(self, pitch, note, octave):
        self.__info_content.set("Pitch: {:.2f} Hz Note: {}{}".format(pitch, note, octave))

    def updateNeedle(self, errorper, error):
        colorIndex = int(10*errorper)
        if error > 0:
            newX = self.__width/2 + (3.0*self.__width/8)*errorper
            newY = self.__height/2
            self.__canvas.coords(self.__needle, newX, newY,
                                                newX, newY - 15)
            self.__canvas.itemconfig(self.__needle, fill=self.__colors[colorIndex])
        else:
            newX = self.__width/2 - (3.0*self.__width/8)*errorper
            newY = self.__height/2
            self.__canvas.coords(self.__needle, newX, newY,
                                                newX, newY - 15)
            self.__canvas.itemconfig(self.__needle, fill=self.__colors[colorIndex])

    def initColors(self):
        green = Color("green")
        self.__colors = list(green.range_to(Color("red"), 10)) 

    def drawBar(self):
        self.__canvas.create_line(1.0/8 * self.__width, self.__height/2,
                                  7.0/8 * self.__width, self.__height/2,
                                  width = 2.0)
        self.__canvas.create_line(self.__width/2, self.__height/2,
                                                  self.__width/2, self.__height/2 - 20,
                                                  fill="black",
                                                  width=2.0)

    def drawNeedle(self):
        self.__needle = self.__canvas.create_line(self.__width/2, self.__height/2,
                                                  self.__width/2, self.__height/2 - 15,
                                                  fill="green",
                                                  width=2.0)


    def run(self):
        self.__master.after(10, self.update)
        self.__master.mainloop()

app = App(width=400, height=281)
app.run()
