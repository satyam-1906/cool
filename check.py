import tkinter

def dimensions():
    global root
    root = tkinter.Tk()
    return [root.winfo_screenwidth(), root.winfo_screenheight()]

def destroy():
    root.destroy()