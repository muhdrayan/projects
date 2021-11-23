from tkinter import messagebox
import sqlite3


class Database:

    def __init__(self):

        self.create_db()

    def create_db(self):

        self.db = sqlite3.connect("Timetable.db")
        self.c = self.db.cursor()

        self.c.execute("CREATE TABLE IF NOT EXISTS timetable8R(day TEXT, p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT, p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT)")
        self.db.commit()

        self.c.execute("CREATE TABLE IF NOT EXISTS timings8R(p1 TEXT, p2 TEXT, p3 TEXT, p4 TEXT, p5 TEXT, p6 TEXT, p7 TEXT, p8 TEXT, p9 TEXT)")
        self.db.commit()

        self.c.execute("CREATE TABLE IF NOT EXISTS yourPreferences(sl TEXT, tl TEXT, value_islamic TEXT)")
        self.db.commit()

        self.c.execute("CREATE TABLE IF NOT EXISTS id(main INTEGER, hindi_sl INTEGER, mal_tl INTEGER, mal_sl INTEGER, hindi_tl INTEGER, fren_sl INTEGER, french_sl INTEGER)")
        self.db.commit()

    def find_period(self, times, day, scr):

        self.c.execute("SELECT * FROM yourPreferences")
        information0 = self.c.fetchall()

        if len(information0) != 0:

            classes_on = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

            if day in classes_on:
                self.c.execute("SELECT * FROM timings8R")
                information = self.c.fetchall()

                for info in information:
                    print(times)
                    print(info)
                    if str(times) in info:
                        index_num = info.index(times)

                        print(index_num, " is the period number")

                        return index_num

                    else:
                        last_time = info[-1]

                        in_minutes = self.convert_time(last_time)
                        now_time = self.convert_time(times)

                        if now_time > in_minutes:
                            return "Stop"
            else:
                return None

        else:

            scr.deiconify()
            messagebox.showerror("Unsuccessful", "Please set your preferences before continuing!")
            return "End"


    def find_name(self, num, day):

        self.c.execute("SELECT * FROM timetable8R")
        information = self.c.fetchall()

        for info in information:
            if info[0] == day:

                print(info[num], "is the name of the period.")

                return info[num]                

    def get_meeting_id(self, name):

        self.c.execute("SELECT * FROM id")
        information = self.c.fetchall()
        
        self.nameX = []

        if name == "sl" or name == "tl" or name == "val":

            self.c.execute("SELECT * FROM yourPreferences")
            information2 = self.c.fetchall()
            

            for info in information2:
                print("accessed")
                if name == "sl":
                    print("It is supposed to be sl") 
                    self.nameX.append(f"{info[0]}_sl")
                elif name == "tl":
                    print("It is supposed to be tl")
                    self.nameX.append(f"{info[1]}_tl")
                else:
                    print("it is isl/val")
                    if info[2] == "Islamic":
                        self.nameX.append(f"{info[2]}")
                    else:
                        self.nameX.append("main")

        else:
            self.nameX.append("main")

        periods = {"main":0, "Hindi_sl":1,"Malayalam_tl":2, "Malayalam_sl":3, "Hindi_tl":4, "French_sl":5, "French_sl":6, "Islamic":7}

        print(self.nameX, "is the list")

        for info in information:
            dude = self.nameX[0]

            print(info[periods[dude]])

            return info[periods[dude]]

    def convert_time(self, time):

        hour = time[:2]
        minutes = time[3:]

        in_minutes = (int(hour) * 60) + int(minutes)

        return in_minutes

    def set_preferences(self, sl, tl, moral):
        
        if sl != "Second-Language" and tl != "Third-Language":
            
            self.c.execute("SELECT * FROM yourPreferences")
            information = self.c.fetchall()

            if len(information) != 0:
                self.c.execute("""UPDATE yourPreferences SET 
                                            sl = :sl,
                                            tl = :tl,
                                            value_islamic = :moral

                                            WHERE oid = :oid""", {

                                            "sl":sl,
                                            "tl":tl,
                                            "moral":moral,
                                            "oid":1
                                            })
                self.db.commit()

            else:
                self.c.execute("INSERT INTO yourPreferences values(?,?,?)", (sl, tl, moral))
                self.db.commit()


            messagebox.showinfo("Updated", "Woohoo! Your preferences were updated successfully!")


        else:
            messagebox.showerror("Unsuccessful", "Please recheck the Second Language and Third Language fields.")
            