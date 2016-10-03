"""
Python Tkinter Splash Screen

This script holds the class SplashScreen, which is simply a window without
the top bar/borders of a normal window.

The window width/height can be a factor based on the total screen dimensions
or it can be actual dimensions in pixels. (Just edit the useFactor property)

Very simple to set up, just create an instance of SplashScreen, and use it as
the parent to other widgets inside it.

www.sunjay-varma.com
"""

from Tkinter import *
x = 0

class SplashScreen(Frame):
    def __init__(self, master=None, width=0.4, height=0.2, useFactor=True):
        Frame.__init__(self, master)
        self.pack(expand=YES, fill=BOTH)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2) 
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.master.overrideredirect(True)
        self.lift()

def func():
    global x
    x += 2
    p.config(padx=x)
    if x > 271:
        root.after(0, lambda: root.destroy())
        
    root.after(2,func)

if __name__ == '__main__':
    root = Tk()

    sp = SplashScreen(root)
    sp.config(bg="#836ff1")

##    photo = PhotoImage(file="bg2.gif")
    m = Label(sp, text="IT Network Programming")
    m.pack(side=TOP, expand=YES)
##    m.config(bg="#3366ff", justify=CENTER, font=("calibri", 29))
    m.config(bg="#836ff1", justify=CENTER, font=("arial", 30), foreground="black")
    m2 = Label(sp, text="client server comiunication with multi-threading")
    m2.pack(side=TOP, expand=YES)
##    m.config(bg="#3366ff", justify=CENTER, font=("calibri", 29))
    m2.config(bg="#836ff1", justify=CENTER, font=("arial", 15), foreground="black")
    p = Label(sp, text="")
    p.pack(side=LEFT)
    p.config(bg="#0DFF00", justify=CENTER, font=("calibri", 1), relief=FLAT, padx=x, bd=0)
    
    
##    Button(sp, text="Close", bg='red', command=root.destroy).pack()
##    root.after(5000, lambda: root.destroy())
    root.after(1000,func)
    root.mainloop()

