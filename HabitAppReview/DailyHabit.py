from datetime import datetime, date, timedelta
import sqlite3
from dateutil import parser


# class daily habit, repeated every day
# the arguments name is the name of the habit, durance is the time the habit takes every time,
# startDay is the day when the habit starts, status can be active or passive, when the habit is finished or interrupted,
# streakDay is always when the user makes the habit for 14 days


class DailyHabit:
    """The class dailyHabit contains attributes like the name(p.ex.jogging), the durance(is the daily time of an habit), the startday(the day on witch the habit starts, this day will be
    changed, if an habit makes a streak, the status(active or passive), the period(for how long will be the habit(a month or a year), the count of streakDays(the day wenn the first time the habit is not interrupted for 14 days)
    and startdayFixed of an habit, also the sum of active days, of missed days and the sum of streaks"""

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
        """Turns an active habit to a passive habit and stops tracking"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name, status FROM dailyHabits')
        daily_habits = cursor.fetchall()
        print(daily_habits)
        cursor.execute('SELECT Name, status FROM weeklyHabits')
        weekly_habits = cursor.fetchall()
        print(weekly_habits)
        habit_name = input("\nWhich habit do you want to check out? ")
        habit_type = None
        if habit_name in [h[0] for h in daily_habits]:
            habit_type = 'daily'
        elif habit_name in [h[0] for h in weekly_habits]:
            habit_type = 'weekly'
        if habit_type:
            cursor.execute(f"UPDATE {habit_type.capitalize()}Habits SET status=? WHERE name=?", ("passive", habit_name))
            connection.commit()
            print(f"\nHabit '{habit_name}' successfully checked out.")
        else:
            print(f"\nHabit '{habit_name}' not found.")

            connection.commit()
            cursor.close()
        connection.close()

    """when the user don't interrupt the habit, he has a streak after 14 days"""
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
        """first find the habit about which the user wants to know a streak"""
        print("For which habit do you want to know the streak?")
        toCheck = input()
        print('Is this a weekly or a daily habit?')
        result = input()
        if result == "daily":
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            cursor.execute('SELECT startDay FROM dailyHabits WHERE Name=?', (toCheck,))
            start = cursor.fetchone()
            """read the startday from the database and convert it to a datatimeformat"""
            beg = start[0]
            obj = datetime.strptime(beg, '%Y-%m-%d %H:%M:%S.%f')
            """store the actually date"""
            today = datetime.now()
            cursor.close()
            connection.commit()
            connection.close()
            """calculate the difference between the start of habit an the actually date"""
            diff = today - obj
            """convert the date to integer"""
            days = diff.days
            """if the difference is bigger than 14 days: there is a streak(or more streaks),if it is 14: there is one straek, if it's smaller than 14: there is no streak"""
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
                """increment sum of streaks"""
                add1 = add[0]
                add1 += 1
                """write to database, update the startday of a streak, the begin for a new streak is today"""
                cursor.execute('UPDATE dailyHabits SET startDay = ?, sumStreak=? WHERE name = ?',
                               (newStart, add1, toCheck))
                cursor.close()
                connection.commit()
                """if the difference is bigger than 14, calculate how many streaks are done"""
            elif days > 14:
                diff = today - obj
                """days between begin of the streak and today"""
                days = diff.days
                """How many streaks are done, calculate all days with modulo"""
                streaksM = days % 14
                print("Your streak was ", days, " days ago, you head ", streaksM, " streaks")
                """calculate the startday for a new streak"""
                newStreakTime = streaksM * 14
                """new startday for a Streak"""
                newDate = obj + timedelta(days=newStreakTime)
                connection = sqlite3.connect('HabitdataApp.db')
                cursor = connection.cursor()
                cursor.execute('SELECT sumStreak FROM dailyHabits WHERE Name=?', (toCheck,))
                """calculate the streak sum"""
                add = cursor.fetchone()
                add1 = add[0]
                add1 += streaksM
                """update the streak sum and the begin of a new streak"""
                cursor.execute('UPDATE dailyHabits SET startDay = ?, sumStreak=? WHERE Name = ?',
                               (newDate, add1, toCheck))
                cursor.close()
                connection.commit()

        if result == "weekly":
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            """read the startday of a streak in the database"""
            cursor.execute('SELECT startDay FROM weeklyHabits WHERE Name=?', (toCheck,))
            start = cursor.fetchone()
            """convert the string to datatime"""
            beg = start[0]
            obj = datetime.strptime(beg, '%Y-%m-%d %H:%M:%S.%f')
            """store the actually date"""
            today = datetime.now()
            cursor.close()
            connection.commit()
            connection.close()
            diff = today - obj
            connection = sqlite3.connect('HabitdataApp.db')
            cursor = connection.cursor()
            cursor.execute('SELECT frequence FROM weeklyHabits WHERE Name=?', (toCheck,))
            freq = cursor.fetchone()
            # days of the week with habit
            days = freq[0]
            # days of the week without habit
            dif = 7 - days
            # are the days more than 14
            res = (dif + days) * 2
            """if days smaller than 14, no streak"""
            if days < res:
                print("Keep going!")
                """if days equal to 14: one streak"""
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
                """if days more than 14, calculate the streaks"""
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
                connection = sqlite3.connect('HabitdataApp.db')
                cursor = connection.cursor()
                cursor.execute('SELECT sumStreak FROM weeklyHabits WHERE Name=?', (toCheck,))
                add = cursor.fetchone()
                #update the number of streaks
                add1 = add[0]
                add1 += streaksM
                cursor.execute('UPDATE weeklyHabits SET startDay = ?, sumStreak=? WHERE Name = ?',
                               (newDate, add1, toCheck))
                cursor.close()
                connection.commit()
            """if active days are not 14, the app makes an output"""

    @staticmethod
    def active_days():
        """this method calculates how many active days an user had for an habit"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        # Display the available habits to the user
        print("Your daily habits:")
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name, sumAct, sumMiss FROM dailyHabits')
        habits = cursor.fetchall()
        for habit in habits:
            print(f"- {habit[0]} ({habit[1]} active days)")
        # Prompt the user for the habit they want to check
        connection.close()

    @staticmethod
    def missed_days():
        """This method calculates shows how many days an habit was not done"""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For Which habit do you want to know the missed days?")
        cursor.execute('SELECT Name, streakDay FROM dailyHabits')
        result = cursor.fetchall()
        for habit in result:
            print(f"- {habit[0]}")
        toCheck = input()
        cursor.execute('SELECT sumMiss FROM dailyHabits WHERE name=?', (toCheck,))
        result = cursor.fetchall()
        print("Your missed days ", result)
        connection.close()

    @staticmethod
    def notToday():
        """if the user missed an habit, this method reduce the active days and changes the startday for a streak"""
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
            #convert the string to integer
            sM = result[0]
            sM += 1
            #update a startday for a streak
            newStart = date.today()
            cursor.execute('UPDATE dailyHabits SET startDay = ?, sumMiss=? WHERE name = ?', (newStart, sM, toCheck,))
            cursor.close()
            connection.commit()
            cursor = connection.cursor()
            cursor.execute('SELECT sumAct FROM dailyHabits WHERE name=?', (toCheck,))
            #reduce the count of active days and update the database
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
        """this method erase a habit from the database."""
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        # Display the available habits to the user
        cursor.execute('SELECT Name FROM dailyHabits')
        daily_habits = cursor.fetchall()
        print("Your daily habits:")
        for habit in daily_habits:
            print(f"- {habit[0]}")
        cursor.execute('SELECT Name FROM weeklyHabits')
        weekly_habits = cursor.fetchall()
        print("Your weekly habits:")
        for habit in weekly_habits:
            print(f"- {habit[0]}")
        # store the name of habit, that shoud be erased
        habit_name = input("\nWhich habit do you want to erase? ")
        # Determine if the habit is daily or weekly
        habit_type = None
        if habit_name in [h[0] for h in daily_habits]:
            habit_type = 'daily'
        elif habit_name in [h[0] for h in weekly_habits]:
            habit_type = 'weekly'

        # Erase the habit from the appropriate table
        if habit_type:
            cursor.execute(f"DELETE FROM {habit_type.capitalize()}Habits WHERE name=?", (habit_name,))
            connection.commit()
            print(f"\nHabit '{habit_name}' successfully erased.")
        else:
            print(f"\nHabit '{habit_name}' not found.")

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
    def active_days():
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name, sumAct FROM weeklyHabits')
        habits = cursor.fetchall()
        for habit in habits:
            print(f"- {habit[0]} ({habit[1]} active days)")
        connection.close()
