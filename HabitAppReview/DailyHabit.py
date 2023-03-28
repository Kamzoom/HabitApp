from datetime import datetime, date
import sqlite3
# class daily habit, repeated every day
# the arguments name is the name of the habit, durance is the time the habit takes every time,
# startDay is the day when the habit starts, status can be active or passive, when the habit is finished or interrupted,
# streakDay is always when the user makes the habit for 14 days


class DailyHabit:
    """The class DailyHabit contains the name(p.ex.jogging), the durance(is the daily time of an habit), the startday(the day on witch the habit starts, this day will be
    changed, if an habit makes a streak, the status(active or passive), the period(for how long will be the habit(a month or a year), the streakDay(the day wenn the first time the habit is not interrupted for 14 days)
    and startdayFixed of an habit."""

    def __init__(self, name, durance, startDay, status, period, streakDay, startDayFixed):
        self.name = name
        self.durance = durance
        self.startDay = startDay
        self.status = status
        self.period = period
        self.streakDay = streakDay
        self.startDayFixed = startDayFixed

    # Status of a habit
    def checkOut(self):
        """Turns an active habit to a passive habit and don't track anymore"""
        print("Witch habit do you missed today, this is the list of your daily and weekly habits")
        habitname = input()
        print("Is this a daily or a weekly habit?")
        frec = str(input)
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        if frec == "daily":
            cursor.execute('UPDATE dailyHabits SET status = ? WHERE name = ?', ("passive", habitname))
            result = cursor.fetchall()
        else:
            cursor.execute('UPDATE weeklyHabits SET status = ? WHERE name = ?', ("passive", habitname))
            result = cursor.fetchall()

    # when the user dont interrupt the habit, he has a streak after 14 days
    def streak(self):
        """After 14 days without interrupting an habit, there is a streak, the data will be synchronized wih the database"""
        print("Do you want to know if you have a Streak? For witch habit?")
        # first find the habit about which the user wants to know a streak
        toCheck = str(input())
        # actually date
        streakDay = str(datetime.now())
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT streakDay FROM dailyHabits WHERE name=?,(toCheck)')
        result = cursor.fetchall()
        # calculate the difference between startday and actually date
        streak = datetime.now() - result
        cursor.execute('SELECT startDay FROM dailyHabits WHERE name=?,(toCheck)')
        result2 = cursor.fetchall()
        if streak >= 14:
            """if there is a streak, the app makes an output, and the the day to count a streak will be actualised,
            the sum of streaks is elevated, the data are synchonized with the database"""
            print("Hurrah!!!Your Streak today!!!")
            newStreak = str(result2 + 14)
            newStart = str(result + 1)
            cursor.execute('UPDATE dailyHabits SET streakDay=? WHERE name=?,(newStreak,toCheck ) ')
            cursor.execute('UPDATE dailyHabits SET startDay=? WHERE name=?,(newStart,toCheck ) ')
            cursor.execute('SELECT sumStreaks FROM statisticHabits WHERE name=?,(toCheck)')
            result = cursor.fetchall()
            resultNew = str(result + 1)
            cursor.execute('UPDATE statisticHabits SET sumStreaks=? WHERE name=?,(resultNew, toCheck)')
        elif streak < 14:
            """if active days are not 14, the app makes an output"""
            print("Not yet, work more for a streak")
        cursor.close()
        connection.commit()
        connection.close()

    def activeDays(self):
        """this method calculates how many active days an  user had for an habit"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For Witch habit do you want to know the missed days?")
        toCheck = input()
        cursor.execute('SELECT startDayFixed FROM dailyHabits WHERE name=?,(toCheck)')
        result = cursor.fetchall()
        cursor.execute('SELECT sumMissed FROM statisticHabits WHERE name=?,(toCheck)')
        result2 = cursor.fetchall()
        activeDays = datetime() - result - result2
        print("Your active  days ", activeDays)
        connection.close()

    def missedDays(self):
        """This method calculates how many days an habit was not done"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For Witch habit do you want to know the missed days?")
        toCheck = input()
        cursor.execute('SELECT sumMissed FROM statisticHabits WHERE name=?,(toCheck)')
        result = cursor.fetchall()
        print("Your missed days ", result)
        connection.close()

    def notToday(self):
        """this method reduce the active days and changes the startday for a streak"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("Witch habit you missed today, this is the list of your daily habits")
        toCheck = str(input())
        cursor.execute('SELECT Name FROM dailyHabits WHERE name =?,(toCheck)')
        result = cursor.fetchall()
        print(result)
        cursor.execute('SELECT sumActive FROM statisticHabits WHERE name=?,(toCheck)')
        sumA = cursor.fetchall()
        sumA -= 1
        cursor.execute('UPDATE statisticHabits SET  sumActive=? WHERE name=?', (sumA, result))
        cursor.execute('SELECT sumMissed FROM statisticHabits')
        sumM = cursor.fetchall()
        sumM += 1
        cursor.execute('UPDATE statisticHabits SET  sumMissed=? WHERE name=?', (sumM, result))
        streakDay = str(date.today())
        cursor.execute("UPDATE dailyHabits SET startDay=? WHERE name=?", (streakDay, result))
        cursor.close()
        connection.commit()
        connection.close()

    def eraseHabit(self):
        """this method erase an habit"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("Witch habit you want to erase, this is the list of your daily habits")
        toErase = str(input())
        print("Is this a daily or a weekly habit?")
        table = str(input)
        if table == "daily":
            cursor.execute("DELETE FROM dailyHabit WHERE name=?", ('toErase',))
        else:
            cursor.execute("DELETE FROM weeklyHabit WHERE name=?", ('toErase',))
        connection.commit()
        connection.close()


# class weekly habit, not repeated every day. it inherits from daily habit and has an argument more like frequency. Frequency counts
# the days in the week on witch the habit is
class WeeklyHabit(DailyHabit):
    def __init__(self, name, durance, startDay, status, period, streakDay, startDayFixed, frequency):
        super().__init__(name, durance, startDay, status, period, streakDay, startDayFixed)
        self.frequency = frequency

    def habitSumdaysW(self):
        pass

    def notToday(self):
        pass

    def activeDays(self):
        pass
