from tkinter import ttk as ttk
from tkinter import *
from tkinter import messagebox
import random, sqlite3
import matplotlib.pyplot as plt
import numpy as np

gold_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10]
silver_values = [0, 1, 2, 3, 4, 5, 6, 7, -1, -2, -3, -4, -5, -6, -7]
bronze_values = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
iron_values = [0, 1, 2, 3, 4, -1, -2, -3, -4]


class StockMarket:
	

	def __init__(self):
		
		self.scr = Tk()
		self.scr.geometry("400x350")
		self.scr.title("Stock Market")
		self.scr.resizable(0,0)
		self.scr.config(bg="white")

		self.stk_db()
		self.start_scr()
		self.update_accounts()

		self.gold_lb = None
		self.gold_lb2 = None
		self.gold_c = None

		self.run1 = True
		self.run2 = False

		self.num = 1

		self.scr.after(0, self.auto_update)

		self.scr.mainloop()


	def on_scr_close(self, n=0):

		if n == 0:
			self.gold_lb = None
			self.analog_scr.destroy()	
		elif n == 1:
			self.gold_c = None
			self.inv_scr.destroy()
			
			

	def start_scr(self):
		
		try:
			stock_market_title = Label(self.scr, text="Stock Market", bg="white", fg="#333333", font=("Roboto", 30, "bold"))
			stock_market_title.pack(pady=10)

			values_btn = Button(self.scr, text="Values", bg="#333333", fg="white", font=("Roboto", 25, "bold"), 
				command=self.show_stock_values)
			values_btn.pack(pady=10)

			login_btn = Button(self.scr, text="Login", bg="#333333", fg="white", font=("Roboto", 25, "bold"),
				command=self.login)
			login_btn.pack(pady=10)

			premium_btn = Button(self.scr, text="Premium", bg="yellow", font=("Roboto", 25, "bold"), fg="#333333")
			premium_btn.pack(pady=10)

		except Exception as e:
			print(e, "is the error... 16")


	def show_stock_values(self):
		
		try:
			self.values_scr = Tk()
			self.values_scr.geometry("400x400")
			self.values_scr.title("Stock Values")
			self.values_scr.resizable(0,0)
			self.values_scr.config(bg="white")

			gold_btn = Button(self.values_scr, text="Gold Value", bg="#333333", fg="white", font=("Roboto", 20, "bold"),
				command=lambda:self.show_item_value("gold"))
			silver_btn = Button(self.values_scr, text="Silver Value", bg="#333333", fg="white", font=("Roboto", 20, "bold"),
				command=lambda:self.show_item_value("silver"))
			bronze_btn = Button(self.values_scr, text="Bronze Value", bg="#333333", fg="white", font=("Roboto", 20, "bold"),
				command=lambda:self.show_item_value("bronze"))
			iron_btn = Button(self.values_scr, text="Iron Value", bg="#333333", fg="white", font=("Roboto", 20, "bold"),
				command=lambda:self.show_item_value("iron"))
			analog_btn = Button(self.values_scr, text="Analog", bg="#333333", fg="white", font=("Roboto", 20, "bold"),
				command=self.analog_view)
			analog_btn.pack(pady=10)


			gold_btn.pack(pady=10)
			silver_btn.pack(pady=10)
			bronze_btn.pack(pady=10)
			iron_btn.pack(pady=10)

		except Exception as e:
			print(e, "is the error... 15")


	def show_item_value(self, item):

		self.c.execute(f"SELECT * FROM {item}")
		information = self.c.fetchall()

		value = []

		for info in information:
			value.append(info[0])

		plt.plot(value)
		plt.show()


	def stk_db(self):

		try:
			self.db = sqlite3.connect("stocks.db")
			self.c = self.db.cursor()

			self.db2 = sqlite3.connect("bank.db")
			self.c2 = self.db2.cursor()

			self.c.execute("CREATE TABLE IF NOT EXISTS stocks_name(items TEXT, current_value INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS gold(value INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS silver(value INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS bronze(value INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS iron(value INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS users(mobile INTEGER, credits INTEGER, profit INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS stock(mobile INTEGER, gold INTEGER, g_av INTEGER, silver INTEGER, s_av INTEGER, bronze INTEGER, b_av INTEGER, iron INTEGER, i_av INTEGER)")
			self.c.execute("CREATE TABLE IF NOT EXISTS premium(mobile INTEGER, days INTEGER, last_date INTEGER)")
			self.db.commit()

		except Exception as e:
			print(e, "is the error... 3")


	def update_accounts(self):

		try:
			self.c2.execute("SELECT * FROM users")
			information = self.c2.fetchall()

			self.c.execute("SELECT * FROM stock")
			information3 = self.c.fetchall()

			mobiles_bnk = []
			mobiles_stk = []
			mobiles_inv = []

			for info in information:
				mobiles_bnk.append(info[0])

			self.c.execute("SELECT * FROM users")
			information2 = self.c.fetchall()

			for info in information2:
				mobiles_stk.append(info[0])

			for info in information3:
				mobiles_inv.append(info[0])

			for mbl in mobiles_bnk:
				if mbl in mobiles_stk:
					pass
				else:
					self.c.execute("INSERT INTO users values(?,?,?)", (mbl, 0, 0))
					self.db.commit()

			for mbl in mobiles_bnk:
				if mbl in mobiles_inv:
					pass 
				else:
					self.c.execute("INSERT INTO stock values (?,?,?,?,?,?,?,?,?)", (mbl,0,0,0,0,0,0,0,0))
					self.db.commit()

		except Exception as e:
			print(e, "is the error... 4")


	def auto_update(self, n=1):

		print(f"Round {self.num}")

		self.num += 1

		inc = [random.choice(gold_values), random.choice(silver_values), random.choice(bronze_values), random.choice(iron_values)]
		
		items = {"gold":0, "silver":1, "bronze":2, "iron":3}

		if self.run1 or self.run2:

			self.c.execute("SELECT * FROM stocks_name")
			information = self.c.fetchall()
				

			for item in items:

				color = []

				x = items[item]

				if inc[x] < 0:
					color.append("red")
				elif inc[x] == 0:
					color.append("yellow")
				else:
					color.append("green")

				information_ = information[x]

				balance = int(information_[1])+inc[x]				

				if self.run1 or self.run2:

					self.c.execute("UPDATE stocks_name SET current_value = :m WHERE items = :i", {
   									"m":balance,
   									"i":item})
					self.c.execute(f"INSERT INTO {item} values(?)", (balance,))

					self.db.commit()

					c_item = item[0].upper() + item[1:]

					print(f"{item} {inc[x]} = {balance}")

					if self.gold_lb != None:
						self.lbl_update(c_item, color[0], balance)
					
					elif self.gold_lb2 != None:
						self.lbl_update(c_item, color[0], balance, n=1)

				else:

					print("Ended")
					return

			if self.run1:
				self.redo(1)
					
			elif self.run2:
				self.redo(2)
				print("2")

			else:

				print("Ended")
				return

		else:
			print("Ended")
			return

	def redo(self, i):

		if i == 1:
			self.scr.after(30000, self.auto_update)
		else:
			self.dsh_scr.after(30000, self.auto_update)


	def lbl_update(self, item, color, balance, n=0):

		if n == 0:
			try:
				if item == "Gold":
					self.gold_lb.config(bg=color, text=f"{item}:{balance}")
				elif item == "Silver":
					self.silver_lb.config(bg=color, text=f"{item}:{balance}")
				elif item == "Bronze":
					self.bronze_lb.config(bg=color, text=f"{item}:{balance}")
				else:
					self.iron_lb.config(bg=color, text=f"{item}:{balance}")
			except Exception as e:
				print(e, "is the error... 1")

		elif n == 1:

			try:
				if item == "Gold":
					self.gold_c.config(bg=color, text=balance)
				elif item == "Silver":
					self.silver_c.config(bg=color, text=balance)
				elif item == "Bronze":
					self.bronze_c.config(bg=color, text=balance)
				else:
					self.iron_c.config(bg=color, text=balance)
			except Exception as e:
				print(e, "is the error... 2")
		elif n == 2:

			pass



	def analog_view(self):

		try:
			self.analog_scr = Tk()
			self.analog_scr.geometry("400x400")
			self.analog_scr.title("Analog View")
			self.analog_scr.resizable(0,0)
			self.analog_scr.config(bg="white")

			self.analog_scr.protocol("WM_DELETE_WINDOW", self.on_scr_close)

			self.c.execute("SELECT * FROM stocks_name")
			information = self.c.fetchall()

			costs = []

			for info in information:
				costs.append(info[1])

			self.gold_lb = Button(self.analog_scr, text=f"Gold:{costs[0]}", bg="white", fg="#333333", font=("Roboto", 30, "bold"))
			self.silver_lb = Button(self.analog_scr, text=f"Silver:{costs[1]}", bg="white", fg="#333333", font=("Roboto", 30, "bold"))
			self.bronze_lb = Button(self.analog_scr, text=f"Bronze:{costs[2]}", bg="white", fg="#333333", font=("Roboto", 30, "bold"))
			self.iron_lb = Button(self.analog_scr, text=f"Iron:{costs[3]}", bg="white", fg="#333333", font=("Roboto", 30, "bold"))

			self.gold_lb.pack(pady=10)
			self.silver_lb.pack(pady=10)
			self.bronze_lb.pack(pady=10)
			self.iron_lb.pack(pady=10)

		except Exception as e:
			print(e, "is the error... 13")


	def login(self):

		try:
			self.login_scr = Tk()
			self.login_scr.title("Login")
			self.login_scr.geometry("425x375")
			self.login_scr.resizable(0,0)
			self.login_scr.config(bg="white")

			self.login1_frame = Frame(self.login_scr, bg="white")
			self.login1_frame.pack()

			title = Label(self.login1_frame, text="Account Login", fg="#333333", bg="white", font=("Roboto", 25, "bold"),
				borderwidth=0)
			title.pack(pady=20)

			mob_n_lb = Label(self.login1_frame, text="Mobile Num:", fg="#333333", bg="white", font=("Roboto", 15, "bold"),
				borderwidth=0)
			mob_n_lb.pack(pady=10)

			mob_n_entry = Entry(self.login1_frame, fg="#333333", bg="white", font=("Roboto", 12, "bold"), borderwidth=1,
				justify="center", width=20)
			mob_n_entry.pack(pady=10)

			pincode1_lb = Label(self.login1_frame, text="Pincode 1:", fg="#333333", bg="white", font=("Roboto", 15, "bold"),
				borderwidth=0)
			pincode1_lb.pack(pady=10)

			pincode1_entry = Entry(self.login1_frame, fg="#333333", bg="white", font=("Roboto", 12, "bold"), borderwidth=1,
				width=10, justify="center")
			pincode1_entry.pack(pady=10)

			continue_btn = Button(self.login1_frame, text="Continue", bg="#333333", fg="white", borderwidth=0,
			 font=("Roboto", 15, "bold"), command=lambda:self.x(mob_n_entry.get(), pincode1_entry.get(), n=1))
			continue_btn.pack(pady=15)

			pincode1_entry.bind("<Return>", lambda x:self.x(mob_n_entry.get(), pincode1_entry.get(), n=1))

		except Exception as e:
			print(e, "is the error... 12")


	def x(self, a, b, n=2, c=None, d=None, e=None , f=None):

		try:
			if n == 1:
				result = self.verify_pin1(a, b)

				self.mob = a
				if result == "Correct":
					self.login2()

			elif n == 2:
				result = self.verify_pin2(self.mob, b)

				if result == "Correct":
					self.dashboard()

		except Exception as e:
			print(e, "is the error... 11")

	def login2(self):
		
		try:
			self.login1_frame.destroy()
			self.login_scr.geometry("425x275")

			title = Label(self.login_scr, text="Account Login", fg="#333333", bg="white", font=("Roboto", 25, "bold"),
				borderwidth=0)
			title.pack(pady=20)

			pincode2_lb = Label(self.login_scr, text="Pincode 2:", fg="#333333", bg="white", font=("Roboto", 15, "bold"),
				borderwidth=0)
			pincode2_lb.pack(pady=10)

			pincode2_entry = Entry(self.login_scr, fg="#333333", bg="white", font=("Roboto", 12, "bold"), borderwidth=1,
				width=7, justify="center")
			pincode2_entry.pack(pady=10)

			continue_btn = Button(self.login_scr, text="Verify", bg="#333333", fg="white", borderwidth=0,
			 font=("Roboto", 15, "bold"), command=lambda:self.x(self.mob, pincode2_entry.get()))
			continue_btn.pack(pady=15)

			pincode2_entry.bind("<Return>", lambda x:self.x(self.mob, pincode2_entry.get()))
		
		except Exception as e:
			print(e, "is the error... 10")


	def verify_pin1(self, mob, pin):

		try:
			self.c2.execute("SELECT * FROM users")
			information = self.c2.fetchall()

			numbers = []

			for info in information:
				numbers.append(int(info[0]))

			if int(mob) in numbers:
				pass 
			else:
				messagebox.showerror("Incorrect", "No bank account registered with that mobile number. Please try again or register with the help of an employee.")
				return None

			for info in information:
				if int(mob) == info[0] and pin == info[1]:
					return "Correct" 
					
			messagebox.showerror("Incorrect", "The mobile number or pincode you entered is incorrect. Please try again.")
			return None

		except Exception as e:
			print(e, "is the error... 9")


	def verify_pin2(self, mob, pin2):

		try:
			mob = int(mob)

			self.c2.execute("SELECT * FROM users")
			information = self.c2.fetchall()

			pincode = []

			for info in information:
				if info[0] == mob:
					pincode.append(info[3])

			if pin2 == pincode[0]:
				return "Correct"
			else:
				messagebox.showerror("Incorrect", "Pincode is incorrect, please try again.")
		except Exception as e:
			print(e, "is the error... 8")



	def dashboard(self):

		try:
			self.login_scr.destroy()

			self.run1 = False
			self.run2 = True

			self.scr.destroy()

			self.dsh_scr = Tk()
			self.dsh_scr.title("Dashboard")
			self.dsh_scr.geometry("700x500")
			self.dsh_scr.resizable(0,0)
			self.dsh_scr.config(bg="white")


			self.c.execute(f"SELECT *, oid FROM users WHERE mobile={self.mob}")
			information = self.c.fetchall()

			self.information = information[0]

			main_w = PanedWindow(self.dsh_scr, bg="red", orient=VERTICAL)
			main_w.pack(fill=BOTH, expand=1, pady=10)

			top_w = PanedWindow(main_w, bg="white", orient=VERTICAL)
			main_w.add(top_w)

			bottom_w = PanedWindow(main_w, bg="white", orient=HORIZONTAL)
			main_w.add(bottom_w)

			self.credits_lb = Label(top_w, text=f"Credits: {self.information[1]}", bg="white", fg="#333333", font=("Roboto", 30, "bold"),
				height=2)
			top_w.add(self.credits_lb)

			mobile_n_lb = Label(top_w, text=f"Mobile Number: {self.mob}", bg="white")
			top_w.add(mobile_n_lb)

			bank_w = PanedWindow(bottom_w, orient=VERTICAL)
			bottom_w.add(bank_w)

			stock_w = PanedWindow(bottom_w, orient=VERTICAL)
			bottom_w.add(stock_w)

			bank_lb = Label(bank_w, text="Bank", fg="#333333", font=("Roboto", 20, "bold"), width=20)
			bank_w.add(bank_lb)

			stock_lb = Label(stock_w, text="Stocks", fg="#333333", font=("Roboto", 20, "bold"))
			stock_w.add(stock_lb)

			convert_btn = Button(bank_w, text="Convert Bits", fg="white", bg="#333333", font=("Roboto", 20, "bold"), height=3,
				command=lambda:self.convert_bits(self.credits_lb))
			bank_w.add(convert_btn)

			send_btn = Button(bank_w, text="Send Credits",  fg="white", bg="#333333", font=("Roboto", 20, "bold"),
				command=lambda:self.send_credits(self.credits_lb))
			bank_w.add(send_btn)

			inventory_btn = Button(stock_w, text="Inventory", fg="white", bg="#333333", font=("Roboto", 20, "bold"), height=3,
				command=self.view_inventory)
			stock_w.add(inventory_btn)

			self.dsh_scr.after(3000, self.auto_update)

		except Exception as e:
			print(e, "is the error... 7")


	def convert_bits(self, lb):

		try:
			self.convert_scr = Tk()
			self.convert_scr.geometry("425x175")
			self.convert_scr.title("Convert Bits to Credits")
			self.convert_scr.resizable(0,0)
			self.convert_scr.config(bg="white")

			convert_lb = Label(self.convert_scr, text="Convert Bits to Credits:", fg="#333333", bg="white", font=("Roboto", 25, "bold"))
			convert_lb.pack(pady=10)

			money_amounts_default = ["5", "10", "25", "50", "100", "250", "500", "1000", "2500", "5000", "10000"]

			amount_entry = ttk.Combobox(self.convert_scr, values=money_amounts_default, justify="center")
			amount_entry.pack(pady=10)
			amount_entry.current(newindex=4)

			send_btn = Button(self.convert_scr, text="Send", bg="#333333", fg="white", font=("Roboto", 15, "bold"),
				command=lambda:self.convert_bits2(amount_entry.get(), lb))
			send_btn.pack(pady=10)
		except Exception as e:
			print(e, "is the error... 6")


	def convert_bits2(self, amount, lb):

		try:
			self.c2.execute("SELECT *, oid FROM users WHERE mobile = "+str(self.mob))
			information = self.c2.fetchall()

			self.c2.execute("SELECT *, oid FROM users WHERE mobile = 30735603")
			information2 = self.c2.fetchall()
			information2 = information2[0]

			self.information2 = information[0]

			if int(self.information2[4])+3 >= int(amount):
				
				self.c.execute("UPDATE users SET credits = :cd WHERE oid = :oid", {
					"cd":int(self.information[1]) + int(amount),
					"oid":self.information[3]
					})
				if int(self.information[0]) == 30735603:
					self.c2.execute("UPDATE users SET money_amount = :mn WHERE mobile=30735603", {
						"mn":int(self.information2[4])-int(amount)
						})
				else:	
					self.c2.execute("UPDATE users SET money_amount = :mn WHERE oid = :oid", {
						"mn":(int(self.information2[4])-int(amount))-3,
						"oid":self.information2[5]
						})
					self.c2.execute("UPDATE users SET money_amount = :mn WHERE oid = :oid", {
						"mn": int(information2[4])+3,
						"oid":information2[5]
					})
				self.db.commit()
				self.db2.commit()

				messagebox.showinfo("Transaction Successful", "Your Transaction was successful!")
				self.refresh_data(lb, self.information2, self.information)

			else:

				messagebox.showerror("Not Successful", f"Unfortunately, you do not have {amount} bits (+3 transaction fee) in your bank account. Please try a lower sum...")
		except Exception as e:
			print(e, "is the error... 5")



	def refresh_data(self, lb, bnk, stk):

		try:
			self.c.execute("SELECT *, oid FROM users WHERE mobile = "+str(self.information[0]))
			information = self.c.fetchall()

			self.information = information[0]

			self.c2.execute("SELECT *, oid FROM users WHERE mobile = "+str(self.information[0]))
			information2 = self.c2.fetchall()

			self.information2 = information2[0]

			lb.config(text=f"Credits: {self.information[1]}")
		except Exception as e:
			print(e, "is the error... 4")


	def send_credits(self, lb):

		try:
			self.send_scr = Tk()
			self.send_scr.geometry("350x300")
			self.send_scr.title("Send Credits")
			self.send_scr.resizable(0,0)
			self.send_scr.config(bg="white")

			send_lb = Label(self.send_scr, text="Send Credits", fg="#333333", bg="white", font=("Roboto", 25, "bold"))
			send_lb.pack(pady=10)

			money_amounts_default = ["5", "10", "25", "50", "100", "250", "500", "1000", "2500", "5000", "10000"]
			amount_entry = ttk.Combobox(self.send_scr, values=money_amounts_default, justify="center")
			amount_entry.pack(pady=10)
			amount_entry.current(newindex=4)

			to_lb = Label(self.send_scr, text="To", fg="#333333", bg="white", borderwidth=0, font=("Roboto", 10, "bold"))
			to_lb.pack(pady=10)

			reciever_entry = ttk.Combobox(self.send_scr, values=[self.information[0]], justify="center")
			reciever_entry.pack(pady=10)
			reciever_entry.current(newindex=0)

			send_btn = Button(self.send_scr, text="Send", bg="#333333", fg="white", font=("Roboto", 15, "bold"),
				command=lambda:self.send_credits2(amount_entry.get(), reciever_entry.get(), lb))
			send_btn.pack(pady=10)

		except Exception as e:
			print(e, "is the error... 16")


	def send_credits2(self, amount, reciever, lb):

		try:
			self.c2.execute("SELECT *, oid FROM users WHERE mobile = "+str(self.mob))
			information = self.c2.fetchall()

			self.c2.execute("SELECT *, oid FROM users")
			information2 = self.c2.fetchall()
			
			info_2 = []
			info_3 = []

			for info in information2:

				if str(info[0]) == str(30735603):
					for i in info:
						info_2.append(i)
				if reciever != "Bank Account":

					if str(info[0]) == str(reciever):
						for i in info:
							info_3.append(i)

			if len(info_3) == 0:
				messagebox.showerror("Number not found", "The number you typed was not found. Please try again.") 
				return

			self.information2 = information[0]


			if int(self.information[1])+3 > int(amount):

				self.c.execute("UPDATE users SET credits = :c WHERE oid = :oid", {
					"c":(int(self.information[1])-int(amount))-3,
					"oid":self.information[3]})
				self.c2.execute("UPDATE users SET money_amount = :mn WHERE oid = :oid", {
					"mn":int(info_3[4])+int(amount),
					"oid":info_3[5]})
				self.c2.execute("UPDATE users SET money_amount = :mn WHERE oid = :oid", {
					"mn": int(info_2[4])+3,
					"oid":info_2[5]})
				self.db.commit()
				self.db2.commit()
				
				messagebox.showinfo("Transaction Successful", "Your Transaction was successful!")
				self.refresh_data(lb, self.information, self.information2)

			else:

				messagebox.showerror("Not Successful", f"Unfortunately, you do not have {amount} bits (+3 transaction fee) in your bank account. Please try a lower sum...")

		except Exception as e:
			print(e, "is the error... 17")

	def view_inventory(self):

	
		self.inv_scr = Tk()
		self.inv_scr.title("Inventory")
		self.inv_scr.geometry("650x450")
		self.inv_scr.config(bg="white")
		self.inv_scr.resizable(0,0)

		self.inv_scr.protocol("WM_DELETE_WINDOW", lambda:self.on_scr_close(1))

		headings = Label(self.inv_scr, text="Item     Quantity     B. Price     C. Price", bg="white", fg="#333333",
			font=("Roboto", 20, "bold"))
		headings.place(x=40, y=10)

		gold_lb = Label(self.inv_scr, text="Gold", bg="white", font=("Times New Roman", 15))
		gold_lb.place(x=45, y=70)

		silver_lb = Label(self.inv_scr, text="Silver", bg="white", font=("Times New Roman", 15))
		silver_lb.place(x=41, y=130)

		bronze_lb = Label(self.inv_scr, text="Bronze", bg="white", font=("Times New Roman", 15))
		bronze_lb.place(x=41, y=190)

		iron_lb = Label(self.inv_scr, text="Iron", bg="white", font=("Times New Roman", 15))
		iron_lb.place(x=45, y=250)

		self.c.execute("SELECT * FROM stock WHERE mobile="+str(self.information[0]))
		
		information = self.c.fetchall()
		information = information[0]

		gold_qt = Label(self.inv_scr, text=f"{information[1]}", bg="white", font=("Times New Roman", 15))
		gold_qt.place(x=180, y=70)

		silver_qt = Label(self.inv_scr, text=f"{information[3]}", bg="white", font=("Times New Roman", 15))
		silver_qt.place(x=180, y=130)

		bronze_qt = Label(self.inv_scr, text=f"{information[5]}", bg="white", font=("Times New Roman", 15))
		bronze_qt.place(x=180, y=190)

		iron_qt = Label(self.inv_scr, text=f"{information[7]}", bg="white", font=("Times New Roman", 15))
		iron_qt.place(x=180, y=250)
		
		gold_b = Label(self.inv_scr, text=f"{round(information[2], 2)}", bg="white", font=("Times New Roman", 15))
		gold_b.place(x=330, y=70)

		silver_b = Label(self.inv_scr, text=f"{round(information[4], 2)}", bg="white", font=("Times New Roman", 15))
		silver_b.place(x=330, y=130)

		bronze_b = Label(self.inv_scr, text=f"{round(information[6], 2)}", bg="white", font=("Times New Roman", 15))
		bronze_b.place(x=330, y=190)

		iron_b = Label(self.inv_scr, text=f"{round(information[8], 2)}", bg="white", font=("Times New Roman", 15))
		iron_b.place(x=330, y=250)

		self.c.execute("SELECT current_value FROM stocks_name")
		information2 = self.c.fetchall()

		values_c = []

		for info in information2:
			values_c.append(info[0])

		self.gold_c = Label(self.inv_scr, text=f"{values_c[0]}", bg="white", font=("Times New Roman", 15))
		self.gold_c.place(x=450, y=70)

		self.silver_c = Label(self.inv_scr, text=f"{values_c[1]}", bg="white", font=("Times New Roman", 15))
		self.silver_c.place(x=450, y=130)

		self.bronze_c = Label(self.inv_scr, text=f"{values_c[2]}", bg="white", font=("Times New Roman", 15))
		self.bronze_c.place(x=450, y=190)

		self.iron_c = Label(self.inv_scr, text=f"{values_c[3]}", bg="white", font=("Times New Roman", 15))
		self.iron_c.place(x=450, y=250)

		g_btn = Button(self.inv_scr, text="B/S", bg="#333333", fg='white', font=("Roboto", 14, "bold"), 
				command=lambda:self.b_s_page1(information[2],"gold", information[1]))
		g_btn.place(x=580, y=70)

		s_btn = Button(self.inv_scr, text="B/S", bg="#333333", fg='white', font=("Roboto", 14, "bold"), 
				command=lambda:self.b_s_page1(information[4],"silver", information[3]))
		s_btn.place(x=580, y=130)

		b_btn = Button(self.inv_scr, text="B/S", bg="#333333", fg='white', font=("Roboto", 14, "bold"), 
				command=lambda:self.b_s_page1(information[6],"bronze", information[5]))
		b_btn.place(x=580, y=190)

		i_btn = Button(self.inv_scr, text="B/S", bg="#333333", fg='white', font=("Roboto", 14, "bold"), 
				command=lambda:self.b_s_page1(information[8], "iron", information[7]))
		i_btn.place(x=580, y=250)

		spent = (round(information[2], 2)*int(information[1]))+(round(information[4], 2)*int(information[3]))+(round(information[6], 2)*int(information[5]))+(round(information[8], 2)*int(information[7]))
		earnt = (int(values_c[0])*int(information[1]))+(int(values_c[1])*int(information[3]))+(int(values_c[2])*int(information[5]))+(int(values_c[3])*int(information[7]))

		profit_lb = Label(self.inv_scr, text=f"Net: {round(earnt-spent, 2)}", bg="white", fg="#333333", font=("Roboto", 30, "bold"))
		profit_lb.place(x=20, y=350)

		total_lb = Label(self.inv_scr, text=f"Total: {round(int(self.information[1])+earnt)}", bg="white")
		total_lb.place(x=50, y=400)



	def b_s_page1(self, b, item, qt):

		self.b_s_scr = Tk()
		self.b_s_scr.title("Buy/Sell")
		self.b_s_scr.geometry("200x75")
		self.b_s_scr.config(bg="white")
		self.b_s_scr.resizable(0,0)

		str_var = IntVar()

		self.c.execute("SELECT current_value FROM stocks_name")
		c = self.c.fetchall()
		
		num = {"gold":0, "silver":1, "bronze":2, "iron":3}

		c = c[num[item]]

		buy_rd = Radiobutton(self.b_s_scr, text="Buy", variable=str_var, bg="white", value=0, fg="#333333")
		buy_rd.place(x=20, y=10)

		sell_rd = Radiobutton(self.b_s_scr, text="Sell", variable=str_var, bg="white", value=1, fg="#333333")
		sell_rd.place(x=120, y=10)

		buy_rd.bind("<Button-1>", lambda x:self.b_s_page2(0, b, c[0], item, qt))
		sell_rd.bind("<Button-1>", lambda x:self.b_s_page2(1, b, c[0], item, qt))


	def b_s_page2(self, transaction, b, c, item, qt):
		
		if transaction == 0:

			try:
				self.frame2.destroy()
			except:
				pass

			self.b_s_scr.geometry("250x400")

			self.frame1 = Frame(self.b_s_scr, bg="white")
			self.frame1.place(x=50, y=80)

			price_lb = Label(self.frame1, text="Price:", font=("Roboto", 20), bg="white")
			price_lb.pack(pady=5)

			self.price_lb = Label(self.frame1, text=f"{c}", font=("Roboto", 20), bg="white")
			self.price_lb.pack(pady=10)


			qt_lb = Label(self.frame1, text="Quantity:", font=("Roboto", 20), bg="white")
			qt_lb.pack(pady=5)

			qt_en = Entry(self.frame1, font=("Roboto", 18), width=10, borderwidth=2, justify="center")
			qt_en.pack(pady=10)

			buy_btn = Button(self.frame1, text="Buy", fg="#333333", bg="green", font=("Roboto", 20, "bold"),
				command=lambda:self.buy_stock(item, c, qt_en.get(), b, qt))
			buy_btn.pack(pady=10)

	
			print("yes")

		elif transaction == 1:

			try:
				self.frame1.destroy()
			except:
				pass

			self.b_s_scr.geometry("250x400")

			self.frame2 = Frame(self.b_s_scr, bg="white")
			self.frame2.place(x=50, y=80)

			price_lb = Label(self.frame2, text="Price:", font=("Roboto", 20), bg="white")
			price_lb.pack(pady=5)

			self.price_lb = Label(self.frame2, text=f"{c}", font=("Roboto", 20), bg="white")
			self.price_lb.pack(pady=10)


			qt_lb = Label(self.frame2, text="Quantity:", font=("Roboto", 20), bg="white")
			qt_lb.pack(pady=5)

			qt_en = Entry(self.frame2, font=("Roboto", 18), width=10, borderwidth=2, justify="center")
			qt_en.pack(pady=10)

			sell_btn = Button(self.frame2, text="Sell", fg="#333333", bg="red", font=("Roboto", 20, "bold"),
				command=lambda:self.sell_stock(item, c, qt_en.get(), b, qt))
			sell_btn.pack(pady=10)

	
			print("yes")


		else:
			print("huh?", transaction)

	def sell_stock(self, item, current_price, quantity, buying_average, previous_qt):

		current_price = int(current_price)
		quantity = int(quantity)
		buying_average = int(buying_average)
		previous_qt = int(previous_qt)

		if quantity <= previous_qt:

			initials = {"gold":"g", "silver":"s", "bronze":"b", "iron":"i"}

			total = (buying_average*previous_qt)+(current_price*quantity)
			total = float(total/(quantity+previous_qt))


			self.c.execute(f"UPDATE stock SET {item} = :item, {initials[item]}_av = :a WHERE oid = :oid", {
							"item":previous_qt-quantity,
							"a":total,
							"oid":self.information[3]})
			print(total)
			self.c.execute(f"UPDATE users SET credits = :c WHERE oid = :oid", {
							"c":round(self.information[1]+(quantity*current_price)),
							"oid":self.information[3]})
			self.db.commit()

			self.refresh_data(self.credits_lb, None, None)

			self.b_s_scr.destroy()
			self.inv_scr.destroy()

			messagebox.showinfo("Successful", f"Your Transaction was successful! You have {previous_qt-quantity} {item} left...")


		else:
			messagebox.showerror("Unsuccessful", f"Unfortunately, you do not have enough stocks ({quantity}) to sell. You have only {previous_qt} {item}...")

	def buy_stock(self, item, current_price, quantity, buying_average, previous_qt):

		#stock(mobile, gold, g_av, silver, s_av, bronze, b_av, iron, i_av = for reference

		current_price = int(current_price)
		quantity = int(quantity)
		buying_average = int(buying_average)
		previous_qt = int(previous_qt)


		if current_price*quantity <= self.information[1]:

			initials = {"gold":"g", "silver":"s", "bronze":"b", "iron":"i"}

			total = (buying_average*previous_qt)+(current_price*quantity)
			total = float(total/(quantity+previous_qt))

			self.c.execute(f"UPDATE stock SET {item} = :item, {initials[item]}_av = :av WHERE oid = :oid", {
						"item":	int(previous_qt)+quantity,
						"av":total,
						"oid":self.information[3]})
			self.c.execute(f"UPDATE users SET credits = :c WHERE oid=:oid", {
						"c":int(self.information[1])-int(current_price*quantity),
						"oid":self.information[3]})

			messagebox.showinfo("Successful", "Your Transaction was successful!")

			self.refresh_data(self.credits_lb, None, None)

			self.b_s_scr.destroy()
			self.inv_scr.destroy()

			self.db.commit()

		else:
			messagebox.showerror("Unsuccessful", f"Unfortunately, you do not have enough money ({int(current_price)+int(quantity)}) to buy this stock...")


trigger = StockMarket()