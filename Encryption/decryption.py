import textwrap

CIPHER = "hsua lcs#ku@ic@nc/ge/ s/if#"
KEY = "123456789"
iterations = 1
padding_symbols = ["#", "$", "/", "@"]

class Decryption:

	def __init__(self):

		self.group(CIPHER)


	def group(self, ciph):
		
		c1 = []
		c2 = []
		c3 = []
		c4 = []
		c5 = []
		c6 = []
		c7 = []
		c8 = []
		c9 = []

		self.column = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

		self.rows = len(ciph)/len(KEY)

		pieces = textwrap.wrap(ciph, int(self.rows), replace_whitespace=False)


		for piece in pieces:
			
			index = pieces.index(piece)
			c = self.column[index]
			for char in piece:
				c.append(char)

		self.decrypt()

	def decrypt(self):

		index_no = 0
		self.ordered = [[], [], [], [], [], [], [], [], []]

		for num in KEY:
			
			index_no += 1
			self.ordered[int(num)-1] = self.column[index_no-1]

		self.deciphered()

	def deciphered(self):


		self.message = ""

		for i in range(int(self.rows)-1):
			for group in self.ordered:

				if group[i] not in padding_symbols:
					self.message += group[i]

		
		print(self.message)



dec = Decryption()



