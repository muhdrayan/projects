import subprocess, pyautogui, time
from database import Database
from datetime import datetime
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
from pathlib import Path
from tkinter import ttk
from tkinter import *





class ZoomBot:
    def __init__(self):

        self.db = Database()

        self.start_screen = Tk()
        self.start_screen.geometry("450x200")
        self.start_screen.title("Zoom Meeting Auto Join v1.1")
        self.start_screen.resizable(0,0)
        self.start_screen.config(bg="#333333")

        self.start_up_screen()

        self.start_screen.mainloop()

    def start_up_screen(self):

        title = Label(self.start_screen, text="Zoom Meeting Auto-Join", font=("Roboto", 25, "bold"), bg="#333333", fg="#e0c68b")
        title.pack(pady=25)

        # Start button Image
        strt_button_image = PIL.Image.open("start_button.png")
        strt_button_image = PIL.ImageTk.PhotoImage(strt_button_image.resize((80, 50), PIL.Image.ANTIALIAS))

        start_button = Label(self.start_screen, image=strt_button_image, borderwidth=0)
        start_button.pack(pady=17)

        start_button.photo = strt_button_image
        start_button.bind("<Button-1>", self.check_period)

        settings_image = PIL.Image.open("settings.png")
        settings_image = PIL.ImageTk.PhotoImage(settings_image.resize((20, 20), PIL.Image.ANTIALIAS))

        settings_button = Label(self.start_screen, image=settings_image, borderwidth=0)
        settings_button.place(x=0, y=0)

        settings_button.photo = settings_image
        settings_button.bind("<Button-1>", self.preferences)


    def preferences(self, e=None):
        
        self.prf_scr = Toplevel()
        self.prf_scr.geometry("300x300")
        self.prf_scr.title("My Preferences")
        self.prf_scr.resizable(0,0)
        self.prf_scr.config(bg="#333333")

        self.db.c.execute("SELECT * FROM yourPreferences")
        information = self.db.c.fetchall()

        second_languages = []
        third_languages = []
        morals = []

        if len(information) == 0:

            second_languages = ["Second-Language","Hindi","Malayalam","Arabic","French","Tamil","Telugu"]
            third_languages = ["Third-Language","Hindi","Malayalam","Arabic","French","Tamil","Telugu"]
            morals = ["Islamic", "Value Education"]

        else:

            for info in information:
                second_languages.append(info[0])
                third_languages.append(info[1])
                morals.append(info[2])

        pref_title = Label(self.prf_scr, text="My Preferences", font=("Roboto", 20, "bold"), bg="#333333", fg="#e0c68b")
        pref_title.pack(pady=16)

        second_language_box = ttk.Combobox(self.prf_scr, values=second_languages, state="readonly", justify="center")
        second_language_box.pack(pady=14)

        second_language_box.current(newindex=0)

        third_language_box = ttk.Combobox(self.prf_scr, values=third_languages, state="readonly", justify="center")
        third_language_box.pack(pady=14)

        third_language_box.current(newindex=0)

        second_language_box.bind("<<ComboboxSelected>>", lambda command:self.eliminate_wrong_options_combobox(second_language_box,
                         third_language_box, second_languages, third_languages))

        moral_box = ttk.Combobox(self.prf_scr, values=morals)
        moral_box.pack(pady=14)

        moral_box.current(newindex=1)

        tick_icon = PIL.Image.open("tick_button2.png")
        tick_icon = PIL.ImageTk.PhotoImage(tick_icon.resize((40, 40), PIL.Image.ANTIALIAS))

        set_button = Label(self.prf_scr, image=tick_icon, borderwidth=0)
        set_button.pack(pady=10)

        set_button.photo = tick_icon
        set_button.bind("<Button-1>", lambda command:self.db.set_preferences(second_language_box.get(), third_language_box.get(), moral_box.get()))

    def eliminate_wrong_options_combobox(self, sl, tl, sl_opt, tl_opt):
        
        sl_pref = sl.get()
        tl_pref = tl.get()

        if sl_pref == "Hindi":
            tl_opt = ["Malayalam","Arabic","French","Tamil","Telugu"]

        else:
            tl_opt = ["Hindi"]

        tl.config(values=tl_opt)



    def check_period(self, e=None):

        self.start_screen.withdraw()
        messagebox.showinfo("Started!","The program has started!")

        round_num = 0
        

        while True:

            round_num += 1

            time_now = datetime.now().strftime("%H:%M")
            day = datetime.today().strftime("%A")

            print(f"\nRound {round_num} started at {time_now}!")

            period_num = self.db.find_period(time_now, day, self.start_screen)

            if period_num != None and period_num != "Stop" and period_num != "End":

                period_name = self.db.find_name(period_num, day)

                meeting_id = self.db.get_meeting_id(period_name)
                self.start_zoom(meeting_id)

                time.sleep(40)

            elif period_num == "Stop":

                print("End")

                messagebox.showinfo("Done!", "All the classes for today are done... :) So bye!")
                
                quit()

            elif period_num == "End":
                break

            else:
                print("There is no class in this round...")
                time.sleep(40)


    def start_zoom(self, id):

        print("starting zoom")
        
        # Opening Zoom
        subprocess.call(f"{str(Path.home())}//AppData//Roaming//Zoom//bin//Zoom.exe", shell=True)

        time.sleep(5)

        self.click_join_button(id)

    def click_join_button(self, id):

        home_menu = pyautogui.locateCenterOnScreen("home_menu.png")
        pyautogui.moveTo(home_menu)

        pyautogui.click()

        join_button = pyautogui.locateCenterOnScreen('join_button.png')
        pyautogui.moveTo(join_button)

        pyautogui.click()

        print(home_menu, join_button)

        if home_menu == None and join_button == None:
            
            time.sleep(3)

            home_menu = pyautogui.locateCenterOnScreen("home_menu.png")
            pyautogui.moveTo(home_menu)

            pyautogui.click()

            time.sleep(1)
            join_button = pyautogui.locateCenterOnScreen('join_button.png')
            pyautogui.moveTo(join_button)

            pyautogui.click()

            print("home_chat_button and join_button clicked")

        

        time.sleep(3)

        self.type_login_id(str(id))

    def type_login_id(self, id):

        print(f"writing id: {id}")
        pyautogui.write(id)

        self.join_meeting()

    def join_meeting(self):

        join_meeting_button = pyautogui.locateCenterOnScreen("join_meeting.png")
        pyautogui.moveTo(join_meeting_button)

        pyautogui.click()


classes = ZoomBot()
