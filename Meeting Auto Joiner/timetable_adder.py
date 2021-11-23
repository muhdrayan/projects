import sqlite3

database = sqlite3.connect("Timetable.db")
c = database.cursor()

c.execute("INSERT INTO timings8R values(?,?,?,?,?,?,?,?,?,?)", ("07:00", "07:15", "07:55", "08:45",	"09:23", "10:09", "10:45", "11:35", "12:15", "12:51"))
database.commit()

c.execute("INSERT INTO timetable8R values(?,?,?,?,?,?,?,?,?,?)", ("Sunday", "main", "main", "main", "main", "sl", "main", "tl", "main", "sl"))
database.commit()

c.execute("INSERT INTO timetable8R values(?,?,?,?,?,?,?,?,?,?)", ("Monday", "main", "main", "main", "main", "sl", "main",
database.commit()

c.execute("INSERT INTO timetable8R values(?,?,?,?,?,?,?,?,?,?)", ("Tuesday", "main", "main", "main", "main", "sl", "main",
databse.commit()

c.execute("INSERT INTO timetable8R values(?,?,?,?,?,?,?,?,?,?)", ("Wednesday", "main", "main", "main", "main", "sl", "main",
database.commit()

c.execute("INSERT INTO timetable8R values(?,?,?,?,?,?,?,?,?,?)", ("Thursday", "main", "main", "main", "main", "sl", "main",
database.commit()