from tkinter import *
from tkinter.filedialog import *
import os

#root = Tk()

fType = [("*.jpg", "*.png")]
iDir = os.path.abspath(os.path.dirname(__file__ + "./SS"))
filename = askopenfile(filetypes=fType, initialdir=iDir)
print(filename)
