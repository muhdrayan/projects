from tkinter import *
import random, requests

#getting some words as place holder for player names
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()

#some variables
positions = ['GK', 'LB', 'CB1', 'CB2', 'RB', 'LM', 'CM', 'RM', 'LWF', 'CF', 'RWF']
playing_styles = ['Offensive','Neutral', 'Defensive']

#only for testing purposes
def player_rand():
	p_stats = [random.choice(WORDS), random.randint(20, 35), 0, random.randint(60, 94), random.randint(60, 94), random.randint(60, 94), random.randint(60, 94), random.choice(positions)]
	ovr = p_stats[3] + p_stats[4] +p_stats[5] + p_stats[6] + 100
	ovr /= 5
	p_stats[2] = ovr

	#convert to dictionary and return it
	return {'name':p_stats[0], 'age':p_stats[1], 'position':p_stats[7], 'stats':{'overall':p_stats[2], 'shooting':p_stats[3], 'passing':p_stats[4], 'defending':p_stats[5], 'speed':p_stats[6]}}

#making a sample team
"""player = {'name':x, 'age':x, 'pos':x,'stats':{'overall':x, 'shooting':x, 'passing':x, 'defending':x, 'speed':x}}"""

team1 = {'players':{}, 'style':random.choice(playing_styles)}
team2 = {'players':{}, 'style':random.choice(playing_styles)}

for pos in positions:
	pl1 = player_rand()
	team1['players'][pos] = pl1
	pl2 = player_rand()
	team2['players'][pos] = pl2

print(team1)

#editing the Canvas class
def _create_circle(self, x, y, r, fill,**kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, fill=fill, **kwargs)
Canvas.create_circle = _create_circle

class Match:
	def __init__(self, team1, team2, width, length):
		#The teams
		self.team1 = team1
		self.team2 = team2

		#Match variables
		self.time = 0
		self.score = [0, 0]

		#Pitch size
		self.pitch_dimensions = (width, length) #width = x, length = y

		#testing area
		self.gridding()

	def gridding(self):
		#Grid screen
		self.grid_scr = Tk()
		self.grid_scr.title('Pitch')
		self.grid_scr.resizable(0,0)

		

		self.grid = []
		for i in range(self.pitch_dimensions[1]):
			self.grid.append([])

		for i in range(self.pitch_dimensions[1]):
			for _ in range(self.pitch_dimensions[0]):
				self.grid[i].append('.')
		
		self.plot_grid()
		for i in range(22):
			self.spawn_player()

		self.grid_scr.mainloop()

	def plot_grid(self, spawned=False):

		if spawned:
			self.pitch_grid.destroy()	

		gui_multiplier = 4 #For seeing the pitch clearly

		self.pitch_grid=Canvas(self.grid_scr, width=(self.pitch_dimensions[0])*(gui_multiplier+3), background="white",
			height=(self.pitch_dimensions[1])*(gui_multiplier+1))
			 
		self.pitch_grid.pack(expand=True)

		#plotting/printing
		len_num = 0
		for li in self.grid:
			width_num = 0
			for char in li:
				if char == ".":
					self.pitch_grid.create_line(width_num, len_num, width_num+1, len_num+1, fill="black")
				elif char == " ":
					self.pitch_grid.create_circle(width_num,len_num,2,fill="red")

				width_num += gui_multiplier + 3
				
			len_num += gui_multiplier + 1
	
	def generate_chance(self):	
		pass

	def spawn_player(self, minimum=[0,0], maximum=None):

		if maximum == None: maximum = [self.pitch_dimensions[0],self.pitch_dimensions[1]]

		#testing
		x_loc = random.randint(minimum[0], maximum[0]-1)
		y_loc = random.randint(minimum[1], maximum[1]-1)

		self.grid[y_loc][x_loc] = " "

		self.plot_grid(spawned=True)


football = Match(team1,team2,60,120)

		

