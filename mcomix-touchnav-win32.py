#! /usr/bin/python2.7
from time import sleep
import win32gui
import thread
import win32com
import win32com.client


def winget():
    root.after(3000,getwindow)
    
def getwindow():    
    global inputWindow
    inputWindow=win32gui.GetForegroundWindow()
    print inputWindow

def left():
    global shell
    shell = win32com.client.Dispatch('WScript.Shell')
    win32gui.SetForegroundWindow(inputWindow)
    win32gui.SetActiveWindow(inputWindow)
    typeleft()
    #root.after(3000,typeleft)
    #shell.SendKeys("Hello World",0)
def right():
    global shell
    shell = win32com.client.Dispatch('WScript.Shell')
    win32gui.SetForegroundWindow(inputWindow)
    win32gui.SetActiveWindow(inputWindow)
    #root.after(3000,typeright)
    typeright()
    #shell.SendKeys("Hello World",0)

def fullscreen():
    global shell
    shell = win32com.client.Dispatch('WScript.Shell')
    win32gui.SetForegroundWindow(inputWindow)
    win32gui.SetActiveWindow(inputWindow)
    typef()

def typeleft():
    shell.SendKeys("{PGUP}",0)

def typeright():
    shell.SendKeys("{PGDN}",0)

def typef():
    shell.SendKeys("f",0)



from Tkinter import *
root=Tk()  #It is just a holder
root.wm_attributes("-topmost", 1)
root.resizable(width=FALSE, height=FALSE)
root.resizable(0,0)
root.attributes("-toolwindow", 1)
buttonframe=Frame(root)
buttonframe1=Frame(buttonframe)
buttonframe2=Frame(buttonframe)
#buttonframe3=Frame(buttonframe)
buttonframe.grid(row=0,column=1)
buttonframe1.grid(row=0,column=0,rowspan=2)
buttonframe2.grid(row=0,column=1)
#buttonframe3.grid(row=2,column=0,columnspan=2)

Button(buttonframe2,text="Select",height=1,width=10,justify=LEFT,command=winget).grid(row=0,column=0)
Button(buttonframe2,text="Fullscreen",height=1,width=10,justify=LEFT,command=fullscreen).grid(row=1,column=0)
Button(buttonframe1,text="<-------",height=3,width=8,justify=LEFT,command=left).grid(row=2,column=0)
Button(buttonframe1,text="------->",height=3,width=8,justify=LEFT,command=right).grid(row=2,column=1)

root.mainloop()           #important for closing the root=Tk()