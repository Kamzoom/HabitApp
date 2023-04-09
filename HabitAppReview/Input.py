import sqlite3
from datetime import datetime, date
from DailyHabit import *
from HabitAppReview import statistic
from statistic import *


def conDB():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    return cursor, connection


# Input habit is the interaction with the user to out in the habits and initialise the database
"""the funktion inputHabit takes the input from user and saves it in the database """


def inputHabit():
    end = False
    while not end:
        # name of habit input
        print("Enter the name of the habit")
        name = input()
        # during of habit input
        print("Enter the durance of the habit in minutes")
        durance = str(input())
        # startday, will change when the strak is done and will be the new start to caculate a streak
        startDay = str(datetime.now())
        print(startDay)
        # streakDay will be updated, when the first streak is done
        streakDay = str(datetime.now())
        # status can change into passive, when the user stops the habit
        status = "active"
        print("For how long do you want to do this? Please give the number of weeks")
        weeks = str(input())
        weeksINT = int(weeks)
        # periodD of daily habit is weeks*7(days of the week9
        periodD = weeksINT * 7
        print("Is this a daily or a weekly habit?")
        choose = input()
        # dayFixed is the startday not used to calculate the streak
        dayFixed = str(datetime.now())
        print(dayFixed)
        # backV=conDB()
        # print("WHAT IS BACKV", backV)
        # cursor=backV[0]
        # print(cursor)
        # connection=backV[1]
        # active days sum
        sumAct = periodD
        # missed days sum
        sumMiss = 0
        # sum streaks
        sumStreak = 0
        if choose == "daily":
            # connect database
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            # create an instance of class habit
            DailyHabit.habit = DailyHabit(name, durance, startDay, status, periodD, streakDay, dayFixed, sumAct,
                                          sumMiss, sumStreak)
            # write data in to database
            cursor.execute("""INSERT INTO dailyHabits  VALUES (?,?,?,?,?,?,?,?,?,?)""",
                           (name, durance, startDay, status, periodD, streakDay, dayFixed, sumAct, sumMiss, sumStreak))
            cursor.execute('SELECT Name, durance, streakDay FROM dailyHabits')
            result = cursor.fetchall()
            print(result)
            cursor.close()
            connection.commit()
            connection.close()
        elif choose == "weekly":
            # frequency of habit : daily or weekly, when the habit is daily,the frequency is 7(=every day), else its like te user input
            print("How many times in the week is the habit?")
            frequency = int(input())
            # active days in weekly habit
            periodW = int(frequency) * weeks
            # actDW = str(periodW)
            # create an instance of class habit
            WeeklyHabit.habit = WeeklyHabit(name, durance, startDay, status, periodW, streakDay, dayFixed, sumAct,
                                            sumMiss, sumStreak, periodW)
            # backV=conDB()
            # cursor=backV[0]
            # connection=backV[1]
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            # create an instance of class ha
            cursor.execute("""INSERT INTO weeklyHabits VALUES (?, ?, ?,?, ?,?,?,?,?,?,?)""", (
                name, durance, startDay, status, periodW, streakDay, dayFixed, sumAct, sumMiss, sumStreak,
                frequency))
            cursor.close()
            connection.commit()
            connection.close()
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE weeklyHabits SET sumAct=?  WHERE name=? ', (periodW, name))
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

# inputHabit()
# DailyHabit.streak() prüfrn datenbank füllen
# DailyHabit.eraseHabit()
# DailyHabit.missedDays()
# DailyHabit.activeDays()
# DailyHabit.checkOut()
# DailyHabit.notToday()
# statistic.showall()
