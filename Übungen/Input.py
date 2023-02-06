# from tkinter import *
from datetime import date
from datetime import datetime

# import switch as switch
# boolean variable to reach end of user input
end = False
# int variable to count habits
global countDailyhabit
countDailyhabit = 0
global countWeeklyHabit
countWeeklyHabit = 0

# lists of habits
weeklyHabitlist = []

weeklySum = []
dailyHabitlist = []

dailySum = []


# class daily habit, repeated every day
class DailyHabit():
    dailyChecklist = [1, 1, 1, 1, 1, 1, 1]

    def __init__(self, name, durance, startDay, status, period):
        self.name = name
        self.durance = durance
        self.startDay = startDay
        self.status = status
        self.period = period

    # Status of an habit
    def checkOut(self):
        """Turns an active habit to an passiv habit and don't track anymore"""
        # beenden und auf passiv setzen
        if self.status == "aktiv":
            status = "passiv"

    # set an habit at null if not done
    def notToday(self):
        """the user can note, if he didn't do the habit at this day"""
        today = datetime.today().weekday()
        self.dailyChecklist[today] = 0

    def days(self):
        pass

    def streak(self):
        pass

    def putToDatabase(self):
        pass

    def doneDays(self):
        pass

    def finsihedHabit(self):
        pass

    def habitSumdays(self):
        pass


# class weekly habit, not repeated every day
class WeeklyHabit(DailyHabit):
    days = []
    weeklyChecklist = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, name, durance, startDay, status, period):
        super().__init__(name, durance, startDay, status)

    def __init__(self, frequence):
        self.frequence = frequence

    def notToday(self):
        print("Whitch habit you missed today, this is the list of your weekly habits")
        print(weeklyHabitlist.WeeklyHabit.name)
        toCheck = input()
        today = datetime.today().weekday()
        self.weeklyChecklist[today] = 0
        # while not end, take the user input

    def changeFrequence(self):
        pass

    def habitSumdays(self):
        pass


def inputHabit():
    end = False
    while not end:
        # mane of habit input
        print("Enter the name of the habit")
        name = input()
        # during of habit input
        print("Enter the durance habit")
        durance = (input())
        startDay = datetime.now()
        print(startDay)
        # frequence of habit : daily or weekly, when the habit is daily, it wiil
        # be stored every day in the list habit, if not it will
        # be stored at the days of this habit
        status = "aktiv"
        print("For how long do you want to do this? Please give the number of weeks")
        period = input()
        print("Is this a daily or a weekly habit?")
        choose = input()
        if choose == "daily":
            countDailyhabit += 1
            dailyHabitlist.append(DailyHabit(name, durance, startDay, status, period))
        elif choose == "weekly":
            countWeeklyHabit += 1
            print("How many times in the week is the habit?")
            frequence = int(input())
            weeklyHabitlist.append(WeeklyHabit(frequence))
            while frequence > 0:
                print(
                    "Enter the days on witch the habit is 0 for monday, 1  tuesday, 2 wenesday, 3 thursday, 4 friday, 5 sutarday, 6 sunday")
                day = input()
                name.weeklyChecklist[day] = 1
                frequence -= 1

    print("If you are ready enter Y, if not enter N")
    # if the usr input is done, the program stops by entering y, by entering n its going on
    answer = input()
    if answer == "Y":
        end = True
    elif answer == "N":
        end = False


def coutHabits():
    pass


def outPutListofHabits():
    pass
