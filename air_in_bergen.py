#!/usr/bin/python3

import requests
#  import re
#  import time
from datetime import date

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
        print(sted, current_date)
        i = 0
        for el in komponent_index:
            a = el + k
            if temp_komp_id[i] == "time":
                print(temp_komp_id[i], ":", t_split[el+1])
            else:
                print(temp_komp_id[i], ": ", t_split[a])
            i += 1
    else:
        print("Can't get data from the site")
