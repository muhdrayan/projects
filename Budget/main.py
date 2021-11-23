import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import *
import sqlite3


class Budget:

	def __init__(self):

		self.scr = Tk()
		self.scr.title("My Finance")
		self.scr.geometry("300x220")
		self.scr.resizable(0,0)
		self.scr.config(bg="white")

		self.make_db()
		self.start_scr()

		self.scr.mainloop()

	def make_db(self):

		self.db = sqlite3.connect("money.db")
		self.c = self.db.cursor()

		self.c.execute("CREATE TABLE IF NOT EXISTS money_data(date_ TEXT, amount INTEGER)")
		self.db.commit()

		self.c.execute("CREATE TABLE IF NOT EXISTS goal(amount INTEGER)")
		self.db.commit()

		self.c.execute("CREATE TABLE IF NOT EXISTS current(amount INTEGER)")
		self.db.commit()


	def start_scr(self):
		
		finance_lb = Label(self.scr, text="My Money", font=("Roboto", 20, "bold"), bg="white")
		finance_lb.pack(pady=10)

		chart = Button(self.scr, text="Money Graph", font=("Roboto", 15, "bold"), bg="black", fg="white", command=self.show_money_chart)
		chart.pack(pady=5)

		add = Button(self.scr, text= "Add Data", font=("Roboto", 15, "bold"), bg="black", fg="white", command=self.add_new_data)
		add.pack(pady=5)

		analysis = Button(self.scr, text="Analysis", font=("Roboto", 15, "bold"), bg="black", fg="white", command=self.analysis)
		analysis.pack(pady=5)

	def show_money_chart(self):

		# Get data
		self.c.execute("SELECT * FROM money_data")
		information = self.c.fetchall()

		dates = []
		amounts = []

		for info in information:
			dates.append(info[0])
			amounts.append(info[1])

		if dates != []:
			plt.plot(dates, amounts)
			plt.show() 

	def add_new_data(self):

		# Adding data

		self.add_scr = Tk()
		self.add_scr.title("Add Data")
		self.add_scr.geometry("300x150")
		self.add_scr.resizable(0,0)
		self.add_scr.config(bg="white")

		date = Entry(self.add_scr, borderwidth=1, justify="center", font=("Roboto", 10))
		date.pack(pady=10)

		amount = Entry(self.add_scr, borderwidth=1, justify="center", font=("Roboto", 10))
		amount.pack(pady=10)

		add_btn = Button(self.add_scr, text= "Add Data", font=("Roboto", 15, "bold"), bg="black", fg="white",
		 command=lambda:self.ad_d2(date.get(), amount.get()))
		add_btn.pack(pady=10)


	def ad_d2(self, date, amount):

		self.c.execute("INSERT INTO money_data values(?,?)", (date, int(amount)))
		self.db.commit()

		messagebox.showinfo("Successful", f"Data was successfuly added for {date}")
		self.add_scr.destroy()

	def analysis(self):

		# Analyse current data

		self.c.execute("SELECT * FROM money_data")
		information = self.c.fetchall()

		money_data = {}

		for info in information:
			money_data[info[0]] = info[1]

		self.c.execute("SELECT * FROM goal")
		information2 = self.c.fetchall()

		if len(money_data) != 0:
	

			change = int(money_data[-1]) - int(money_data[-2])

			color = []

			if change < 0:
				color.append("red", "")
			elif change > 0:
				color.append("green", "+")
			else:
				color.append("black", "") 

			self.an_scr = Tk()
			self.an_scr.title("Analysis")
			self.an_scr.geometry("750x750")
			self.an_scr.resizable(0,0)
			self.an_scr.config(bg="white")

			total = Label(self.an_scr, text=f"Total: {current_amount} QR", bg="white", font=("Roboto", 25, "bold"))
			total_lb.place(x=10, y=10)

			change_lb = Label(self.an_scr, text=f"{color[1]}{change}", bg="white", fg=color[0], font=("Roboto", 7))
			change_lb.place(x=15, y=50)

		else:
			messagebox.showerror("No data", "No data to analyse")



		
budgetting = Budget()


