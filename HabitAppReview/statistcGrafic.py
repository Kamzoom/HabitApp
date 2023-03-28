import sqlite3
from datetime import datetime, date
import matplotlib as plt
import matplotlib.pyplot as plt


# active days, missed day
# Streaks
# active, passiv
def activedays():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    print("Witch habit you missed today, this is the list of your daily habits")
    toCheck = str(input())
    cursor.execute('SELECT sumActive FROM dailyHabits WHERE name =?,(* )')
    result = cursor.fetchall()
    print(result)
    plt.plot(result)
    plt.show()
    cursor.close()
    connection.commit()
    connection.close()


def misseddays():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    print("Witch habit you missed today, this is the list of your daily habits")
    toCheck = str(input())
    cursor.execute('SELECT sumMissed FROM dailyHabits WHERE name =?,(* )')
    result = cursor.fetchall()
    print(result)
    plt.plot(result)
    plt.show()
    cursor.close()
    connection.commit()
    connection.close()


def misseddays():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    print("Witch habit you missed today, this is the list of your daily habits")
    toCheck = str(input())
    cursor.execute('SELECT sumSTREAKS FROM dailyHabits WHERE name =?,(* )')
    result = cursor.fetchall()
    print(result)
    plt.plot(result)
    plt.show()
    cursor.close()
    connection.commit()
    connection.close()


daten = [4, 7, 1, 9, 5, 2, 8]
plt.plot(daten)
plt.show()
