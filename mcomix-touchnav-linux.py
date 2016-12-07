#! /usr/bin/env python2.7
# coding=UTF-8
from time import sleep
import thread

# python libxcb bindings (xcffib):
import xcffib
import xcffib.xproto
import xcffib.xtest

#================<CONFIG>================#

# no_wm :
#   when set to True, program does not have a window border and is moved by additional buttons.
#   when set to False, program is draggable via your window manager.
#   default is True.
global no_wm
no_wm=True

# hax :
#   when set to 1, program kills the program 'mate-panel' and relauunches it when entering and exiting fullscreen
#   to stop it from sitting above the fullscreen window. 'mate-panel' is hardcoded, like most of the rest of this
#   program. Sorry. I'm just amazed this program  works at all, honestly. It's based on one of the earliest programs
#   I wrote that I still have source code for! It works more like assembly language or Commodore BASIC than Python...
global hax
hax=0

# delay_ms :
#   window selection delay, in milliseconds. After hitting the 'select' button you have this many milliseconds to
#   set input focus to the window you want to control. Default is 3000 (3 seconds.)
global delay_ms
delay_ms=3000

#================</CONFIG>===============#

if(hax==1):
    import os # only needed for an ugly hack to kill mate-panel when entering
              # fullscreen.

# this is not part of config. It is an easy way for the program to retain an idea of when it is in fullscreen and
# not.
global full_screen
full_screen=0

# connection might be used anywhere (of course).
global connection
connection = xcffib.connect()

global window_selected
window_selected=False

def winget():
    global delay_ms
    root.after(delay_ms,getwindow)

def getwindow():
    global inputWindow
    global window_selected
    connection.flush()
    windowCookie = connection.core.GetInputFocus().reply()
    # 'focus' is the window's ID.
    inputWindow = windowCookie.focus
    window_selected=True
    print inputWindow

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
        print "No window has been selected! Select a window and then try again."

def right():
    global shell
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        typeright()
    else:
        print "No window has been selected! Select a window and then try again."

def killPanel():
# hax again
    global hax
    if(hax == 1):
        os.system("killall mate-panel")

def fullscreen():
    global shell
    global full_screen
    global root
    global hax
    global window_selected
    if(window_selected==True):
        xtest.conn.core.SetInputFocus(xcffib.xproto.InputFocus.Parent, inputWindow, xcffib.CurrentTime)
        if(full_screen == 0):
            # {
            killPanel()
            full_screen=1
            root.wm_attributes("-fullscreen", 1)
            # }

        else:
            if(hax == 1):
            # {
                os.system("mate-panel --replace 2>&1 1>/dev/null &")
            # }
            root.wm_attributes("-fullscreen",0)
            full_screen=0
        typef()
    else:
        print "No window has been selected! Select a window and then try again."


def typeleft():
    # 117 is the 'Page Up' key on a ANSI layout keyboard (U.S. layout 101-key IBM PC 'Enhanced Keyboard.')
    pressKey(112)

def typeright():
    # 117 is the 'Page Down' key on a ANSI layout keyboard (U.S. layout 101-key IBM PC 'Enhanced Keyboard.')
    pressKey(117)

def typef():
    # 41 is the 'f' key on a ANSI layout keyboard (U.S. layout 101-key IBM PC 'Enhanced Keyboard.')
    pressKey(41)

def topleft():
    root.geometry('+0+0')

def topright():
    root.geometry('-0+0')

def btmleft():
    root.geometry('+0-0')

def btmright():
    root.geometry('-0-0')

global xtest
xtest=connection(xcffib.xtest.key)
global inputWindow


from Tkinter import *
global root
root=Tk()  #holder

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

buttonframe=Frame(root)
buttonframe1=Frame(buttonframe)
buttonframe2=Frame(buttonframe)

buttonframe.grid(row=0,column=1)
buttonframe1.grid(row=0,column=0,rowspan=2)
buttonframe2.grid(row=0,column=2,rowspan=2)

#
# 'move window' buttons
# only needed if you have the window manager control of the window disabled.
if(no_wm == True):
# {
    Button(buttonframe2,text="↖",height=1,width=1,justify=LEFT,font=(None,8),command=topleft).grid(row=0,column=3)
    Button(buttonframe2,text="↗",height=1,width=1,justify=LEFT,font=(None,8),command=topright).grid(row=0,column=4)
    Button(buttonframe2,text="↙",height=1,width=1,justify=LEFT,font=(None,8),command=btmleft).grid(row=1,column=3)
    Button(buttonframe2,text="↘",height=1,width=1,justify=LEFT,font=(None,8),command=btmright).grid(row=1,column=4)
#    Button(buttonframe2,text="X",height=3,width=1,justify=LEFT,font=(None,8),command=root.destroy).grid(row=0,column=5,rowspan=2)
    Button(buttonframe2,text="❌",height=3,width=1,justify=LEFT,font=(None,8),command=root.destroy).grid(row=0,column=5,rowspan=2)
# }

Button(buttonframe2,text="Select",height=1,width=3,justify=LEFT,font=(None,8),command=winget).grid(row=0,column=2)
Button(buttonframe2,text="FScreen",height=1,width=3,justify=LEFT,font=(None,8),command=fullscreen).grid(row=1,column=2)
Button(buttonframe1,text="<-------",height=3,width=3,justify=LEFT,font=(None,8),command=left).grid(row=0,column=0)
Button(buttonframe1,text="------->",height=3,width=3,justify=LEFT,font=(None,8),command=right).grid(row=0,column=1)

def on_close():
    # connection is disconnected when the TK window closes.
    # the program (and thus connection) can also be aborted via ctrl+\ (SIGQUIT)
    # in a terminal.
    connection.disconnect()
    root.destroy()

root.mainloop()           #important for closing the root=Tk()

