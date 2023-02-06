import  sqlite3
from sqlite3 import Cursor

import cursor as cursor
#Verbindung zur Datenbank und erstellen der Datenbank habitdata
connection = sqlite3.connect('habitdata.db')
cursor = connection.cursor()
# cursor.execute("""CREATE TABLE habits (name VARCHAR PRIMARY KEY, durance INTEGER, frequence INTEGER ) """)
# cursor.execute("""INSERT INTO habits VALUES ('laufen', 2, 3)""")
#cursor.execute("""INSERT INTO habits VALUES ('essen', 4, 3)""")
#cursor.execute("""ALTER TABLE habits ADD COLUMN CountStrike INTEGER""")
print("Do you want to see the data")
#name habit, how many days, how many hours
cursor.execute('SELECT Name FROM habits')
result = cursor.fetchall()
print(result)
connection.commit()
cursor.close()
