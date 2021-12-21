import sqlite3, time

print('Welcome to the reward system. Please authorize yourself to continue.')
time.sleep(1)

guess = input('Type the auth key: ')

if guess == "Rayan123":
    print('Correct Password!')
else:
    exit()

time.sleep(1)

database = sqlite3.connect('bank.db')
cursor = database.cursor()

cursor.execute("SELECT *,oid FROM users")
information = cursor.fetchall()

found = False
mob_n =  input('Enter your mobile number: ')
for info in information:
    if str(info[0]) == mob_n:
        information = info        
        found = True

if not found:
    print('You might have typed the wrong mobile number...')
    time.sleep(2)
    exit()

def calculate_reward(times):

    reward_sec = 250/3600
    total_reward = int(int(times) * reward_sec)
    print(f"You will get {total_reward} bits for studying.")
    print(f"You had {int(information[4])} in the bank...")

    cursor.execute("UPDATE users SET money_amount=:mn WHERE oid=:oid", {"mn":int(information[4])+int(total_reward), "oid":information[5]})
    database.commit()

    print(information[5])

    time.sleep(2)
    print(f"Money Added! Now you have {int(information[4])+int(total_reward)} bits in your account!")
    
    time.sleep(4)
    exit()

confirm = input(f'Is {information[2]} your name? (y/n): ')
if confirm == "y":
    print("Great! Let's continue!")
else:
    print("Sad, please try again!")
    exit()

time.sleep(1)
timing = input('How much time did you study for? (in seconds format): ')

try:
    timing = int(timing)
    calculate_reward(timing)

except ValueError:
    print('You did not give a number')
    time.sleep(1)
    exit()






