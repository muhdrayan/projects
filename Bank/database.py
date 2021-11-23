import sqlite3
from tkinter import messagebox

def element_stuff(elem):
	return elem[1]

class Database:
	def __init__(self):

		self.create_database()

	def create_database(self):

		self.db = sqlite3.connect("bank.db")
		self.c = self.db.cursor()

		self.c.execute("CREATE TABLE IF NOT EXISTS users(mobile INTEGER, pincode TEXT, name TEXT, pincode_2 TEXT, money_amount TEXT)")
		self.db.commit()

		self.c.execute("CREATE TABLE IF NOT EXISTS savings(num TEXT, money_amount INTEGER)")
		self.db.commit()

		self.c.execute("CREATE TABLE IF NOT EXISTS d(num TEXT)")
		self.db.commit()

	def get_country_list(self):

		self.c.execute("SELECT * FROM users")
		information = self.c.fetchall()

		people = []

		for info in information:

			tuple_ = (info[2], int(info[4]))
			people.append(tuple_)

		people.sort(key=element_stuff, reverse=True)

		return people

	def check_registration_data(self, mob_n, name, pin, pin2, scr):
		
		type_ = 0
		self.c.execute("SELECT * FROM users")
		information = self.c.fetchall()

		mobile_numbers = []
		for info in information:
			mobile_numbers.append(info[0])

		mob_n2 = 0

		try:
			mob_n2 += int(mob_n)
			
		except:
			type_ += 1


		if len(mob_n) != 8 or type_ == 1:
			messagebox.showerror("Incorrect", "The Mobile Number should be 8 numbers.")
		
		elif len(pin) != 4 or len(pin2) != 4:
			messagebox.showerror("Incorrect", "The pincodes should be 4 characters long.")

		elif int(mob_n) in mobile_numbers:
			messagebox.showerror("Already Taken", "The phone number you gave is already taken. Please try again.")

		else:
			self.register(mob_n, name, pin, pin2, scr)

	def register(self, mob_n, name, pin, pin2, scr):
		
		self.c.execute("INSERT INTO users values(?,?,?,?,?)",(mob_n, pin, name, pin2, 0))
		self.db.commit()

		self.c.execute("INSERT INTO savings values(?,?)", (mob_n, 0))
		self.db.commit()

		messagebox.showinfo("Successful", "The Registration was successful.")

		scr.destroy()

	def verify_pin1(self, mob, pin):

		self.c.execute("SELECT * FROM users")
		information = self.c.fetchall()

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
		
	def verify_pin2(self, mob, pin2):

		mob = int(mob)

		self.c.execute("SELECT * FROM users")
		information = self.c.fetchall()

		pincode = []

		for info in information:
			if info[0] == mob:
				pincode.append(info[3])

		if pin2 == pincode[0]:
			return "Correct"
		else:
			messagebox.showerror("Incorrect", "Pincode is incorrect, please try again.")

	def send_money(self, mobile, amount, client):
		
		self.mobile = client[0]

		if int(amount) < 1 and client[2] != "Bank":
			return
		

		if mobile != "Savings" and int(amount) <= int(client[4]):
			
			self.c.execute("SELECT *, oid FROM users")
			information = self.c.fetchall()


			for info in information:
				if info[0] == int(mobile):
					self.c.execute("""UPDATE users SET
									money_amount = :mn
									WHERE oid=:oid""", {
									"mn":int(info[4]) + int(amount),
									"oid":info[5]})
					self.db.commit()

					self.c.execute("""UPDATE users SET
									money_amount = :mn
									WHERE oid=:oid""", {
									"mn":(int(client[4]) - int(amount)) - 1,
									"oid":client[5]})
					self.db.commit()

					return "Update"

		elif mobile == "Savings" and int(amount) < int(client[4]):

			self.c.execute("SELECT *, oid FROM savings WHERE num="+str(client[0]))
			information = self.c.fetchall()
			information = information[0]
			
			self.c.execute("SELECT *, oid FROM users")
			information3 = self.c.fetchall()
			
			self.c.execute("""UPDATE savings SET
							money_amount = :mn
							WHERE oid = :oid""", {
							"mn": int(information[1]) + int(amount),
							"oid": information[2]
							})
			self.db.commit()

			client_amount = (int(client[4]) - int(amount)) - 1

			self.c.execute("""UPDATE users SET
							money_amount = :mn
							WHERE oid=:oid""", {
							"mn":client_amount,
							"oid": client[5]})
			self.db.commit()

			return "Update"
		else:
			messagebox.showerror("Not Enough Money", f"Unfortunately, you do not have {int(amount)+1} bits (+! transaction fees)in your main bank account.")

	def update(self, labels, main_btn, savings_btn):
		
		self.c.execute("SELECT money_amount FROM users WHERE mobile="+str(self.mobile))
		information = self.c.fetchall()
		information = information[0]

		self.c.execute("SELECT * FROM savings WHERE num="+str(self.mobile))
		information2 = self.c.fetchall()
		information2 = information2[0]

		for label in labels:
			label.config(text=f"Amount: {information[0]} bits")

		main_btn.config(text=f"Account ({information[0]} bits)")
		savings_btn.config(text=f"Savings ({information2[1]} bits)")

		return "Updated"

	def send_money_to_main(self, svngs, client, amount):
		
		status = self.c.execute("SELECT * FROM d")
		mode = []
		for st in status:
			if client[0] in st:
				mode.append("d")

		if "d" in mode:
			messagebox.showerror("Unable.", "Unable to process")
		else:
			if int(amount) < svngs[1]:
				self.c.execute("""UPDATE users SET
								money_amount = :mn
								WHERE oid=:oid""",{
								"mn":int(client[4])+int(amount),
								"oid":client[5]})
				self.db.commit()

				self.c.execute("""UPDATE savings SET
								money_amount = :mn
								WHERE oid=:oid""",{
								"mn":(int(svngs[1]) - int(amount)) - 1,
								"oid":svngs[2]
								})
				self.db.commit()

				return "Update"
			else:
				messagebox.showerror("Inadequate Funds", f"Unfortunately, you do not have {int(amount)+1} bits (+1 transaction fees), so please try again.")


	def update2(self, lbls, spendings, savings, client, svngs):

		lbls[0].config(text=f"Amount: {svngs[1]} bits")
		lbls[1].config(text=f"Amount: {client[4]} bits")

		spendings.config(text=f"Account ({client[4]} bits)")
		savings.config(text=f"Savings ({svngs[1]} bits)")

		return "Updated"

	def ex(self):

		if amount < 1 and client[2] != "Bank":
			return