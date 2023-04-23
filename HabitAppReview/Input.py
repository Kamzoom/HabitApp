import sqlite3
from datetime import datetime, date
from DailyHabit import *
from HabitAppReview import Statistic
from Statistic import *

"""Input habit is the interaction with the user to out in the habits and initialise the database"""
"""the function inputHabit takes the input from user and saves it in the database """


def inputHabit():
    end = False
    """while: the user stops the input"""
    while not end:
        """name of habit input"""
        name = input("Enter the name of the habit")
        """during of habit input"""
        durance = str(input("Enter the durance of the habit in minutes"))
        """startday, will change when the streak is done and will be the new start to caculate a streak"""
        startDay = str(datetime.now())
        """streakDay will be updated, when the first streak is done"""
        streakDay = str(datetime.now())
        """status can change into passive, when the user stops the habit"""
        status = "active"
        weeks = str(input("For how long do you want to do this? Please give the number of weeks"))
        """convert string to integer"""
        weeksINT = int(weeks)
        """periodD of daily habit is weeks*7(days of the week), period in days"""
        periodD = weeksINT * 7
        choose = input("Is this a daily or a weekly habit?")
        """dayFixed is the startday not used to calculate the streak, it doesn't change"""
        dayFixed = str(datetime.now())
        """sumAct ist the sum of active days, the value is stored in the database"""
        sumAct = periodD
        """missed days sum"""
        sumMiss = 0
        """sum streaks"""
        sumStreak = 0
        if choose == "daily":
            """connect database"""
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            """create an instance of class habit"""
            DailyHabit.habit = DailyHabit(name, durance, startDay, status, periodD, streakDay, dayFixed, sumAct,
                                          sumMiss, sumStreak)
            """write the input in to database dailyHabits"""
            cursor.execute("""INSERT INTO dailyHabits  VALUES (?,?,?,?,?,?,?,?,?,?)""",
                           (name, durance, startDay, status, periodD, streakDay, dayFixed, sumAct, sumMiss, sumStreak))
            cursor.close()
            connection.commit()
            connection.close()
        elif choose == "weekly":
            """frequency of habit :  when the habit is daily,the frequency is 7(=every day),if it's weekly it's like te user input"""
            frequency = int(input("How many times in the week is the habit?"))
            """active days in weekly habit muliplied with the number of weeks"""
            periodW = int(frequency) * weeks
            """creates an instance of class weeklyHabit"""
            WeeklyHabit.habit = WeeklyHabit(name, durance, startDay, status, periodW, streakDay, dayFixed, sumAct,
                                            sumMiss, sumStreak, periodW)
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            """write the input into database"""
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
        """if the user input is done, the program stops by entering y, by entering n it is going on"""
        answer = input()
        if answer == "Y":
            end = True
        elif answer == "N":
            end = False


inputHabit()
# DailyHabit.streak()
# DailyHabit.eraseHabit()
# DailyHabit.missed_days()
# WeeklyHabit.active_days()
# DailyHabit.checkOut()
# DailyHabit.notToday()
# statistic.showallDailyinCSV()
# Statistic.activedays()
# Statistic.misseddays()
# Statistic.streakdays()
