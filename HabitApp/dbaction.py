import sqlite3

import cursor
from sqlite3 import Cursor
from datetime import date


connection = sqlite3.connect('HabitdataApp.db')
cursor = connection.cursor()
#cursor.execute("DROP TABLE HabitdataApp.dailyHabits CASCADE")
#cursor.execute("""CREATE TABLE dailyHabits (name VARCHAR PRIMARY KEY, durance INTEGER, startDay VARCHAR, status VARCHAR, period INTEGER,streakday VARCHAR) """)
#cursor.execute("""CREATE TABLE weeklyHabits (name VARCHAR PRIMARY KEY, durance INTEGER, startDay VARCHAR, status VARCHAR, period INTEGER,streakday VARCHAR, frequence INTEGER) """)
#cursor.execute("""INSERT INTO dailyHabits VALUES ('laufen', 2,'2023-03-02',4,'active',8,'2023-02-02')""")
#cursor.execute('SELECT name FROM statisticsHabits')
#cursor.execute(""" dailyHabits ADD COLUMN streakDay VARCHAR """)
#cursor.execute("""CREATE TABLE IF NOT EXISTS statisticHabits(name VARCHAR PRIMARY KEY, sumActive INTEGER, sumMissed INTEGER, sumSTREAKS)""")
#print("Do you want to see the data")
#cursor.execute("ALTER TABLE dailyHabits ADD COLUMN startDayFixed VARCHAR")
#name habit, how many days, how many hours
#cursor.execute('ALTER TABLE dailyHabits DROP COLUMN week')
#result = cursor.fetchall()
#print(result)
#cursor.close()
#connection.commit()
#connection.close()
#today = date.today()
#startDay = date(2023,3,6)
#diff = today-startDay
#print("The difference :",diff)