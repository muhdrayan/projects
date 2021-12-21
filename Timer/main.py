#importing
import sqlite3, time

#database connection
db = sqlite3.connect("categories.db")
c = db.cursor()

#making table
c.execute("CREATE TABLE IF NOT EXISTS cat(name TEXT, time INTEGER, today INTEGER, date TEXT)")
db.commit()

#functions
def clean_up_data():
    c.execute("SELECT *,oid FROM cat")
    information = c.fetchall()
    for info in information:
        current_date = time.strftime("%j")
        if str(info[3]) != current_date:
            c.execute("UPDATE cat SET today=:t, date=:d WHERE oid=:oid",{"t":0,"d":time.strftime("%j"),
            "oid":info[4]})
            db.commit()
    db.commit()

def convert_time(sec):
    min_, sec = divmod(sec, 60)
    hour, min_ = divmod(min_, 60)
    list_ = [int(hour), int(min_),int(sec)]
    type_ = 0
    for timing in list_:
        if len(str(timing)) != 2:
            list_[type_] = "0"+str(timing)
        type_ += 1
    return list_ 

def start(category):
    start_time = time.time()
    input_text = input()
    if input_text == "stop": end_time = time.time()

    #calculating time
    total_time = end_time - start_time
    converted = convert_time(total_time)

    print(f"You spend {total_time} on {category} or {converted[0]}:{converted[1]}:{converted[2]}sec!")

    #getting oid
    c.execute("SELECT *, oid FROM cat")
    information = c.fetchall()
    for info in information:
        if info[0] == category:
            information = [info[1],info[2],info[4]]
            break
    clean_up_data()
    #updating the database
    c.execute(f"UPDATE cat SET time = :i, today=:t WHERE oid = :oid",{"i":int(information[0])+int(total_time),
            "t":int(information[1])+int(total_time),"oid":information[2]})
    db.commit()   


def view_data(category):
    c.execute("SELECT * FROM cat")
    information = c.fetchall()
    if category == "all":
        for cat in information:
            converted = convert_time(cat[1])
            if cat[3] != time.strftime("%j"): clean_up_data()
            converted2 = convert_time(cat[2])
            print(f"{cat[0]} has been done for {converted2[0]}:{converted2[1]}:{converted2[2]}secs today or {converted[0]}:{converted[1]}:{converted[2]}secs in total")
    else:
        for cat in information:
            if cat[0] == category:
                converted = convert_time(cat[1])
                if cat[3] != time.strftime("%j"): clean_up_data()
                converted2 = convert_time(cat[2])
                print(f"{cat[0]} has been done for {converted2[0]}:{converted2[1]}:{converted2[2]}secs today or {converted[0]}:{converted[1]}:{converted[2]}secs in total")
                return

def delete_data(category):
    c.execute("SELECT name, oid FROM cat")
    information = c.fetchall()
    for info in information:
        if info[0] == category:
            information = info[1]
 
    c.execute("DELETE FROM cat WHERE oid="+str(information))
    db.commit()

    print(f"{category} deleted!")

clean_up_data()

def help_guide():

    #helping process
    print("Oh...")
    time.sleep(1)
    print("So you are lost...")
    time.sleep(2)
    print("Don't worry- ")
    time.sleep(1)
    print("I'm here to guide you =D.")
    while True:
        input_ = input("You ready? (y/n): ")
        if input_.lower() in ["y","yes"]:
            print("Fantastic! So let us begin.")
            break
        elif input_.lower() in ["n","no"]:
            print("Aww, that's sad. Come back when you are ready!")
            return
        else:
            print("Say yes or no.")
    time.sleep(1)
    
    #making a class
    print("'new' <activity-name>")
    time.sleep(1)
    print("^ that is the command to make a new activity")
    time.sleep(1)
    print("Let's try it!")

    while True:
        time.sleep(1)
        input_ = input("Make an activity named 'football': ")
        if input_ == "new football":
            print("Congrats! You're becoming a pro!")
            break
        elif input_ == "answer":
            print("new football")
            time.sleep(1)
            print("I thought I made it easy... Try again")
        else:
            print("Sad, it's wrong... Try again (if you don't know how to, type 'answer' to get the answer)")

    time.sleep(1)

    #deleting a class
    print("Suppose you don't want a class you made.")
    time.sleep(1)
    print("What do you do now?")
    time.sleep(1)
    print("'delete' <activity-name>")
    time.sleep(2)
    print("As simple as that. Try it!")

    while True:
        time.sleep(1)
        input_ = input("Delete an activity named 'fly': ")
        if input_ == "delete fly":
            print("Woah, I think you are getting the hang of it!")
            break
        elif input_ == "answer":
            print("delete fly")
            time.sleep(1)
            print("Use your brain next time...")
        else:
            print("Aww, try again. Better luck next time!")
    
    #starting an activity
    time.sleep(2)
    print("Now that you've mastered the basics on how to create a class and delete it, let's actually get to using it...")
    time.sleep(1)
    print("To start the timer, we have to:-")
    time.sleep(2)
    print("'start' <activity-name>")
    time.sleep(1)
    print("Got it?")
    
    while True:
        time.sleep(1)
        input_ = input("Start the class 'math': ")
        if input_ == "start math":
            print("Woohoo! Well done.")
            break 
        elif input_ == "answer":
            print("start math")
            time.sleep(1)
            print("You should be knowing this after all this time... Anyways, try again!")
        else:
            print("Sorry to say, you are wrong. But try again! (type answer if you don't know the answer)")
    
    time.sleep(1)
    #stopping class
    print("You know how to start a class, but how to stop it?")
    time.sleep(2)
    print("After starting a class, you have to wait until your activity is done. Once it is completed, just type 'stop'")
    time.sleep(3)
    print("Now that can't be hard can it?")

    while True:
        time.sleep(1)
        input_ = input("Start and then stop an activity named 'science': ")
        if input_ == "start science":
            input_2 = input()
            if input_2 == "stop":
                print("Bravo, you are smarter than I thought...")
                break
            else:
                print("Oh oh, you were supposed to say 'stop'...")
                time.sleep(1)
                print("Try again from the start.")
        else:
            print("We just did this last exercise -_- How do you not remember!?")
    time.sleep(3)
    
    #viewing data
    print("You are almost there! Just one more command and you are done!")
    time.sleep(2)
    print("Last but not the least, we need to see how much time we've spent on an activity.")
    time.sleep(1)
    print("To do this, we have the command:")
    time.sleep(1)
    print("'view'")
    time.sleep(1)
    print("^ that command will show you how much time you've spent on everything...")
    time.sleep(2)
    print("If you want to do this for only a particular activity, just specify the name of the activity like: 'view' football")
    time.sleep(1)
    
    print("And I forgot, just type 'exit' when you want to close the program.")
    time.sleep(3)

    print("That's it! You've now earnt a Ph.D in this program! (I don't feel like I want to test you again, you must be smart enough I hope.)")
    time.sleep(1)
    print("If you have any problems, email 08202@bpsdoha.edu.qa or drop me a message on zoom ;) Bye!")
    return

def add_sec(cat, t):
    c.execute("SELECT name,time,today,oid FROM cat")
    information = c.fetchall()

    for info in information:
        if info[0] == cat:
            c.execute("UPDATE cat SET time=:t, today=:t2 WHERE oid=:oid", {"t":info[1]+int(t),"t2":info[2]+int(t),"oid":info[3]})
            db.commit()
            print("Updated!")
            return
while True:
    #getting command
    input_text = input("Please enter a command: ")
    input_text = input_text.split(" ")

    if input_text[0] == "new": #if user wants new timer
        c.execute("INSERT INTO cat VALUES(?,?,?,?)",(input_text[1],0,0,time.strftime("%j")))
        db.commit()
        print("Done!")
    elif input_text[0] == "start": #if user wants to start timer for category
        start(input_text[1])
    elif input_text[0] == "view":
        try:
            view_data(input_text[1])
        except IndexError:
            view_data("all")

    elif input_text[0] == "delete":
        delete_data(input_text[1])

    elif input_text[0] == "exit":
        exit()
    elif input_text[0] == "help":
        help_guide()
    elif input_text[0] == "add":
        add_sec(input_text[1],input_text[2])
    else:
        print("Invalid command.")
