import random

# in the format = [name, position, overall, shooting, passing, dribbling, defending]
#Sample data - real data will be added once this thing is done =D 
players = [["Messi", "RW", 94, 95, 91, 95, 40],
		   ["Ronaldo", "ST", 92, 97, 88, 94, 55],
		   ["Neymar", "LW", 91, 93, 88, 96, 40],
		   ["Mbappe", "ST", 90, 96, 88, 96, 68],
		   ["Ter Stegen", "GK", 91, 50, 80, 60, 93]]

#Class for each player
class Players:
	def __init__(self, stats):
		
		#Assigning Attributes
		self.name = stats[0]
		self.overall = stats[2] 
		self.position = stats[1]

		print(stats)
		self.stats = {"overall":stats[2],"shoot":stats[3],"pass":stats[4],"dribble":stats[5], "defence":stats[6]}

	def print_data(self):
		#printing stats
		print(self.name, self.overall, self.position, self.stats)

	def randomised_data(self, type_):
		if type_ == "shoot":
			return random.randint(5, 50)


	def shooting_outcome(self, distance):
		#gives chance of getting shot on target
		luck = random.randint(4, 10)

		skill = (self.stats["shoot"]*0.9)/100
		distance_prob = float((90 - distance)/100)
		luck_prob = luck/10

		outcome_prob = round(((skill*6) + (distance_prob*60) + (luck_prob*2))/68, 2)
		print(f"{self.name}:{distance}m {distance_prob}, luck {luck_prob}, skill {round(skill,2)}, final {round(outcome_prob*100,2)}% ")
		
		outcome = random.choices(["On target", "Off target"], weights=[outcome_prob*100,(100-outcome_prob*100)],k=1)
		print(outcome)
		return outcome[0]

	def saving_outcome(self, distance):
		
		luck = random.randint(4, 10)

		skill = (self.stats["defence"]*0.7/100)
		distance_prob = round((distance+skill*10)/100, 2)
		luck_prob = luck/10

		outcome_prob = round((((skill*10) + (distance_prob*60) + (luck_prob*2))/72)*distance/40, 2)
		print(f"{self.name}:{distance}m {distance_prob}, luck {luck_prob}, skill {round(skill,2)}, final {round(outcome_prob*100,2)}%")	

		outcome = random.choices(["Save", "Not save"], weights=[outcome_prob*100, (100-outcome_prob*100)],k=1)
		print(outcome)

		return outcome[0] 

	def passing_outcome(self, type_):
		if type_ == "long":
			pass #will do this later -_- its too late

class Match:
	def __init__(self, team1, team2, mode1, mode2):
		
		#Defining Match Variables
		self.time = 0
		self.extra_time = 0

		self.team1 = {"GK":team1[0], "CB":team1[1], "CB2":team1[2], "LB":team1[3],
						"RB":team1[4], "CM":team1[5],"RM":team1[6],"LM":team1[7],
						"CF":team1[8], "LW":team1[9], "RW":team1[10]}
		self.team2 = {"GK":team2[0], "CB":team2[1], "CB2":team2[2], "LB":team2[3],
						"RB":team2[4], "CM":team2[5],"RM":team2[6],"LM":team2[7],
						"CenterForward":team2[8], "LeftWinger":team2[9], "RightWinger":team2[10]}
		
		self.teams = [self.team1, self.team2]

		#Either Attacking, Neutral or Defensive
		self.mode1 = mode1
		self.mode2 = mode2

		#testing area
		"""while self.time + self.extra_time != 90:
			self.generate_chance()"""
		self.classify_players()

	def classify_players(self):
		#this function is to make a class for each player
		global players

		self.class_players = {}
		plyr_n = 0
		for team in self.teams:
			for pos, player in team.items():
				#data fetching
				player_data = []
				for p in players:
					if p[0] == player:
						player_data = p
						break
				if player_data == []:
					player_data.append([player, "U", 80, 80, 80, 80, 80])
					player_data = player_data[0]
					 
				self.class_players[plyr_n] = Players(player_data)

	def generate_chance(self):
		#Generating the time after which the chance is occuring.
		remaining_time = (90+self.extra_time) - self.time
		chance_after = 0

		#Deciding after how much time the next chance will occur
		if 15 <= remaining_time: chance_after += random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],weights=[1,2,3,3,4,5,4,3,2,2,1,1,1,1,1,1],k=1)[0]
		else: chance_after += random.choices([n for n in range(remaining_time+1)],k=1)[0]

		self.time += chance_after

		#Choosing which team gets the chance
		distribution = {"Attacking":8,"Neutral":5,"Defensive":3}
		attacks = [distribution[self.mode1],distribution[self.mode2]]
		if attacks[0]+attacks[1] > 10:
			while attacks[0] + attacks[1] != 10:
				attacks[random.choice([0,1])] -= 1
		elif attacks[0] + attacks[1] < 10:
			while attacks[0] + attacks[1] == 10:
				attacks[random.choice([0,1])] += 1
		
		attacking_team = random.choices([1,2],weights=attacks,k=1)[0]
		self.generate_field_layout(attacking_team)

		print(f"chance at {self.time}' for team {attacking_team}")

	def generate_field_layout(self,attacking_team):
		#names in players list
		pass

match1 = Match(["Ter Stegen","Ruben Dias","Van Dijk","Robertson","Alexander-Arnold","De Jong","De Bruyne","Busquets","Mbappe","Messi","Neymar"],
		["Oblak","Ramos","Marquinhos","Jordi Alba","Pavard","Kante","Jorginho","Havertz","Lewandowski","Salah","Ronaldo"],
		"Neutral","Neutral")