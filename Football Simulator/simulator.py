import random

#Sample data - real data will be added once this thing is done =D 
players = [["Messi", "CAM", 94, 95, 91, 95, 40],
		   ["Ronaldo", "ST", 92, 97, 88, 94, 55],
		   ["Neymar", "LWF", 91, 93, 88, 96, 40],
		   ["Mbappe", "ST", 90, 96, 88, 96, 68]]

players_class = [] 

#Class for each player
class Players:
	def __init__(self, name, ovr, position, shoot, pass_, dribble, defence):
		#Assigning Attributes
		self.name = name
		self.overall = ovr 
		self.position = position
		self.stats = {"overall":ovr,"shoot":shoot,"pass":pass_,"dribble":dribble, "defense":defence}

	def print_data(self):
		#printing stats
		print(self.name, self.overall, self.position, self.stats)

	def shooting_outcome(self):
		#gives chance of getting shot on target
		distance = random.randint(5, 50)
		luck = random.randint(4, 10)

		skill = (self.stats["shoot"]*0.9)/100
		distance_prob = float((90 - distance)/100)
		luck_prob = luck/10

		outcome_prob = round(((skill*6) + (distance_prob*60) + (luck_prob*2))/68, 2)
		print(f"{self.name}:{distance}m {distance_prob}, luck {luck_prob}, skill {round(skill,2)}, final {round(outcome_prob*100,2)}% ")
		
		outcome = random.choices(["On target", "Off target"], weights=[outcome_prob*100,(100-outcome_prob*100)],k=1)
		print(outcome)
		return outcome
	

#Making classes for all players
for player in players:
	players_class.append(Players(player[0],player[2],player[1],player[3],player[4],player[5],player[6]))

for _ in range(10):
	for c in players_class:
		c.shooting_outcome()

