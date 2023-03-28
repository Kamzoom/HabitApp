import sqlite3
from datetime import datetime, date
from DailyHabit import *
# Input habit is the interaction with the user to out in the habits and initialise the database
"""the funktion inputHabit takes the input from user and saves it in the database """
def inputHabit():
    end = False
    while not end:
        # name of habit input
        print("Enter the name of the habit")
        name = input()
        # during of habit input
        print("Enter the durance habit in minutes")
        durance = str(input())
        # startday, will change when the strak is done and will be the new start to caculate a streak
        startDay = str(datetime.now())
        print(startDay)
        streakDay = str(datetime.now())
        # frequency of habit : daily or weekly, when the habit is daily, it will
        status = "active"
        print("For how long do you want to do this? Please give the number of weeks")
        weeks = str(input())
        periodD = weeks * 7
        print("Is this a daily or a weekly habit?")
        choose = input()
        # startday not used to calculate the streak
        dayFixed = str(datetime.now())

        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO statisticHabits VALUES(?,?,?,?)""", (name, periodD, 0, 0))
        if choose == "daily":
            DailyHabit.habit = DailyHabit(name, durance, startDay, status, periodD, streakDay, dayFixed)
            cursor.execute("""INSERT INTO dailyHabits  VALUES (?,?,?,?,?,?,?)""",
                           (name, durance, startDay, status, periodD, streakDay, dayFixed))
            # Write in to database
            cursor.execute('SELECT Name, durance, streakDay FROM dailyHabits')
            result = cursor.fetchall()
            print(result)
            cursor.close()
            connection.commit()
            connection.close()
        elif choose == "weekly":
            # Weekly habit is not every day, frequency gives how many days in the week the habit is
            print("How many times in the week is the habit?")
            frequency = int(input())
            # active days
            periodW = frequency * weeks
            actDW = str(periodW)
            habit = habit.WeeklyHabit(name, durance, startDay, status, periodW, streakDay, dayFixed, frequency)
            cursor.execute("""INSERT INTO weeklyHabits VALUES (?, ?, ?,?, ?,?,?,?)""", (
                habit.name, habit.durance, habit.startDay, habit.status, actDW, habit.streakDay, dayFixed,
                habit.frequency))
            cursor.execute('UPDATE statisticHabits SET sumActive=res WHERE name = periodW')
            cursor.close()
            connection.commit()
            connection.close()
    print("If you are ready enter Y, if not enter N")
    # if the user input is done, the program stops by entering y, by entering n it is going on
    answer = input()
    if answer == "Y":
        end = True
    elif answer == "N":
        end = False


inputHabit()
