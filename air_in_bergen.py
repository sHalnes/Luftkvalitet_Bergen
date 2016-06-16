#!/usr/bin/python3

import requests
import timestring
#  import re
#  import time
from datetime import date
import psycopg2
#  import pyodbc

connect_db = psycopg2.connect(database="new_db", user="postgres", password="BAZeN49Def2X", host="127.0.0.1", port="5432")
#  connect_db = psycopg2.connect(database="friskby_db", user="postgres", password="BAZeN49Def2X", host="127.0.0.1", port="5432")

print ("Opened database successfully")

cur = connect_db.cursor()
all_db_values = ['PLACE', 'DATE_TIME', 'PM10', 'PM25', 'NO2', 'O3']

luft_map = {"DANMARKSPLASS": "http://luftkvalitet.info/"
                             "home/overview.aspx?type=2&topic=1&id=%7b4ff685c1-ad51-4468-b2fc-08345d11f447%7d",
            "LODDEFJORD": "http://www.luftkvalitet.info/home/"
                          "overview.aspx?type=2&topic=1&id=%7b751808f5-d561-4737-9185-4ecc0e834975%7d",
            "AASANE": "http://www.luftkvalitet.info/home/"
                      "overview.aspx?type=2&topic=1&id=%7bceade2ac-e62f-4e50-af7c-347e402fff27%7d",
            "RAADHUSET": "http://www.luftkvalitet.info/home/"
                         "overview.aspx?type=2&topic=1&id=%7b5b0ff070-e6e6-4f60-88a3-bd923ac3a7e6%7d"}
komponent_id = ["ctl00_cph_Map_ctl00_gwStation_ctl02_Label2", "PM10", "PM2.5", "NO2", "O3"]

current_date = date.today().isoformat()
# '''
for sted in luft_map:
    text_from_site = requests.get(luft_map[sted])
    if text_from_site.status_code == 200:
        text_from_site = text_from_site.text
        translation_table = dict.fromkeys(map(ord, '"<>='), ' ')
        text_from_site = text_from_site.translate(translation_table)
        t_split = text_from_site.split()
        k = 27  # konstanta
        komponent_index = []
        temp_komp_id = []
        for i in range(len(komponent_id)):
            try:
                index = t_split.index(komponent_id[i], 0, -1)
            except ValueError as e:
                pass
            else:
                komponent_index.append(index)
                temp_komp_id.append(komponent_id[i])
        for i in range(len(temp_komp_id)):
            if temp_komp_id[i] == "ctl00_cph_Map_ctl00_gwStation_ctl02_Label2":
                temp_komp_id[i] = "time"
        #  here instead of output we have to send data to DB
        #  but before we do it we have to check if temp_komp_id is not empty, like if len(temp_komp_id) > 0:

        #  date = '2016-06-16 15:00'
        #  print(timestring.Date(date))
        db_input = []
        if len(temp_komp_id) > 0:
            db_input.append(sted)
            i = 0
            for el in komponent_index:
                a = el + k
                if temp_komp_id[i] == "time":
                    date_time = current_date + " " + t_split[el + 1]
                    date_time = timestring.Date(date_time)
                    db_input.append(date_time)
                  #  print(temp_komp_id[i], ":", t_split[el + 1])
                else:
                    db_input.append(t_split[a])
                    #  print(temp_komp_id[i], ": ", t_split[a])
                i += 1
        #  NB: O3 exists only for Raadhus(?)
      #  cur.execute("INSERT INTO LUFTKVALITET_STATISTIKK (PLACE, DATE_TIME, PM10, PM25, NO2, O3)\
       #             VALUES (db_input)");
       # connect_db.commit()
    #   idea from stackoverflow
        print(db_input)
        cols = ",".join(all_db_values)
     #   qmarks = ','.join(['?' for s in cols])
        insert_statement = "INSERT INTO LUFTKVALITET_STATISTIKK (%s) VALUES (%s);" % (cols, str(db_input))
        cur.execute(insert_statement)
        print("records created successfully")
        connect_db.commit()
        #  print(sted, current_date)

    else:
        print("Can't get data from the site")
# Luftkvalitet_Bergen
#'''
connect_db.close()

'''data = [
    ('user_name', "Adam 'Adi' Bobek"), ('user_age', 23), ('person_name', "Jurek 'Jerry' Jimowski") ,('person_age', 28),
    ]
data = dict(data)
cols = ",".join(data.keys())
qmarks = ','.join(['?' for s in data.keys()])
values = [v for v in data.values()]
insert_statement = "INSERT INTO users (%s) VALUES (%s);" % (cols, qmarks)

import pyodbc
connection = pyodbc.connect('DSN=pglocal')
cursor = connection.cursor()
cursor.execute(insert_statement, values)
connection.commit()'''