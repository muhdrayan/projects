import random, time
MESSAGE = "hacking is succesful" 
padding_symbols = ["#", "$", "/", "@"]

def generate_key():

	list_of_nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
	
	key = ""

	while list_of_nums != []:

		r = random.choice(list_of_nums)
		list_of_nums.remove(r)
		key += r

	return key


#KEY = generate_key()
KEY = "123456789"
print(KEY, "is the key")

class Encrypt:

	def __init__(self):

		self.start_time = 0
		self.start_time += time.time_ns()
		self.times = 0

		self.encrypt(MESSAGE)


	def encrypt(self, msg):

		self.cipher_text = ""

		for i in range(1):

			if i == 0:
				self.grouped = self.classify(MESSAGE)
			else:
				self.grouped = self.classify(self.cipher_text)
				self.cipher_text = ""
			for num in KEY:
				c = self.grouped[int(num)-1]
				for letters in c:
					self.cipher_text += letters
			self.times += 1

		print(self.cipher_text)
		print((time.time_ns() - self.start_time)/1000000000, "seconds", f"for {self.times} iterations.")


	def classify(self, msg):

		c1 = []
		c2 = []
		c3 = []
		c4 = []
		c5 = []
		c6 = []
		c7 = []
		c8 = []
		c9 = []

		column = [c1, c2, c3, c4, c5, c6, c7, c8, c9]
		x = 1

		for character in msg:
			if x <= 9:
				c = column[x-1]
				c.append(character)
				x += 1
			else:
				c1.append(character)
				x = 2

		#add padding
		max_length = 0
		for lists in column:
			if len(lists) > max_length:
				max_length = len(lists)
		for lists in column:
			if len(lists) < max_length:
				lists.append(random.choice(padding_symbols))

		return column

encrypt = Encrypt()

