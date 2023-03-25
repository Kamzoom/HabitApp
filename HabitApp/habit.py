import sqlite3
# class daily habit, repeated every day
# the arguments name is the name of the habit, durance is the time the habit takes every time,
# startDay is the day when the habit starts, status can be active or passive, when the habit is finished or interrupted,
# streakDay is always when the user makes the habit for 14 days
class DailyHabit:
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
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name FROM dailyHabits')
        result = cursor.fetchall()
        print(result)
        cursor.execute('SELECT Name FROM weeklyHabits')
        result = cursor.fetchall()
        print(result)
        toStop = input()
        cursor.execute('UPDATE dailyHabits SET status = ? WHERE name = ?', ("passive", toStop))
        cursor.close()
        connection.commit()
        connection.close()


    #when the user dont interrupt the habit, he has a streak after 14 days
    def streak(self):
        print("Do you want to know if you have a Streak? For witch habit?")
        #first find the habit about which the user wants to know a streak
        toCheck = str(input())
        #actually date
        streakDay = str(datetime.now())
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        cursor.execute('SELECT streakDay FROM dailyHabits WHERE name=?,(toCheck)')
        result = cursor.fetchall()
        #calculate the difference between startday and actually date
        streak = datetime.now() - result
        cursor.execute('SELECT startDay FROM dailyHabits WHERE name=?,(toCheck)')
        result2 = cursor.fetchall()
        if streak >= 14:
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
            print("Not yet, work more for a streak")
        cursor.close()
        connection.commit()
        connection.close()

    def activeDays(self):
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For Witch habit do you want to know the missed days?")
        toCheck = input()
        cursor.execute('SELECT startDayFixed FROM dailyHabits WHERE name=?,(toCheck)')
        result = cursor.fetchall()
        cursor.execute('SELECT sumMissed FROM statisticHabits WHERE name=?,(toCheck)')
        result2 = cursor.fetchall()
        cursor.execute('SELECT startDayFixed FROM dailyHabits WHERE name=?,(toCheck)')
        result3=cursor.fetchall()
        activeDays = datetime()-result3-result2
        print("Your mactive  days ",activeDays)
        connection.close()

    def missedDays(self):
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("For Witch habit do you want to know the missed days?")
        toCheck = input()
        cursor.execute('SELECT sumMissed FROM statisticHabits WHERE name=?,(toCheck)')
        result = cursor.fetchall()
        print("Your missed days ",result)
        connection.close()
    def notToday(self):
        connection = sqlite3.connect('HabitdataApp.db')
        cursor = connection.cursor()
        print("Witch habit you missed today, this is the list of your daily habits")
        toCheck = str(input())
        cursor.execute('SELECT Name FROM dailyHabits WHERE name =?,(toCheck)')
        result = cursor.fetchall()
        print(result)
        cursor.execute('SELECT sumActive FROM statisticHabits WHERE name=?,(toCheck)')
        sumA = cursor.fetchall()
        sumA -=1
        cursor.execute('UPDATE statisticHabits SET  sumActive=? WHERE name=?', (sumA, result))
        cursor.execute('SELECT sumMissed FROM statisticHabits')
        sumM = cursor.fetchall()
        sumM += 1
        cursor.execute('UPDATE statisticHabits SET  sumMissed=? WHERE name=?', (sumM, result))
        streakDay = str(date.today())
        cursor.execute("UPDATE dailyHabits SET streakDay=? WHERE name=?", (streakDay, result))
        cursor.close()
        connection.commit()
        connection.close()
    def eraseHabit(self):
        pass


# class weekly habit, not repeated every day. it inherits from daily habit and has an argument more like frequency. Frequency counts
# the days in the week on witch the habit is
class WeeklyHabit(DailyHabit):
    def __init__(self, name, durance, startDay, status, period, streakDay,startDayFixed, frequency):
        super().__init__(name, durance, startDay, status, period, streakDay, startDayFixed)
        self.frequency = frequency

    def habitSumdaysW(self):
        pass
    # def countWeeklyHabit(self):
    #     global countWeeklyHabit
    #     self.countWeeklyHabit +=1