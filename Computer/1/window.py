from tkinter import *

scr = Tk()
scr.geometry("422x300")
scr.configure(bg = "#ffffff")
scr.title("Windows 1")

canvas = Canvas(scr, bg = "#ffffff", height = 300, width = 422, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(211.0, 150.0,image=background_img)

scr.resizable(False, False)
scr.mainloop()
