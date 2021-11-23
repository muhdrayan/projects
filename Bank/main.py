from tkinter import *
from database import Database
from tkinter import messagebox
from tkinter import ttk

hidden_n = ["Bank", "Mutual Funds"]

class BankStartUp:

	def __init__(self, stk):
		
		if not stk:
			self.scr = Tk()
			self.scr.title("Rayan National Bank")
			self.scr.geometry("500x350")
			self.scr.resizable(0,0)
			self.scr.config(bg="white")
			self.cdx = 57680/56

			self.home_screen_widgets()

			self.database = Database()

			self.scr.mainloop()

	def home_screen_widgets(self):
		
		bank_title = Label(self.scr, text="Rayan National Bank", bg="white", fg="#333333", font=("Roboto", 20, "bold"))
		bank_title.pack(pady=30)

		country_button = Button(self.scr, text="Country Amount", font=("Roboto", 15, "bold"), fg="white", bg="#333333",
			borderwidth=0, command=self.see_country_rankings)
		country_button.pack(pady=10)

		account_login = Button(self.scr, text="Login Account", fg="white", bg="#333333", font=("Roboto", 15, "bold"), 
			borderwidth=0, command=self.login_account)
		account_login.pack(pady=10)

		register_account = Button(self.scr, text="Register Account", fg="white", bg="#333333", font=("Roboto", 15, "bold"), 
			borderwidth=0, command=self.register_account)
		register_account.pack(pady=10)

		admin_dash = Label(self.scr, text="Admin Dash", fg="grey", bg="white", font=("Roboto", 7))
		admin_dash.place(x=220, y=325)
		admin_dash.bind("<Button-3>", self.admin_dash)

	def admin_dash(self, e):
		
		self.admin_dash_ver_scr = Tk()
		self.admin_dash_ver_scr.geometry("300x300")

		entry_bx = Entry(self.admin_dash_ver_scr, borderwidth=1, font=("Roboto", 15, "bold"))
		entry_bx.pack(pady=10)

		verify_bt = Button(self.admin_dash_ver_scr, borderwidth=0, bg="#333333", fg="white", font=("Roboto", 15, "bold"),
			command=lambda:self.verify_admin(entry_bx.get()))
	
	def verify_admin(self, entry):

		if entry == str(self.cdx):
			self.verified_admin()
		else:
			messagebox.showinfo("Incorrect", "Password is incorrect v_v")

	def verified_admin(self):
		pass

	def see_country_rankings(self):
		
		self.c_r_screen = Toplevel(self.scr)
		self.c_r_screen.title("Country Overview")
		self.c_r_screen.config(bg="white")
		self.c_r_screen.geometry("600x500")
		self.c_r_screen.resizable(0,0)

		amount_title = Label(self.c_r_screen, text="Amount", fg="#333333", bg="white", font=("Roboto", 25, "bold"),
			borderwidth=0)
		amount_title.pack(pady=30)

		people = self.database.get_country_list()
		number = 0

		self.database.c.execute("SELECT * FROM d")
		status = self.database.c.fetchall()
		dis_nums = []
		for person in people:
			for st in status:
				if person[0] in st:
					dis_nums.append(person[0])
		print(dis_nums)


		for person in people:

			if person[0] in hidden_n:
				pass 
			elif person[0] in dis_nums:
				number += 1
				lb = Label(self.c_r_screen, text=f"{number}. {person[0]} - {person[1]} bits", bg="white", fg="grey",
					borderwidth=2, font=("Roboto", 15, "bold"))
				lb.pack(pady=12)
			else:				
				number += 1
				lb = Label(self.c_r_screen, text=f"{number}. {person[0]} - {person[1]} bits", bg="white", fg="#333333",
					borderwidth=2, font=("Roboto", 15, "bold"))
				lb.pack(pady=12)


	def login_account(self):
		
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

	def x(self, a, b, n=2, c=None, d=None, e=None , f=None):

		if n == 1:
			result = self.database.verify_pin1(a, b)

			self.mob = a
			if result == "Correct":
				self.login2()
		elif n == 2:
			result = self.database.verify_pin2(self.mob, b)

			if result == "Correct":

				self.dashboard()
		elif n == 3:
			
			result = self.database.send_money(a, b, c)
			if result == "Update":
				self.refresh_data()
				result2 = self.database.update(d, e, f)
				if result2 == "Updated":
					
					print("yes")
					messagebox.showinfo("Successful", "The transaction was successful!")

		elif n == 4:

			result = self.database.send_money_to_main(self.information2, self.information, a)
			if result == "Update":
				self.refresh_data()
				result2 = self.database.update2(b, c, d, self.information, self.information2)

				if result2 == "Updated":
					
					
					messagebox.showinfo("Successful", "The transaction was successful!")

	def dashboard(self):
		
		self.login_scr.destroy()

		self.dashboard_scr = Tk()
		self.dashboard_scr.title("Dashboard")
		self.dashboard_scr.geometry("500x325")
		self.dashboard_scr.resizable(0,0)
		self.dashboard_scr.config(bg="white")

		try:
			self.scr.destroy()
		except:
			pass

		self.database.c.execute(f"SELECT *, oid FROM users WHERE mobile={str(self.mob)}")
		information = self.database.c.fetchall()
		self.information = information[0]

		self.database.c.execute(f"SELECT *, oid FROM savings WHERE num={str(self.mob)}")
		information2 = self.database.c.fetchall()

		print(information2)
		
		self.information2 = information2[0]

		self.amount_title_d = Label(self.dashboard_scr, text=f"Amount: {self.information[4]} bits", bg="white", fg="#333333",
			font=("Roboto", 25, "bold"), borderwidth=0)
		self.amount_title_d.pack(pady=20)

		mobile_lb = Label(self.dashboard_scr, text=f"Mobile Number: {self.mob}", bg="white", borderwidth=0)
		mobile_lb.pack(pady=10)

		self.spendings_btn = Button(self.dashboard_scr, text=f"Account ({self.information[4]} bits)", bg="#333333", fg="white",
			borderwidth=0, font=("Roboto", 20, "bold"), command=self.main_account)
		self.spendings_btn.pack(pady=15)

		self.savings_btn = Button(self.dashboard_scr, text=f"Savings ({self.information2[1]} bits)", bg="#333333", fg="white",
			borderwidth=0, font=("Roboto", 20, "bold"), command=self.savings)
		self.savings_btn.pack(pady=15)

	def login2(self):
		
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


	def register_account(self):
		
		self.register_scr = Tk()
		self.register_scr.title("Register Account")
		self.register_scr.geometry("450x350")
		self.register_scr.resizable(0,0)
		self.register_scr.config(bg="white")

		self.verification_frame = Frame(self.register_scr, bg="white")
		self.verification_frame.pack()

		register_title = Label(self.verification_frame, text="Register Account", bg="white", fg="#333333", borderwidth=0,
		 font=("Roboto", 25, "bold"))
		register_title.pack(pady=10)

		warning = "Warning: Authorized personell only are allowed to register\nnew clients to QNB. Thank You for your coorperation."

		warning_lb = Label(self.verification_frame, text=warning, font=("Roboto", 10), fg="red", bg="white")
		warning_lb.pack(pady=10)

		auth_pass_lb = Label(self.verification_frame, text="Auth Pin", fg="#333333", bg="white", borderwidth=0,
			font=("Roboto", 20, "bold"))
		auth_pass_lb.pack(pady=10)

		auth_pass_entry = Entry(self.verification_frame, fg="#333333", bg="white", font=("Roboto", 25, "bold"), borderwidth=1,
			width=7, justify="center")
		auth_pass_entry.pack(pady=10)

		continue_btn = Button(self.verification_frame, text="Continue", bg="#333333", fg="white", borderwidth=0,
		 font=("Roboto", 15, "bold"), command=lambda:self.register_account_auth(auth_pass_entry.get()))
		continue_btn.pack(pady=15)

		auth_pass_entry.bind("<Return>", lambda x:self.register_account_auth(auth_pass_entry.get()))

	def register_account_auth(self, attempt, e=None):

		if attempt == str(int(self.cdx)):
			self.register_portal()
		else:
			messagebox.showerror("Incorrect", "The PINCODE you inserted was incorrect. Please try again.")

	def register_portal(self):
		
		self.verification_frame.destroy()

		self.r_p_frame = Frame(self.register_scr, bg="white")
		self.r_p_frame.pack()

		mobile_num_lb = Label(self.r_p_frame, text="Mobile Number:", fg="#333333", bg="white", font=("Roboto", 15, "bold"))
		mobile_num_lb.pack(pady=5)

		mobile_num_entry = Entry(self.r_p_frame, borderwidth=1, fg="#333333", bg="white", font=("Roboto", 12),
			justify="center")
		mobile_num_entry.pack(pady=5)

		name_lb = Label(self.r_p_frame, text="Name:", fg="#333333", bg="white", font=("Roboto", 15, "bold"))
		name_lb.pack(pady=5)

		name_entry = Entry(self.r_p_frame,  borderwidth=1, fg="#333333", bg="white", font=("Roboto", 12),
			justify="center")
		name_entry.pack(pady=5)

		pincode1_lb = Label(self.r_p_frame, text="Pincode", fg="#333333", bg="white", font=("Roboto", 15, "bold"))
		pincode1_lb.pack(pady=5)

		pincode1_entry = Entry(self.r_p_frame,  borderwidth=1, fg="#333333", bg="white", font=("Roboto", 12),
			justify="center")
		pincode1_entry.pack(pady=5)

		pincode2_lb = Label(self.r_p_frame, text="Pincode 2", fg="#333333", bg="white", font=("Roboto", 15, "bold"))
		pincode2_lb.pack(pady=5)

		pincode2_entry = Entry(self.r_p_frame,  borderwidth=1, fg="#333333", bg="white", font=("Roboto", 12),
			justify="center")
		pincode2_entry.pack(pady=5)

		register_btn = Button(self.r_p_frame, text="Register", bg="#333333", fg="white", borderwidth=0,
			font=("Roboto", 15, "bold"), command=lambda:self.database.check_registration_data(mobile_num_entry.get(),
			name_entry.get(), pincode1_entry.get(), pincode2_entry.get(), self.register_scr))
		register_btn.pack(pady=10)

	def main_account(self):
		
		self.main_account_scr = Tk()
		self.main_account_scr.title("Account")
		self.main_account_scr.geometry("450x300")
		self.main_account_scr.resizable(0,0)
		self.main_account_scr.config(bg="white")

		amount_title = Label(self.main_account_scr, text=f"Amount: {self.information[4]} bits", bg="white", fg="#333333",
			font=("Roboto", 25, "bold"), borderwidth=0)
		amount_title.pack(pady=20)

		transactions_lb = Label(self.main_account_scr, text="Send:", fg="#333333", bg="white", borderwidth=0,
		    font=("Roboto", 15, "bold"))
		transactions_lb.pack(pady=10)

		money_amounts_default = ["5", "10", "25", "50", "100", "250", "500", "1000", "2500", "5000", "10000"]
		amount_entry = ttk.Combobox(self.main_account_scr, values=money_amounts_default, justify="center")
		amount_entry.pack(pady=10)

		to_lb = Label(self.main_account_scr, text="To", fg="#333333", bg="white", borderwidth=0,
		    font=("Roboto", 10, "bold"))
		to_lb.pack(pady=10)

		reciever_entry = ttk.Combobox(self.main_account_scr, values=["Savings"], justify="center")
		reciever_entry.pack(pady=10)

		amount_entry.current(newindex=4)
		reciever_entry.current(newindex=0)

		send_btn = Button(self.main_account_scr, text="Send", bg="#333333", fg="white", borderwidth=0, 
			font=("Roboto", 15, "bold"), command=lambda:self.x(reciever_entry.get(), amount_entry.get(), 3,
			self.information, [amount_title, self.amount_title_d], self.spendings_btn, self.savings_btn))
		send_btn.pack(pady=10)

	def savings(self):
		
		self.savings_scr = Tk()
		self.savings_scr.title("Savings Account")
		self.savings_scr.geometry("450x350")
		self.savings_scr.resizable(0,0)
		self.savings_scr.config(bg="white")

		amount_title = Label(self.savings_scr, text=f"Amount: {self.information2[1]} bits", bg="white", fg="#333333",
			font=("Roboto", 25, "bold"), borderwidth=0)
		amount_title.pack(pady=20)

		transfer_lb = Label(self.savings_scr, text="Transfer:", bg="white", fg="#333333", font=("Roboto", 20, "bold"),
			borderwidth=0)
		transfer_lb.pack(pady=10)

		money_amounts_default = ["5", "10", "25", "50", "100", "250", "500", "1000", "2500", "5000", "10000"]
		amount_entry = ttk.Combobox(self.savings_scr, values=money_amounts_default, justify="center")
		amount_entry.pack(pady=10)
		amount_entry.current(newindex=4)

		to_lb = Label(self.savings_scr, text="To Main Account", fg="#333333", bg="white", borderwidth=0,
		    font=("Roboto", 10, "bold"))
		to_lb.pack(pady=10)

		send_btn = Button(self.savings_scr, text="Send", bg="#333333", fg="white", borderwidth=0, 
			font=("Roboto", 15, "bold"), command=lambda:self.x(amount_entry.get(), [amount_title, self.amount_title_d],
			4, self.spendings_btn, self.savings_btn))
		send_btn.pack(pady=10)

	def refresh_data(self):

		self.database.c.execute("SELECT *, oid FROM users WHERE mobile="+str(self.mob))
		information = self.database.c.fetchall()
		self.information = information[0]

		self.database.c.execute("SELECT *, oid FROM savings WHERE num="+str(self.mob))
		information2 = self.database.c.fetchall()
		self.information2 = information2[0]


trigger = BankStartUp(False)