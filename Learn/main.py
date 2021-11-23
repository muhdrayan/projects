from tkinter import *
import ctypes

class Login:
    def __init__(self):

        self.scr = Tk()
        self.scr.geometry("700x550")
        self.scr.title("Learning App")
        self.scr.config(bg="white")

        self.create_screen()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


        self.scr.mainloop()

    def create_screen(self):

        learn_title = Label(self.scr, text="Learn", bg="white", fg="#333333", font=("Roboto", 40, "bold"))
        learn_title.pack(pady=35)

        login_btn = Button(self.scr, text="Login", bg="#333333", fg="white", font=("Roboto", 30, "bold"),
                           width=10)
        login_btn.pack(pady=20)
        sign_up_btn = Button(self.scr, text="Sign Up", bg="#333333", fg="white")



make_scr = Login()