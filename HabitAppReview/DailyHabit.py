from datetime import datetime, date, timedelta
import sqlite3
from dateutil import parser


# class daily habit, repeated every day
# the arguments name is the name of the habit, durance is the time the habit takes every time,
# startDay is the day when the habit starts, status can be active or passive, when the habit is finished or interrupted,
# streakDay is always when the user makes the habit for 14 days


class DailyHabit:
    """The class DailyHabit contains the name(p.ex.jogging), the durance(is the daily time of an habit), the startday(the day on witch the habit starts, this day will be
    changed, if an habit makes a streak, the status(active or passive), the period(for how long will be the habit(a month or a year), the streakDay(the day wenn the first time the habit is not interrupted for 14 days)
    and startdayFixed of an habit."""

    def __init__(self, name, durance, startDay, status, period, streakDay, startDayFixed, sumAct, sumMiss, sumStreak):
        self.name = name
        self.durance = durance
        self.startDay = startDay
        self.status = status
        self.period = period
        self.streakDay = streakDay
        self.startDayFixed = startDayFixed
        self.sumAct = 0
        self.sumMiss = 0
        self.sumStreak = 0

    # Status of a habit
    @staticmethod
    def checkOut():
        """Turns an active habit to a passive habit and don't track anymore"""
        print("Witch habit do you want to CheckOut")
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name, status FROM dailyHabits')
        result1 = cursor.fetchall()
        print(result1)
        cursor.execute('SELECT Name, status FROM weeklyHabits')
        result2 = cursor.fetchall()
        print(result2)
        toCheck = input()
        print(type(toCheck))
        print("Is this a daily or a weekly habit?")
        result = input()
        if result == "daily":
            cursor.execute('UPDATE dailyHabits SET status = ? WHERE name = ?', ("passive", toCheck))
            result = cursor.fetchall()
            cursor.close()
            connection.commit()
        elif result == "weekly":
            cursor.execute('UPDATE weeklyHabits SET status = ? WHERE name = ?', ("passive", toCheck))
            result = cursor.fetchall()
            cursor.close()
            connection.commit()
            cursor.close()
        connection.close()

    # when the user don't interrupt the habit, he has a streak after 14 days
    @staticmethod
    def streak():
        """After 14 days without interrupting an habit, there is a streak, the data will be synchronized wih the database"""
        print("Do you want to know if you have a Streak?")
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name, startDay FROM dailyHabits')
        result = cursor.fetchall()
        print(result)
        cursor.execute('SELECT Name FROM weeklyHabits')
        result1 = cursor.fetchall()
        print(result1)
        cursor.close()
        connection.commit()
        # first find the habit about which the user wants to know a streak
        print("For which habit do you want to know the streak?")
        toCheck = input()
        print('Is this a weekly or a daily habit?')
        result = input()
        if result == "daily":
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            cursor.execute('SELECT startDay FROM dailyHabits WHERE Name=?', (toCheck,))
            start = cursor.fetchone()
            beg = start[0]
            obj = datetime.strptime(beg, '%Y-%m-%d %H:%M:%S.%f')
            print(type(obj))
            today = datetime.now()
            print(type(today))
            cursor.close()
            connection.commit()
            connection.close()
            diff = today - obj
            print(type(diff))
            print("DIFF", diff)
            print(diff.days)
            days = diff.days
            print(type(days))
            if days < 14:
                rest = 14 - days
                print("REST ", rest)
                print("Keep going, there are still ", rest, " days until a streak ")
            elif days == 14:
                print("Hurrah!!!Your Streak today!!!")
                newStart = datetime.today()
                connection = sqlite3.connect('HabitdataApp.db')
                cursor = connection.cursor()
                cursor.execute('SELECT sumStreak FROM dailyHabits WHERE Name=?', (toCheck,))
                add = cursor.fetchone()

                add1 = add[0]
                print(type(add1))
                add1 += 1
                cursor.execute('UPDATE dailyHabits SET startDay = ?, sumStreak=? WHERE name = ?',
                               (newStart, add1, toCheck))
                cursor.close()
                connection.commit()
                cursor.execute('SELECT sumStreak FROM dailyHabits WHERE Name=?', (toCheck,))
                re = cursor.fetchall()
                print("Neue SUmme ", re)
            elif days > 14:
                diff = today - obj
                # days between begin of the streak and today
                days = diff.days
                # How many straks did you have
                streaksM = days % 14
                print("Your streak was ", days, " days ago, you head ", streaksM, " streaks")
                newStreakTime = streaksM * 14
                # new startday for a Streak
                newDate = obj + timedelta(days=newStreakTime)
                print("Neuesdatum ", newDate)
                connection = sqlite3.connect('HabitdataApp.db')
                cursor = connection.cursor()
                cursor.execute('SELECT sumStreak FROM dailyHabits WHERE Name=?', (toCheck,))
                add = cursor.fetchone()
                add1 = add[0]
                add1 += streaksM
                cursor.execute('UPDATE dailyHabits SET startDay = ?, sumStreak=? WHERE Name = ?',
                               (newDate, add1, toCheck))
                cursor.close()
                connection.commit()

        if result == "weekly":
            cursor = connection.cursor()
            cursor.execute('SELECT startDay FROM weeklyHabits WHERE Name=?', (toCheck,))
            start = cursor.fetchone()
            beg = start[0]
            obj = datetime.strptime(beg, '%Y-%m-%d %H:%M:%S.%f')
            print(type(obj))
            today = datetime.now()
            print(type(today))
            cursor.close()
            connection.commit()
            connection.close()
            diff = today - obj
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            cursor.execute('SELECT frequence FROM weeklyHabits WHERE Name=?', (toCheck,))
            freq = cursor.fetchone()
            print("IST WAS DRIN?", freq)
            # days of the week with habit
            days = freq[0]
            # days of the week without habit
            dif = 7 - days
            # are the days more than 14
            res = (dif + days) * 2
            if days < res:
                print("Keep going!")
            elif days == res:
                print("Hurrah!!!Your Streak today!!!")
                newStart = datetime.today()
                connection = sqlite3.connect('HabitdataApp.db')
                cursor = connection.cursor()
                cursor.execute('SELECT sumStreak FROM weeklyHabits WHERE Name=?', (toCheck,))
                add = cursor.fetchone()
                add += 1
                cursor.execute('UPDATE weeklyHabits SET startDay = ?, sumStreak=? WHERE name = ?',
                               (newStart, add, toCheck))
                cursor.close()
                connection.commit()
            elif days > res:
                diff = today - obj
                # days between begin of the streak and today
                days = diff.days
                # How many straks did you have
                streaksM = days % 14
                print("Your streak was ", days, " days ago, you head ", streaksM, " streaks")
                newStreakTime = streaksM * 14
                # new startday for a Streak
                newDate = obj + timedelta(days=newStreakTime)
                print("Neuesdatum ", newDate)
                connection = sqlite3.connect('HabitdataApp.db')
                cursor = connection.cursor()
                cursor.execute('SELECT sumStreak FROM weeklyHabits WHERE Name=?', (toCheck,))
                add = cursor.fetchone()
                add1 = add[0]
                add1 += streaksM
                cursor.execute('UPDATE weeklyHabits SET startDay = ?, sumStreak=? WHERE Name = ?',
                               (newDate, add1, toCheck))
                cursor.close()
                connection.commit()
            """if active days are not 14, the app makes an output"""

    @staticmethod
    def activeDays():
        """this method calculates how many active days an  user had for an habit"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For which habit do you want to know the missed days?")
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name, sumAct FROM dailyHabits')
        result = cursor.fetchall()
        print(result)
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name, sumAct FROM weeklyHabits')
        result1 = cursor.fetchall()
        print(result1)
        toCheck = input()
        print(type(toCheck))
        print("Is this a daily or a weekly habit?")
        result2 = input()
        if result2 == "daily":
            cursor.execute('SELECT sumAct FROM dailyHabits WHERE name=?', (toCheck,))
            resultA = cursor.fetchone()
            print(resultA)
            cursor.execute('SELECT sunMiss FROM dailyHabits WHERE name=?', (toCheck,))
            resultM = cursor.fetchone()
            activeDays = resultA[0] - resultM[0]
            print("Your active  days ", activeDays)
            connection.close()
        elif result2 == "weekly":
            cursor.execute('SELECT sumAct FROM weeklyHabits WHERE name=?', (toCheck,))
            resultA = cursor.fetchall()
            cursor.execute('SELECT sunMiss FROM weeklyHabits WHERE name=?', (toCheck,))
            resultM = cursor.fetchall()
            activeDays = resultA - resultM
            print("Your active  days ", activeDays)
            connection.close()

    @staticmethod
    def missedDays():
        """This method calculates how many days an habit was not done"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For Which habit do you want to know the missed days?")
        cursor.execute('SELECT Name, streakDay FROM dailyHabits')
        result = cursor.fetchall()
        print(result)
        toCheck = input()
        cursor.execute('SELECT sunMiss FROM statisticHabits WHERE name=?', (toCheck,))
        result = cursor.fetchall()
        print("Your missed days ", result)
        connection.close()

    @staticmethod
    def notToday():
        """this method reduce the active days and changes the startday for a streak"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("Which habit you missed today, this is the list of your daily habits")
        cursor.execute('SELECT Name FROM dailyHabits')
        result = cursor.fetchall()
        print(result)
        print("This is the list of your weekly habits")
        cursor.execute('SELECT Name FROM weeklyHabits')
        result1 = cursor.fetchall()
        print(result1)
        toCheck = str(input())
        print('Is this a weekly or a daily habit?')
        result2 = input()
        if result2 == "daily":
            cursor = connection.cursor()
            cursor.execute('SELECT sumMiss FROM dailyHabits WHERE name =?', (toCheck,))
            result = cursor.fetchone()
            sM = result[0]
            sM += 1
            newStart = date.today()
            cursor.execute('UPDATE dailyHabits SET startDay = ?, sumMiss=? WHERE name = ?', (newStart, sM, toCheck,))
            cursor.close()
            connection.commit()
            cursor = connection.cursor()
            cursor.execute('SELECT sumAct FROM dailyHabits WHERE name=?', (toCheck,))
            sumAS = cursor.fetchone()
            sumAI1 = sumAS[0]
            sumAI1 -= 1
            cursor.execute('UPDATE dailyHabits SET sumAct=? WHERE name = ?', (sumAI1, toCheck,))
            cursor.close()
            connection.commit()
        elif result2 == "weekly":
            cursor = connection.cursor()
            cursor.execute('SELECT sumMiss FROM weeklyHabits WHERE name =?', (toCheck,))
            result = cursor.fetchone()
            print(result)
            sMw = result[0]
            sMw += 1
            newStart = date.today()
            cursor.execute('UPDATE weeklyHabits SET startDay = ?, sumMiss=? WHERE name = ?', (newStart, sMw, toCheck,))
            cursor.close()
            connection.commit()
            cursor = connection.cursor()
            cursor.execute('SELECT sumAct FROM weeklyHabits WHERE name=?', (toCheck,))
            sumAS = cursor.fetchone()
            sumAI1w = sumAS[0]
            sumAI1w -= 1
            cursor.execute('UPDATE weeklyHabits SET sumAct=? WHERE name = ?', (sumAI1w, toCheck,))
            cursor.close()
            connection.commit()

    @staticmethod
    def eraseHabit():
        """this method erase an habit"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name FROM dailyHabits')
        result = cursor.fetchall()
        print("Your daily habits")
        print(result)
        cursor.execute('SELECT Name FROM weeklyHabits')
        result1 = cursor.fetchall()
        print("Your weekly habits")
        print(result1)
        print("Witch habit you want to erase, this is the list of your habits")
        toErase = input()
        print("Is this a daily or a weekly habit?")
        toChoose = input()
        print(type(toChoose))
        if toChoose == "daily":
            cursor.execute("DELETE FROM dailyHabits WHERE name=?", (toErase,))
            connection.commit()
            connection.close()

        elif toChoose == "weekly":
            cursor.execute("DELETE FROM weeklyHabits WHERE name=?", (toErase,))
            connection.commit()
            connection.close()


# class weekly habit, not repeated every day. it inherits from daily habit and has an argument more like frequency. Frequency counts
# the days in the week on witch the habit is

class WeeklyHabit(DailyHabit):
    def __init__(self, name, durance, startDay, status, period, streakDay, startDayFixed, sumAct, sumMiss, sumStreak,
                 frequency):
        super().__init__(name, durance, startDay, status, period, streakDay, startDayFixed, sumAct, sumMiss, sumStreak)
        self.frequency = frequency

    @staticmethod
    def habitSumdaysW():
        pass

    @staticmethod
    def notToday(self):
        pass

    @staticmethod
    def activeDays(self):
        pass
