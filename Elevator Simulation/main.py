from tkinter import *
import random, ctypes

additional_passengers = [0, 1, 2, 3]
generation_turn = 20

# Elevator stats

current_elevator_level = 0
current_passengers = []
current_population = 0
current_direction = "up"
max_capacity = 30


def make_passengers():

    direction = []
    destination = []
    current_floor = []
    passenger_data = []

    for floor in range(4):

        number_of = random.choice(additional_passengers)

        for passenger in range(number_of):
            current_floor.append(floor)
            if floor > 0 and floor < 3:
                choice = random.choice(["up", "down"])
                direction.append(choice)
                possible_dest = [0, 1, 2, 3]
                for dest in [0,1,2,3]:
                    if choice == "up" and dest > floor:
                        pass
                    elif choice == "down" and dest < floor:
                        pass
                    else:
                        possible_dest.remove(dest)
                destination.append(random.choice(possible_dest))
            elif floor == 0:
                direction.append("up")
                possible_dest = [1, 2, 3]
                destination.append(random.choice(possible_dest))
            else:
                direction.append("down")
                possible_dest = [0, 1, 2]
                destination.append(random.choice(possible_dest))

    total_no = 0
    for _ in direction:
        total_no += 1

    for passenger in range(len(direction)):
        passenger_data.append((current_floor[passenger], direction[passenger], destination[passenger]))

    return passenger_data, total_no

floor0 = []
floor1 = []
floor2 = []
floor3 = []

def organize_floors(passengers_data):

    new_people_list = {0:0, 1:0, 2:0, 3:0}

    lists = [floor0, floor1, floor2, floor3]
    for data in passengers_data:
        if data[0] in [0, 1, 2, 3]:
            floor = lists[data[0]]
            floor.append((data[1], data[2]))
            new_people_list[data[0]] = new_people_list[data[0]]+1

    return new_people_list




"""for _ in range(10):
    current_elevator_level, current_direction, current_population = move_elevator(current_elevator_level, current_direction, current_population)
    print("elevator is at floor", current_elevator_level)"""


class GUI:

    def __init__(self, lvl, direct, pop, max_):

        self.turn = 0
        self.log_scr_on = False

        self.current_elevator_level = lvl
        self.current_direction = direct
        self.current_population = pop
        self.max_capacity = max_

        self.scr = Tk()
        self.scr.geometry("700x600")
        self.scr.title("Elevator Simulator")
        self.scr.resizable(0, 0)

        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.scr.config(bg="white")
        self.make_screen()

        self.scr.mainloop()

    def move_elevator(self, level, direction, population):

        current_floor = level

        if current_floor == 3 and direction == "up":
            direction = "down"
        elif current_floor == 0 and direction == "down":
            direction = "up"

        movement_values = {"up": 1, "down": -1}
        lists = [floor0, floor1, floor2, floor3]

        for passenger in current_passengers:
            if passenger[1] == current_floor:
                current_passengers.remove(passenger)
                print(passenger, "exited")
                self.log_data_to_console("1 person just exited to this floor. \n")
                population -= 1

        for passenger in lists[current_floor]:
            p_dir = passenger[0]
            if p_dir == direction and population != max_capacity:
                current_passengers.append(passenger)
                population += 1
                print(passenger, "got in.")
                self.log_data_to_console("1 person just got inside the elevator in this floor \n")
                lists[current_floor].remove(passenger)

        current_floor += movement_values[direction]
        return current_floor, direction, population

    def log_closed(self):

        self.log_scr_on = False
        self.log_scr.destroy()

    def make_screen(self):

        simulate_button = Button(self.scr, text="➜", bg="#333333", fg="white", font=("Roboto", 20, "bold"), height=1,
                                 width=6, command=self.simulate_pressed)
        simulate_button.pack(pady=10)

        self.y_locations = [360, 280, 200, 120]

        self.floor_3 = Label(self.scr, text="Floor 3:   0 people", bg="white", fg="#333333", font=("Roboto", 20))
        self.floor_3.place(x=40, y=120)
        self.floor_2 = Label(self.scr, text="Floor 2:   0 people", bg="white", fg="#333333", font=("Roboto", 20))
        self.floor_2.place(x=40, y=200)
        self.floor_1 = Label(self.scr, text="Floor 1:   0 people", bg="white", fg="#333333", font=("Roboto", 20))
        self.floor_1.place(x=40, y=280)
        self.floor_0 = Label(self.scr, text="Floor 0:   0 people", bg="white", fg="#333333", font=("Roboto", 20))
        self.floor_0.place(x=40, y=360)

        self.elevator = Label(self.scr, text=f"0/{self.max_capacity}", fg="white", bg="#333333", font=("Roboto", 25),
                         width=5, height=1)
        self.elevator.place(x=400, y=360)

        self.floors_lb = [self.floor_0, self.floor_1, self.floor_2, self.floor_3]

        log_button = Button(self.scr, text="View Log", bg="#333333", fg="white", font=("Roboto", 20, "bold"),
                            command=self.view_log)
        log_button.place(x=275, y=475)

    def view_log(self):

        self.log_scr_on = True
        self.log_scr = Toplevel(self.scr)
        self.log_scr.config(bg="white")
        self.log_scr.geometry("900x500")
        self.log_scr.title("Elevator Log")

        page_scrollbar = Scrollbar(self.log_scr)
        page_scrollbar.pack(side=RIGHT, fill=Y)

        self.text_area = Text(self.log_scr, font=("Arial", 15), state=DISABLED, bg="black", fg="white")
        self.text_area.pack(fill=BOTH, expand=1)

    def log_data_to_console(self, message):

        if self.log_scr_on:
            self.text_area.config(state=NORMAL)
            self.text_area.insert(END, message)
            self.text_area.config(state=DISABLED)


    def simulate_pressed(self):

        if self.turn % generation_turn == 0:

            passengers_data, total_no = make_passengers()

            print(total_no)
            self.log_data_to_console(f"{total_no} new people have come. \n")

            # printing
            for person in passengers_data:
                print(f"From Floor {person[0]} to Floor {person[2]} in {person[1]} direction.")

            new_ppl_list = organize_floors(passengers_data)

            for amount in [0, 1, 2, 3]:
                if amount == 3:
                    self.log_data_to_console(f"{new_ppl_list[amount]} new in Floor {amount}.\n")
                else:
                    self.log_data_to_console(f"{new_ppl_list[amount]} new in Floor {amount}, ")

        self.current_elevator_level, self.current_direction, self.current_population = self.move_elevator(self.current_elevator_level,
                                                                                      self.current_direction,
                                                                                      self.current_population)
        print("elevator is at floor", self.current_elevator_level)
        self.log_data_to_console(f"The elevator just reached Floor {self.current_elevator_level} \n")
        self.log_data_to_console(f"Currently, there are {self.current_population} people inside. \n")

        self.elevator.place(x=400, y=self.y_locations[self.current_elevator_level])
        self.elevator.update()

        self.elevator.config(text=f"{self.current_population}/{self.max_capacity}")

        if self.turn % 3 == 0:
            lists = [floor0, floor1, floor2, floor3]

            for floor in lists:
                index_no = lists.index(floor)
                floor_lb = self.floors_lb[index_no]
                floor_lb.config(text=f"Floor {index_no}:   {len(floor)} people")



        self.turn += 1

graphics = GUI(current_elevator_level, current_direction, current_population, max_capacity)
