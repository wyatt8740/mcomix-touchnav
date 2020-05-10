#! /usr/bin/env python3
# coding=UTF-8
from time import sleep
#import thread
# in python 3 it is called 'threading'
import threading

# python libxcb bindings (xcffib):
import xcffib
import xcffib.xproto
import xcffib.xtest

import os
import sys
#================<CONFIG>================#

filename="/home/wyatt/.touchnavid"


# no_wm :
#   when set to True, program does not have a window border and is moved by additional buttons.
#   when set to False, program is draggable via your window manager.
#   default is True.
global no_wm
# no_wm=True
no_wm=False

# extended_controls:
#   when true, extended functionality buttons are present
global extended_controls
extended_controls=True


# corner_controls :
#   when set to True, the corner controls (always visible when no_wm is set) are visible, regardless
#   of if the WM is managing the window.
global corner_controls
corner_controls=True

# hax :
#   when set to 1, program kills the program 'mate-panel' and relauunches it when entering and exiting
#   fullscreen to stop it from sitting above the fullscreen window. 'mate-panel' is hardcoded, like most
#   of the rest of this program. Sorry. I'm just amazed this program  works at all, honestly. It's based
#   on one of the earliest programs I wrote that I still have source code for! It works more like
#   assembly language or Commodore BASIC than Python...
global hax
hax=0

# Will the next 'wide' button press fit to height or fit to width?
global wideset
wideset=0

# delay_ms :
#   window selection delay, in milliseconds. After hitting the 'select' button you have this many
#   milliseconds to set input focus to the window you want to control. Default is 3000 (3 seconds.)
global delay_ms
delay_ms=3000

#================</CONFIG>===============#

# if(hax==1):
#    import os # only needed for an ugly hack to kill mate-panel when entering
              # fullscreen.

# this is not part of config. It is an easy way for the program to retain an idea of when it is in
# fullscreen and not. Lazy, though.
global full_screen
full_screen=0

global portrait
portrait=False

# connection might be used anywhere (of course).
global connection
connection = xcffib.connect()

global window_selected
global inputWindow

# allow passing window ID as argument to script. This allows for reloading the
# 'widget' without having to re-select the window to control each time.
if (len(sys.argv) == 3 ) :
    if (sys.argv[1]=="-win") :
        window_selected=True
        inputWindow=int(sys.argv[2])
    if (sys.argv[1]=="-rot") :
        if (sys.argv[2]=="portrait") :
            portrait=True
        else :
            portrait=False

elif (len(sys.argv) == 5) :
    if (sys.argv[1]=="-win") :
        window_selected=True
        inputWindow=int(sys.argv[2])
    elif (sys.argv[3]=="-win") :
        window_selected=True
        inputWindow=int(sys.argv[4])
    if (sys.argv[1]=="-rot") :
        if (sys.argv[2]=="portrait") :
            portrait=True
        else :
            portrait=False
    elif (sys.argv[3]=="-rot") :
        if (sys.argv[4]=="portrait") :
            portrait=True
        else :
            portrait=False

else:
    window_selected=False
    portrait=False

if (not window_selected): # cli args override this methodology
    if(not os.path.exists(filename)):
        f=open(filename,'w')
    else:
        f=open(filename,'r')
        f.seek(0)
        teststr=f.readline()
        if teststr=='' or teststr=='\n':
           print("Could not read a window ID from "+filename+". Clearing file." )
           f.close()
           f=open(filename,'w')
        else:
           inputWindow=teststr
           window_selected=True


def winget():
    global delay_ms
    root.after(delay_ms,getwindow)

def getwindow():
    global f # persist file
    global filename
    global inputWindow
    global window_selected
    connection.flush()
    windowCookie = connection.core.GetInputFocus().reply()
    # 'focus' is the window's ID.
    inputWindow = windowCookie.focus
    window_selected=True
    print(inputWindow)
    f.close() # erase file
    f=open(filename,'w')
    f.write(str(inputWindow)+'\n')
    f.close()
    f=open(filename,'r')

def pressKey(keyCode):
    XTEST_EVENTS = {
        'KeyPress': 2,
        'KeyRelease': 3,
        'ButtonPress': 4,
        'ButtonRelease': 5,
        'MotionNotify': 6
    }
    # send keycode to X server
    xtest.FakeInput(XTEST_EVENTS['KeyPress'],keyCode,xcffib.CurrentTime, inputWindow, 0,0,0,is_checked=True)
    xtest.FakeInput(XTEST_EVENTS['KeyRelease'],keyCode,xcffib.CurrentTime, inputWindow, 0,0,0,is_checked=True)
    connection.flush()

def left():
    global shell
    global window_selected
    if(window_selected==True):
        # set focused window
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typeleft()
    else:
        print("No window has been selected! Select a window and then try again.")

def right():
    global shell
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typeright()
    else:
        print("No window has been selected! Select a window and then try again.")

def killPanel():
# hax again
    global hax
    if(hax == 1):
        os.system("killall mate-panel")

def pixelsize():
    global shell
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typea()
    else:
        print("No window has been selected! Select a window and then try again.")

def zoomin():
    global shell
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typeplus()
    else:
        print("No window has been selected! Select a window and then try again.")

def zoomout():
    global shell
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typeminus()
    else:
        print("No window has been selected! Select a window and then try again.")

def fitwidth():
    global shell
    global root
    global hax
    global window_selected
    global wideset
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        if(wideset==0):
            typew()
            wideset=1
        else:
            typeh()
            wideset=0
    else:
        print("No window has been selected! Select a window and then try again.")
        
def bestfit():
    global shell
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typeb()
    else:
        print("No window has been selected! Select a window and then try again.")

def rotate():
    global shell
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typer()
    else:
        print("No window has been selected! Select a window and then try again.")
        
def fullscreen():
    global shell
    global full_screen
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typef()
    else:
        print("No window has been selected! Select a window and then try again.")


def typeleft():
    # 117 is the 'Page Up' key on a ANSI layout keyboard (U.S. layout 101-key IBM PC 'Enhanced Keyboard.')
    pressKey(112)

def typeright():
    # 117 is the 'Page Down' key on a ANSI layout keyboard (U.S. layout 101-key IBM PC 'Enhanced Keyboard.')
    pressKey(117)

def typeb():
    pressKey(56)

def typea():
    pressKey(38)

def typeplus(): #numpad plus has a unique keycode, unlike +/= key
    pressKey(86)

def typeminus():
    pressKey(20)

def typef():
    # 41 is the 'f' key on a ANSI layout keyboard (U.S. layout 101-key IBM PC 'Enhanced Keyboard.')
    pressKey(41)

def typer():
    # 'r' ansi
    pressKey(27)

def typew():
    # 'w' ansi
    pressKey(25)

def typeh():
    # 'h' ansi
    pressKey(43)

def topleft():
    root.geometry('+0+0')
def topright():
    root.geometry('-0+0')
def btmleft():
     root.geometry('+0-0')
def btmright():
    root.geometry('-0-0')

def callback():
    return
    
def reload():
    global inputWindow
    global root
    root.destroy()
    root=Tk()  # reload
    root["bg"]="#424242"
    root.configure(background="#424242")
    root.title("touchnav")
    python = sys.executable
#    os.execl(python, python, * sys.argv)
# Pass
    try:
        str(inputWindow)
    except NameError:
        inputWindow=""
    if(str(inputWindow) == ""):
        if(portrait==False):
            os.execl(python, python, sys.argv[0])
        else:
            os.execl(python, python, sys.argv[0], "-rot", "portrait")
    else:
        if(portrait==False):
            os.execl(python, python, sys.argv[0], "-win", str(inputWindow))
        else:
            os.execl(python, python, sys.argv[0], "-win", str(inputWindow), "-rot", "portrait")
            
global xtest
xtest=connection(xcffib.xtest.key)
# global inputWindow

# python 2
#from Tkinter import *
# python 3
from tkinter import *

global root
root=Tk()  #holder
root.configure(background='#424242')
root.title("touchnav")
root.resizable(width=FALSE, height=FALSE)
root.resizable(0,0)

if(no_wm == True):
# {
    # do not let the window manager take control of the window.
    root.overrideredirect(True)
    root.attributes('-fullscreen', True)
    # root.overrideredirect(no_wm)
# }

root.wm_attributes("-type",['_NET_WM_WINDOW_TYPE_DOCK'])
root.wm_attributes("-topmost", 1) # always on top, works for me (tm)

buttonframe=Frame(root,bg="#424242")
buttonframe1=Frame(buttonframe,bg="#424242")
buttonframe2=Frame(buttonframe,bg="#424242")
buttonframe3=Frame(buttonframe,bg="#424242")

if(portrait == False):
    buttonframe.grid(row=0,column=1)
    buttonframe1.grid(row=0,column=0,rowspan=2)
    buttonframe2.grid(row=0,column=2,rowspan=2)
    buttonframe3.grid(row=0,column=10,rowspan=2)
else:
    buttonframe.grid(row=1,column=0)
    buttonframe1.grid(row=10,column=0,rowspan=2)
    buttonframe2.grid(row=2,column=0,rowspan=2)
    buttonframe3.grid(row=15,column=0,rowspan=2)


if(portrait == False):
#
# 'move window' buttons
# only needed if you have the window manager control of the window disabled.
    if(no_wm == True or corner_controls == True):
# {
        Button(buttonframe2,text="↖",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=topleft).grid(row=0,column=3)
        Button(buttonframe2,text="↗",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=topright).grid(row=0,column=4)
        Button(buttonframe2,text="↙",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=btmleft).grid(row=1,column=3)
        Button(buttonframe2,text="↘",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=btmright).grid(row=1,column=4)
        #    Button(buttonframe2,text="1:1",height=1,width=1,justify=LEFT,font=(None,8),command=pixelsize).grid(row=0,column=5,rowspan=1)
        #    Button(buttonframe2,text="Fit",height=1,width=1,justify=LEFT,font=(None,8),command=bestfit).grid(row=1,column=5,rowspan=1)
        #    Button(buttonframe2,text="+",height=1,width=1,justify=LEFT,font=(None,8),command=zoomin).grid(row=0,column=6,rowspan=1)
        #    Button(buttonframe2,text="−",height=1,width=1,justify=LEFT,font=(None,8),command=zoomout).grid(row=1,column=6,rowspan=1)
        Button(buttonframe3,text="❌",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=root.destroy).grid(row=0,column=7,rowspan=1)
        Button(buttonframe3,text="⟳",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=reload).grid(row=1,column=7,rowspan=1)
        # }
        
        if( extended_controls == True ):
            Button(buttonframe2,text="1:1",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=pixelsize).grid(row=0,column=5,rowspan=1)
            Button(buttonframe2,text="fit",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=bestfit).grid(row=1,column=5,rowspan=1)
            Button(buttonframe2,text="r",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=rotate).grid(row=0,column=6,rowspan=1)
            Button(buttonframe2,text="w/h",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=fitwidth).grid(row=1,column=6,rowspan=1)
            Button(buttonframe2,text="+",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=zoomin).grid(row=0,column=7,columnspan=2)
            Button(buttonframe2,text="−",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=zoomout).grid(row=1,column=7,columnspan=2) 
            
            Button(buttonframe2,text="Select",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=3,justify=LEFT,font=(None,8),command=winget).grid(row=0,column=2)
            Button(buttonframe2,text="FullScr",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=3,justify=LEFT,font=(None,8),command=fullscreen).grid(row=1,column=2)
            Button(buttonframe1,text="<-------",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=3,width=3,justify=LEFT,font=(None,8),command=left).grid(row=0,column=0)
            Button(buttonframe1,text="------->",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=3,width=3,justify=LEFT,font=(None,8),command=right).grid(row=0,column=1)
            #Button(buttonframe1,text="<-----",height=1,width=2,justify=LEFT,font=(None,8),command=left).grid(row=0,column=0)
            #Button(buttonframe1,text="----->",height=1,width=2,justify=LEFT,font=(None,8),command=right).grid(row=1,column=0)
else:
    if(no_wm == True or corner_controls == True):
        Button(buttonframe2,text="↖",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=topleft).grid(row=3,column=0)
        Button(buttonframe2,text="↗",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=topright).grid(row=3,column=1)
        Button(buttonframe2,text="↙",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=btmleft).grid(row=4,column=0)
        Button(buttonframe2,text="↘",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=btmright).grid(row=4,column=1)
        #    Button(buttonframe2,text="1:1",height=1,width=1,justify=LEFT,font=(None,8),command=pixelsize).grid(row=5,column=0,rowspan=1)
        #    Button(buttonframe2,text="Fit",height=1,width=1,justify=LEFT,font=(None,8),command=bestfit).grid(row=5,column=1,rowspan=1)
        #    Button(buttonframe2,text="+",height=1,width=1,justify=LEFT,font=(None,8),command=zoomin).grid(row=6,column=0,rowspan=1)
        #    Button(buttonframe2,text="−",height=1,width=1,justify=LEFT,font=(None,8),command=zoomout).grid(row=6,column=1,rowspan=1)
        Button(buttonframe3,text="❌",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=root.destroy).grid(row=1,column=1,rowspan=1)
        Button(buttonframe3,text="⟳",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=reload).grid(row=1,column=0,rowspan=1)
        # }
        
        if( extended_controls == True ):
            Button(buttonframe2,text="1:1",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=pixelsize).grid(row=5,column=0,rowspan=1)
            Button(buttonframe2,text="fit",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=bestfit).grid(row=5,column=1,rowspan=1)
#            Button(buttonframe2,text="fit",height=1,width=3,justify=LEFT,font=(None,8),command=bestfit).grid(row=5,column=1,rowspan=1)
            Button(buttonframe2,text="r",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=rotate).grid(row=6,column=6,rowspan=1)
            Button(buttonframe2,text="w/h",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=fitwidth).grid(row=6,column=6,rowspan=1)
            Button(buttonframe2,text="+",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=zoomin).grid(row=7,column=0,rowspan=1)
            Button(buttonframe2,text="−",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=zoomout).grid(row=7,column=1,rowspan=1)
            
            Button(buttonframe3,text="Sel",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=winget).grid(row=0,column=0)
            Button(buttonframe3,text="FSc",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=1,width=1,justify=LEFT,font=(None,8),command=fullscreen).grid(row=0,column=1)
            Button(buttonframe1,text="<-----",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=3,width=3,justify=LEFT,font=(None,8),command=left).grid(row=0,column=0)
            Button(buttonframe1,text="----->",relief="flat",highlightbackground="#282828",bg="#424242",activebackground="#424242",fg="#848484",activeforeground="#848484",height=3,width=3,justify=LEFT,font=(None,8),command=right).grid(row=1,column=0)
            #Button(buttonframe1,text="<-----",height=1,width=2,justify=LEFT,font=(None,8),command=left).grid(row=0,column=0)
            #Button(buttonframe1,text="----->",height=1,width=2,justify=LEFT,font=(None,8),command=right).grid(row=1,column=0)

        

def on_close():
    # connection is disconnected when the TK window closes.
    # the program (and thus connection) can also be aborted via ctrl+\ (SIGQUIT)
    # in a terminal.
    # inputWindow saved to file for next run (useful for restarts)
    global f
    f.close() # close file descriptor for persist file
    if window_selected: # inputWindow is set
        persistfile.close()
    
    connection.disconnect()
    root.destroy()


root.mainloop()           #important for closing the root=Tk()

