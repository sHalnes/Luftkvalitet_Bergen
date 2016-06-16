#!/usr/bin/python

# import timestring
import psycopg2

connect_db = psycopg2.connect(database="new_db", user="postgres", password="BAZeN49Def2X", host="127.0.0.1", port="5432")

print("Opened database successfully")

cur = connect_db.cursor()
cur.execute('''CREATE TABLE LUFTKVALITET_STATISTIKK
      (PLACE           CHAR(20)     NOT NULL,
      DATE_TIME         TIMESTAMP WITH TIME ZONE    NOT NULL,
       PM10            REAL,
       PM25            REAL,
       NO2            REAL,
       O3            REAL);''')
print("Table created successfully")

connect_db.commit()
connect_db.close()

#  date = '2016-06-16 15:00'
#  print(timestring.Date(date))