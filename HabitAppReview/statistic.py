import sqlite3
from datetime import datetime, date
from typing import List, Any
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# active days, missed day
# Streaks
# active, passiv
def activedays():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    # cursor.execute('SELECT sumAct FROM dailyHabits ')
    cursor.execute('select sumAct from weeklyHabits')
    result = cursor.fetchall()
    y = []
    for n in result:
        print(n[0])
        y.append(n[0])
    print(y)
    cursor.execute('select * from weeklyHabits')
    result1 = cursor.fetchall()
    x = []
    for n in result1:
        print(n[0])
        x.append(n[0])
    print(x)

    plt.xlabel("active days")
    plt.ylabel("counter")
    plt.title("active days")
    plt.bar(x, y, color='grey', width=0.5)
    plt.show()
    cursor.close()
    connection.commit()
    connection.close()


def misseddays():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    cursor.execute('SELECT sumMiss FROM dailyHabits ')
    result = cursor.fetchall()
    y = []
    for n in result:
        print(n[0])
        y.append(n[0])
    print(y)
    cursor.execute('select * from weeklyHabits')
    result1 = cursor.fetchall()
    x = []
    for n in result1:
        print(n[0])
        x.append(n[0])
    print(x)
    plt.xlabel("missed days")
    plt.ylabel("counter")
    plt.title("missed days")
    plt.bar(x, y, color='grey', width=0.5)
    plt.show()
    cursor.close()
    connection.commit()
    connection.close()


def streakdays():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    cursor.execute('SELECT sumStreak FROM dailyHabits')
    result = cursor.fetchall()
    print(result)
    y = []
    for n in result:
        print(n[0])
        y.append(n[0])
    print(y)
    cursor.execute('select * from weeklyHabits')
    result1 = cursor.fetchall()
    x = []
    for n in result1:
        print(n[0])
        x.append(n[0])
    print(x)
    plt.xlabel("streak days")
    plt.ylabel("counter")
    plt.title("streak days")
    plt.bar(x, y, color='red', width=0.5)
    plt.show()
    cursor.close()
    connection.commit()
    connection.close()


def showallDailyinCSV():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM dailyHabits')
    result1 = cursor.fetchall()
    print(result1)
    df = pd.read_sql_query("SELECT * FROM dailyHabits", connection)
    df.to_csv('dailyHabits_new.csv')
    cursor.close()
    connection.commit()
    connection.close()


def showallWeeklyinCSV():
    connection = sqlite3.connect('HabitdataApp.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM weeklyHabits')
    result1 = cursor.fetchall()
    print(result1)
    df = pd.read_sql_query("SELECT * FROM weeklyHabits", connection)
    df.to_csv('weeklyHabits_new.csv')
    cursor.close()
    connection.commit()
    connection.close()


# misseddays()
showallWeeklyinCSV()
showallDailyinCSV()
# streakdays()
